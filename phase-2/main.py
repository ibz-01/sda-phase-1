import json

from core.engine import TransformationEngine
from plugins.inputs import JsonReader
from plugins.outputs import ConsoleWriter


def load_config(path: str) -> dict:
    with open(path, "r") as file:
        return json.load(file)


def main():
    config = load_config("config.json")

    output_driver = ConsoleWriter()

    # Inject BOTH sink and config into engine
    engine = TransformationEngine(output_driver, config)

    input_driver = JsonReader(config["data_path"], engine)

    input_driver.run()


if __name__ == "__main__":
    main()