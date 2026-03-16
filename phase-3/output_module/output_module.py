# output_module.py — the real-time dashboard.
# reads processed packets from the queue, draws two live line charts,
# and subscribes to PipelineTelemetry to show colored queue health bars.

import multiprocessing
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch
from abc import ABC, abstractmethod
from telemetry.telemetry import AbstractObserver  # inherit from Observer interface


# abstract base class — all output modules must implement run()
class AbstractOutputModule(ABC):
    @abstractmethod
    def run(self):
        pass


class OutputModule(AbstractOutputModule, AbstractObserver):
    """
    the real-time dashboard — both an output module and an Observer.
    it reads processed data and visualizes it while also reacting to telemetry updates.
    inheriting AbstractObserver means it has an update() method that Telemetry calls
    """

    def __init__(self, config: dict, processed_queue: multiprocessing.Queue):
        self.config = config
        self.processed_queue = processed_queue  # read final enriched packets from here

        # read chart config so dashboard knows what to display (domain-agnostic)
        self.charts_config = config["visualizations"]["data_charts"]
        self.telemetry_config = config["visualizations"]["telemetry"]

        # internal storage for chart data points
        self.x_values = []       # time axis (e.g. timestamps)
        self.y_values = []       # actual metric values
        self.avg_values = []     # computed running averages

        # latest telemetry snapshot (updated by Observer callback)
        self.telemetry_data = {
            "raw_queue_size": 0,
            "intermediate_queue_size": 0,
            "processed_queue_size": 0,
            "max_size": 1
        }

    def update(self, telemetry_data: dict):
        """
        Observer callback — called by PipelineTelemetry every 0.5 seconds.
        just stores the latest data so the next chart redraw picks it up
        """
        self.telemetry_data = telemetry_data  # update our local snapshot

    def _get_queue_color(self, current: int, maximum: int) -> str:
        """
        returns a color string based on how full the queue is:
        green = healthy, yellow = getting full, red = backpressure warning
        """
        if maximum == 0:
            return 'green'
        ratio = current / maximum
        if ratio < 0.5:
            return 'green'
        elif ratio < 0.8:
            return 'gold'
        else:
            return 'red'

    def _draw_telemetry_bar(self, ax, label: str, current: int, maximum: int):
        """
        draws a single colored progress bar for one queue on the given matplotlib axes
        """
        ax.clear()
        ax.set_xlim(0, maximum if maximum > 0 else 1)
        ax.set_ylim(0, 1)
        ax.set_yticks([])
        ax.set_title(label, fontsize=9)

        color = self._get_queue_color(current, maximum)

        # draw a filled rectangle representing current queue fill level
        bar = FancyBboxPatch((0, 0.1), current, 0.8,
                             boxstyle="round,pad=0.02",
                             linewidth=1, edgecolor='black',
                             facecolor=color)
        ax.add_patch(bar)

        # show the numbers inside the bar
        ax.text(maximum / 2, 0.5, f"{current}/{maximum}",
                ha='center', va='center', fontsize=9, fontweight='bold')

    def run(self):
        """
        main loop — reads from processed_queue, updates data lists,
        and redraws charts every time new data arrives.
        runs as its own process from main.py
        """
        print("[OutputModule] Dashboard starting...")

        # set up matplotlib figure with a grid layout
        plt.ion()  # interactive mode — allows live updates
        fig = plt.figure(figsize=(14, 9))
        fig.suptitle("Real-Time Pipeline Dashboard", fontsize=14, fontweight='bold')

        # create a grid: 2 rows of charts on top, 1 row of telemetry bars at bottom
        gs = gridspec.GridSpec(3, 3, figure=fig, height_ratios=[3, 3, 1])

        ax_values = fig.add_subplot(gs[0, :])   # top row: full width for values chart
        ax_avg = fig.add_subplot(gs[1, :])       # middle row: full width for average chart
        ax_raw = fig.add_subplot(gs[2, 0])       # bottom-left: raw queue bar
        ax_inter = fig.add_subplot(gs[2, 1])     # bottom-middle: intermediate queue bar
        ax_proc = fig.add_subplot(gs[2, 2])      # bottom-right: processed queue bar

        # read chart metadata from config (e.g. axis names, titles)
        chart_values_cfg = self.charts_config[0]   # first chart = raw values
        chart_avg_cfg = self.charts_config[1]      # second chart = running average

        while True:
            packet = self.processed_queue.get()  # block until a packet arrives

            if packet is None:
                # None means Aggregator is done — stop the dashboard
                print("[OutputModule] All data received. Closing dashboard.")
                break

            # append new data points to our lists for charting
            self.x_values.append(packet[chart_values_cfg["x_axis"]])   # e.g. time_period
            self.y_values.append(packet[chart_values_cfg["y_axis"]])   # e.g. metric_value
            self.avg_values.append(packet.get("computed_metric", 0))   # e.g. running average

            # ─── draw live values chart ───
            ax_values.clear()
            ax_values.plot(self.x_values, self.y_values, color='dodgerblue', linewidth=1.2)
            ax_values.set_title(chart_values_cfg["title"], fontsize=10)
            ax_values.set_xlabel(chart_values_cfg["x_axis"])
            ax_values.set_ylabel(chart_values_cfg["y_axis"])

            # ─── draw running average chart ───
            ax_avg.clear()
            ax_avg.plot(self.x_values, self.avg_values, color='tomato', linewidth=1.2)
            ax_avg.set_title(chart_avg_cfg["title"], fontsize=10)
            ax_avg.set_xlabel(chart_avg_cfg["x_axis"])
            ax_avg.set_ylabel(chart_avg_cfg["y_axis"])

            # ─── draw telemetry bars (using latest data from Observer callback) ───
            td = self.telemetry_data
            max_size = td["max_size"]

            if self.telemetry_config.get("show_raw_stream"):
                self._draw_telemetry_bar(ax_raw, "Raw Queue",
                                         td["raw_queue_size"], max_size)
            if self.telemetry_config.get("show_intermediate_stream"):
                self._draw_telemetry_bar(ax_inter, "Intermediate Queue",
                                         td["intermediate_queue_size"], max_size)
            if self.telemetry_config.get("show_processed_stream"):
                self._draw_telemetry_bar(ax_proc, "Processed Queue",
                                         td["processed_queue_size"], max_size)

            plt.tight_layout()
            plt.pause(0.01)  # small pause allows matplotlib to redraw the figure

        plt.ioff()
        plt.show()  # keep window open after all data is done
        print("[OutputModule] Dashboard closed.")