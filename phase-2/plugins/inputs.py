from typing import List, Any
from core.contracts import PipelineService


class JsonReader:
    """
    Concrete Input Implementation.
    Reads JSON file and sends raw data to Core.
    """

    def __init__(self, file_path: str, service: PipelineService):
        self.file_path = file_path
        self.service = service
    def run(self) -> None:
        """
        Entry point to start reading data.
        """

        with open(self.file_path, "r") as file:
            data = json.load(file)

        # Send raw data to core
        self.service.execute(data)






