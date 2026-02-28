from typing import List, Any
from .contracts import DataSink, PipelineService


class TransformationEngine(PipelineService):

    def __init__(self, sink: DataSink):
        # Dependency Injection happens here
        self.sink = sink

    def execute(self, raw_data: List[Any]) -> None:
        """
        Entry point from Input Module.
        """
        # For now, just pass raw data directly to sink
        processed_data = raw_data

        self.sink.write(processed_data) 
    