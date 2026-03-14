# main.py — the Central Orchestrator.
# creates all queues, instantiates all modules, wraps them in processes, and starts everything.

import json
import multiprocessing

# import all module classes — main knows about everyone but modules don't know about each other
from input_module.input_module import InputModule
from core_module.core_module import CoreWorker, Aggregator
from output_module.output_module import OutputModule
from telemetry.telemetry import PipelineTelemetry


def load_config(path: str) -> dict:
    """reads and returns the config.json file as a Python dictionary"""
    with open(path, 'r') as f:
        return json.load(f)
def main():
    print("=== Pipeline Starting ===")

    # load all settings from config file — the entire system is driven by this
    config = load_config("config.json")

    # read pipeline settings
    max_size = config["pipeline_dynamics"]["stream_queue_max_size"]
    num_workers = config["pipeline_dynamics"]["core_parallelism"]

    # ─── create the three queues that connect the modules ───
    # maxsize makes them bounded — if full, producer automatically blocks (backpressure!)
    raw_queue = multiprocessing.Queue(maxsize=max_size)           # Input → Core workers
    intermediate_queue = multiprocessing.Queue(maxsize=max_size)  # Core workers → Aggregator
    processed_queue = multiprocessing.Queue(maxsize=max_size)     # Aggregator → Output

    # ─── instantiate all module objects ───
    # each module gets the config + the queues it needs (no module knows about others)
    input_mod = InputModule(config, raw_queue)

    # create one CoreWorker per parallelism setting (e.g. 4 workers)
    core_workers = [
        CoreWorker(config, raw_queue, intermediate_queue, worker_id=i)
        for i in range(num_workers)
    ]

    # one aggregator that collects from all core workers
    aggregator = Aggregator(config, intermediate_queue, processed_queue, num_workers)

    # the dashboard that reads final output and draws charts
    output_mod = OutputModule(config, processed_queue)

    # ─── set up telemetry (Observer pattern) ───
    telemetry = PipelineTelemetry(raw_queue, intermediate_queue, processed_queue, max_size)
    # subscribe the dashboard as an observer — it will receive queue size updates
    telemetry.subscribe(output_mod)
    telemetry.start()  # starts background monitoring thread

    # ─── wrap module run() methods in separate processes ───
    # multiprocessing.Process takes a target function to run in the new process
    input_process = multiprocessing.Process(target=input_mod.run)

    # list of processes for all core workers
    worker_processes = [
        multiprocessing.Process(target=w.run)
        for w in core_workers
    ]

    aggregator_process = multiprocessing.Process(target=aggregator.run)

    # output runs in the main process (matplotlib needs to be on the main thread on some systems)
    # so we call output_mod.run() directly at the end, not in a subprocess

    # ─── start all processes ───
    print("[Main] Launching all pipeline processes...")
    input_process.start()
    for p in worker_processes:
        p.start()
    aggregator_process.start()

    # run the dashboard in the main thread (required for matplotlib GUI on most OSes)
    output_mod.run()

    # ─── wait for all background processes to finish before exiting ───
    input_process.join()
    for p in worker_processes:
        p.join()
    aggregator_process.join()

    telemetry.stop()
    print("=== Pipeline Complete ===")


# this guard is REQUIRED for multiprocessing on Windows — prevents recursive process spawning
if __name__ == "__main__":
    main()
