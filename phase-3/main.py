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
