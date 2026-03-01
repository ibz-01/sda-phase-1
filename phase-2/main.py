import json

from core.engine import TransformationEngine
from plugins.inputs import JsonReader
from plugins.outputs import ConsoleWriter


def load_config(path: str) -> dict:
    """
    Reads configuration file and returns dictionary.
    """
    with open(path, "r") as file:
        return json.load(file)


def main():
    # Step 1: Load configuration
    config = load_config("config.json")

    # Step 2: Create Output (DataSink)
    output_driver = ConsoleWriter()

    # Step 3: Create Core Engine and inject Output
    engine = TransformationEngine(output_driver)

    # Step 4: Create Input and inject Core Engine
    input_driver = JsonReader(config["data_path"], engine)

    # Step 5: Start pipeline
    input_driver.run()


if __name__ == "__main__":
    main()