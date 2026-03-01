from typing import List, Any
from .contracts import DataSink, PipelineService


class TransformationEngine(PipelineService):

    def __init__(self, sink: DataSink):
        self.sink = sink

    def execute(self, raw_data: List[Any]) -> None:
        """
        Entry point from Input Module.
        Applies simple filtering logic (temporary).
        """

        # Example simple transformation:
        # Only keep records that contain "country"
        processed_data = list(
            filter(lambda record: "country" in record, raw_data)
        )

        self.sink.write(processed_data)







        