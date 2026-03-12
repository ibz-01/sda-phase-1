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