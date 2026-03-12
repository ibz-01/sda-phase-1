# input_module.py — reads the CSV file row by row, maps column names using config,
# and sends standardized "data packets" (dicts) into the raw queue

import csv
import time
import multiprocessing
from abc import ABC, abstractmethod  # ABC = Abstract Base Class, enforces structure (DIP principle)


# abstract base class — defines the interface all input modules must follow (Dependency Inversion Principle)
class AbstractInputModule(ABC):
    @abstractmethod
    def run(self):
        pass


class InputModule(AbstractInputModule):
    """
    reads CSV rows, renames columns to internal generic names,
    casts values to correct types, and pushes packets into raw_queue
    """

    def __init__(self, config: dict, raw_queue: multiprocessing.Queue):
        # store the full config so we can read schema and path from it
        self.config = config

        # this is the shared queue we write into — Core workers read from this
        self.raw_queue = raw_queue

        # path to the CSV file, taken directly from config
        self.dataset_path = config["dataset_path"]

        # how long to wait between sending each row (controls input speed)
        self.delay = config["pipeline_dynamics"]["input_delay_seconds"]

        # schema_mapping tells us: original column name → internal name + data type
        self.columns = config["schema_mapping"]["columns"]

    def _cast_value(self, value: str, data_type: str):
        """
        converts a raw string value from CSV into the correct Python type
        based on what the config says the type should be
        """
        if data_type == "integer":
            return int(value)
        elif data_type == "float":
            return float(value)
        else:
            # default: treat as string (no conversion needed)
            return str(value)

    def _map_row(self, row: dict) -> dict:
        """
        takes one raw CSV row and converts it to a generic data packet
        using the schema mapping from config — this makes the module domain-agnostic
        """
        packet = {}
        for col in self.columns:
            # get the original column name from config (e.g. "Sensor_ID")
            source = col["source_name"]

            # get the internal name we want to use (e.g. "entity_name")
            internal = col["internal_mapping"]

            # get what type this value should be (e.g. "float")
            dtype = col["data_type"]

            # read the raw string from the CSV row and cast it to the right type
            raw_val = row[source]
            packet[internal] = self._cast_value(raw_val, dtype)

        return packet  # returns something like: {"entity_name": "Sensor_Alpha", "time_period": 1773037623, ...}

    def run(self):
        """
        main loop — opens the CSV, reads each row, maps it, and puts it in the queue.
        this method runs as its own separate process (called from main.py)
        """
        print("[InputModule] Starting to read data...")

        with open(self.dataset_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)  # reads each row as a dict with column names as keys

            for row in reader:
                # convert the raw CSV row into a standardized packet
                packet = self._map_row(row)

                # put the packet into the queue — if queue is full (backpressure), this will block automatically
                self.raw_queue.put(packet)

                # wait before reading the next row (simulates a data stream speed)
                time.sleep(self.delay)

        # after all rows are sent, put a special sentinel value to signal "no more data"
        # each core worker will receive one of these to know it should stop
        num_workers = self.config["pipeline_dynamics"]["core_parallelism"]
        for _ in range(num_workers):
            self.raw_queue.put(None)  # None = stop signal for workers

        print("[InputModule] All data sent. Sent stop signals to workers.")