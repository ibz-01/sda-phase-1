import json
import os

from core.engine import TransformationEngine
from plugins.inputs import JsonReader, CsvReader
from plugins.outputs import ConsoleWriter


def load_config(path: str) -> dict:
    with open(path, "r") as file:
        return json.load(file)


def main():
    base_dir = os.path.dirname(__file__)
    config_path = os.path.join(base_dir, "config.json")
    config = load_config(config_path)

    # Driver Factories
    INPUT_DRIVERS = {
        "json": JsonReader,
        "csv": CsvReader
    }

    OUTPUT_DRIVERS = {
        "console": ConsoleWriter
    }

    # Create Output dynamically
    output_driver = OUTPUT_DRIVERS[config["output_type"]]()

    # Inject output + config into engine
    engine = TransformationEngine(output_driver, config)

    # Create Input dynamically
    input_class = INPUT_DRIVERS[config["input_type"]]
    input_driver = input_class(config["data_path"], engine)

    input_driver.run()


if __name__ == "__main__":
    main()