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