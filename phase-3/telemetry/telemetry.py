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
    def subscribe(self, observer: AbstractObserver):
        """
        adds an observer to the notification list.
        this is how the dashboard "registers" itself to receive telemetry updates
        """
        self._observers.append(observer)

    def _notify_all(self, telemetry_data: dict):
        """
        calls update() on every subscribed observer with the latest queue data.
        observers don't know about each other — they just react to the data
        """
        for observer in self._observers:
            observer.update(telemetry_data)

    def _poll_loop(self):
        """
        runs in a background thread — checks queue sizes every 0.5s and notifies observers
        """
        while self._running:
            try:
                # read current fill levels of each queue
                raw_size = self.raw_queue.qsize()
                inter_size = self.intermediate_queue.qsize()
                proc_size = self.processed_queue.qsize()
            except Exception:
                # qsize() can fail on some platforms (like macOS) — default to 0 if so
                raw_size = inter_size = proc_size = 0

            # package the data into a dict for observers to use
            telemetry_data = {
                "raw_queue_size": raw_size,
                "intermediate_queue_size": inter_size,
                "processed_queue_size": proc_size,
                "max_size": self.max_size
            }

            # push this data to all subscribed observers (e.g. the dashboard)
            self._notify_all(telemetry_data)

            time.sleep(0.5)  # poll every half second
    def start(self):
        """
        starts the background polling thread — non-blocking so rest of app keeps running
        """
        self._running = True
        # daemon=True means this thread auto-dies when the main program exits
        thread = threading.Thread(target=self._poll_loop, daemon=True)
        thread.start()
        print("[Telemetry] Monitoring started.")

    def stop(self):
        """stops the polling loop"""
        self._running = False
        print("[Telemetry] Monitoring stopped.")