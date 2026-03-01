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
        # Step 2: Map to compute GDP sum between years
        def compute_total(record):
            years = [
                value for key, value in record.items()
                if key.isdigit() and start_year <= key <= end_year
            ]

            # convert to float safely
            numbers = list(
                map(lambda x: float(x) if x not in (None, "", "null") else 0.0, years)
            )

            total = reduce(lambda a, b: a + b, numbers, 0.0)

            return {
                "Country": record.get("Country Name", "Unknown"),
                "Total GDP": total
            }

        mapped_data = list(map(compute_total, filtered_by_continent))
        