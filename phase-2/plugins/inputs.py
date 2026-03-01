import json
import csv
from typing import Any
from core.contracts import PipelineService


class JsonReader:

    def __init__(self, file_path: str, service: PipelineService):
        self.file_path = file_path
        self.service = service

    def run(self) -> None:
        with open(self.file_path, "r") as file:
            data = json.load(file)

        self.service.execute(data)


class CsvReader:

    def __init__(self, file_path: str, service: PipelineService):
        self.file_path = file_path
        self.service = service

    def run(self) -> None:
        with open(self.file_path, newline="") as file:
            reader = csv.DictReader(file)
            data = list(reader)

        self.service.execute(data)