# core_module.py — contains two things:
# 1. CoreWorker: pulls packets from raw_queue, verifies their cryptographic signature,
#    sends verified ones to an intermediate queue
# 2. Aggregator: collects from intermediate queue, computes sliding window average,
#    pushes final results to processed_queue

import hashlib
import multiprocessing
from abc import ABC, abstractmethod  # enforces structure across modules (DIP)
from collections import deque        # deque is a fast list used for the sliding window


# abstract base class — all core modules must implement run()
class AbstractCoreModule(ABC):
    @abstractmethod
    def run(self):
        pass


# ─────────────────────────────────────────
# FUNCTIONAL CORE (pure functions, no side effects)
# these functions only take inputs and return outputs — no global state touched
# ─────────────────────────────────────────

def verify_signature(packet: dict, secret_key: str, iterations: int) -> bool:
    """
    pure function — checks if the packet's signature matches what we compute.
    uses PBKDF2-HMAC-SHA256 (a heavy cryptographic hash, 100k iterations)
    key = secret password, salt = the raw value string rounded to 2 decimal places
    returns True if authentic, False if tampered/fake
    """
    # round the metric value to 2 decimal places and turn it into a string (matches how signature was made)
    raw_value_str = f"{packet['metric_value']:.2f}"

    # the secret key is the "password", the raw value string is the "salt"
    password_bytes = secret_key.encode('utf-8')
    salt_bytes = raw_value_str.encode('utf-8')

    # compute the expected hash using the same algorithm that created the signature
    computed_hash = hashlib.pbkdf2_hmac(
        hash_name='sha256',
        password=password_bytes,
        salt=salt_bytes,
        iterations=iterations
    ).hex()  # convert bytes to hex string for comparison

    # compare computed hash with the signature attached to the packet
    return computed_hash == packet['security_hash']


def compute_sliding_average(window: deque) -> float:
    """
    pure function — given a sliding window (list of recent values), returns their average.
    this is the "Functional Core" — it has no state, just math
    """
    if len(window) == 0:
        return 0.0
    return sum(window) / len(window)


# ─────────────────────────────────────────
# IMPERATIVE SHELL (manages state and queues)
# ─────────────────────────────────────────

class CoreWorker(AbstractCoreModule):
    """
    one worker process — pulls packets from raw_queue,
    runs signature verification (stateless/parallel-safe),
    pushes authentic packets to intermediate_queue
    """

    def __init__(self, config: dict, raw_queue: multiprocessing.Queue,
                 intermediate_queue: multiprocessing.Queue, worker_id: int):
        self.config = config
        self.raw_queue = raw_queue                   # read from here
        self.intermediate_queue = intermediate_queue  # write verified packets here
        self.worker_id = worker_id                   # just for logging

        # read signing config values once at startup
        self.secret_key = config["processing"]["stateless_tasks"]["secret_key"]
        self.iterations = config["processing"]["stateless_tasks"]["iterations"]

    def run(self):
        """
        main loop — keeps pulling packets until it gets the None stop signal
        """
        print(f"[CoreWorker-{self.worker_id}] Started.")

        while True:
            # block here until a packet is available in the raw queue
            packet = self.raw_queue.get()

            # None is the stop signal sent by InputModule — exit the loop
            if packet is None:
                # forward the stop signal so Aggregator also knows to stop eventually
                self.intermediate_queue.put(None)
                print(f"[CoreWorker-{self.worker_id}] Received stop signal. Exiting.")
                break

            # call the pure function to check if this packet is authentic
            is_valid = verify_signature(packet, self.secret_key, self.iterations)

            if is_valid:
                # packet passed verification — send it forward
                self.intermediate_queue.put(packet)
            else:
                # packet failed — drop it silently (or log for debugging)
                print(f"[CoreWorker-{self.worker_id}] DROPPED fake packet: {packet.get('entity_name')}")


class Aggregator(AbstractCoreModule):
    """
    single aggregator process — gathers verified packets from intermediate_queue,
    computes sliding window average using the Functional Core pattern,
    pushes final enriched packets to processed_queue

    IMPERATIVE SHELL: this class manages the mutable sliding window state
    FUNCTIONAL CORE:  compute_sliding_average() does the actual math (pure function above)
    """

    def __init__(self, config: dict, intermediate_queue: multiprocessing.Queue,
                 processed_queue: multiprocessing.Queue, num_workers: int):
        self.config = config
        self.intermediate_queue = intermediate_queue  # read verified packets from here
        self.processed_queue = processed_queue        # write enriched packets here
        self.num_workers = num_workers                # need to count how many stop signals to expect

        # window size for sliding average (e.g. last 10 values)
        self.window_size = config["processing"]["stateful_tasks"]["running_average_window_size"]

        # the sliding window — stores last N metric_values (mutable state lives here in the shell)
        self.window = deque(maxlen=self.window_size)

    def run(self):
        """
        main loop — waits for all workers to send their stop signals before quitting.
        this is needed because multiple workers all send None when done
        """
        print("[Aggregator] Started.")
        stop_signals_received = 0

        while True:
            packet = self.intermediate_queue.get()

            if packet is None:
                stop_signals_received += 1
                # only stop when ALL core workers have signaled done
                if stop_signals_received >= self.num_workers:
                    self.processed_queue.put(None)  # signal to Output that we're done
                    print("[Aggregator] All workers done. Sending stop to Output.")
                    break
                continue  # keep waiting for more packets from other workers

            # add this packet's metric value to the sliding window (imperative shell manages state)
            self.window.append(packet['metric_value'])

            # call the pure function to compute average (functional core does the math)
            avg = compute_sliding_average(self.window)

            # attach the computed average to the packet before sending it forward
            packet['computed_metric'] = avg

            # push the enriched packet to the output queue
            self.processed_queue.put(packet)

        print("[Aggregator] Finished.")