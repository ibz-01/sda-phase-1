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

        # Normalize keys to match JSON format expected by engine
        normalized = []
        for row in data:
            new_row = {k.strip(): v for k, v in row.items() if k is not None}
            
            # Remap CSV column names to match engine expectations
            if "continent" in new_row:
                new_row["Continent"] = new_row.pop("continent")
            if "Country Name" not in new_row and "Country NameCountry Code" in new_row:
                new_row["Country Name"] = new_row.pop("Country NameCountry Code")

            normalized.append(new_row)

        print(list(normalized[0].keys()))
        input("Press Enter to continue...")

        self.service.execute(normalized)