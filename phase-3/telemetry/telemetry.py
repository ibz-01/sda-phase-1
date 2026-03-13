# telemetry.py — implements the Observer Design Pattern for monitoring pipeline health.
# PipelineTelemetry is the Subject: it watches queue sizes and notifies all subscribed observers.
# Any dashboard component can subscribe to receive updates.

import multiprocessing
import time
import threading
from abc import ABC, abstractmethod  # used to define the Observer interface (DIP)


# abstract observer — every observer (e.g. dashboard) must implement this method
class AbstractObserver(ABC):
    @abstractmethod
    def update(self, telemetry_data: dict):
        """called by the Subject (PipelineTelemetry) whenever queue stats change"""
        pass


class PipelineTelemetry:
    """
    the Subject in the Observer pattern.
    polls queue sizes every 0.5 seconds and notifies all subscribed observers.
    runs on its own background thread so it doesn't block anything else.
    """

    def __init__(self, raw_queue: multiprocessing.Queue,
                 intermediate_queue: multiprocessing.Queue,
                 processed_queue: multiprocessing.Queue,
                 max_size: int):
        # store references to all three queues so we can read their sizes
        self.raw_queue = raw_queue
        self.intermediate_queue = intermediate_queue
        self.processed_queue = processed_queue
        self.max_size = max_size  # the max capacity of each queue (for % calculation)

        # list of observers — anyone who calls subscribe() gets added here
        self._observers = []

        # flag to stop the polling loop cleanly
        self._running = False