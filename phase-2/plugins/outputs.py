from typing import List
from core.contracts import DataSink


class ConsoleWriter:
    """
    Concrete Output Implementation.
    This satisfies the DataSink Protocol.
    """

    def write(self, records: List[dict]) -> None:
        print("\n--- OUTPUT START ---\n")

        for record in records:
            print(record)

        print("\n--- OUTPUT END ---\n")