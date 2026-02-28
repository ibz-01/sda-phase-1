from typing import Protocol, List, Any, runtime_checkable


@runtime_checkable
class DataSink(Protocol):
    """
    Outbound Abstraction:
    The Core will call this to send processed data outward.
    Any Output module must implement this method.
    """

    def write(self, records: List[dict]) -> None:
        ...


@runtime_checkable
class PipelineService(Protocol):
    """
    Inbound Abstraction:
    The Input module will call this to send raw data into the Core.
    """

    def execute(self, raw_data: List[Any]) -> None:
        ...