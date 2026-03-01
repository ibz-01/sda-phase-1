from typing import List, Any
from functools import reduce
from .contracts import DataSink, PipelineService


class TransformationEngine(PipelineService):

    def __init__(self, sink: DataSink, config: dict):
        self.sink = sink
        self.config = config

    def execute(self, raw_data: List[Any]) -> None:

        continent = self.config["continent"]
        start_year = str(self.config["start_year"])
        end_year = str(self.config["end_year"])

        # Step 1: Filter by continent
        filtered_by_continent = list(
            filter(lambda record: record.get("Continent") == continent, raw_data)
        )