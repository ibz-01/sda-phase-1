import json
import os

from core.engine import TransformationEngine
from plugins.inputs import JsonReader, CsvReader
from plugins.outputs import ConsoleWriter, GraphicsChartWriter


def load_config(path: str) -> dict:
    with open(path, "r") as file:
        return json.load(file)


# Maps each supported input type to the file extensions it accepts
VALID_EXTENSIONS = {
    "json": [".json"],
    "csv":  [".csv"],
}


def validate_config(config: dict) -> None:
    """
    Validate config.json fields:
      - data_path extension must match the declared input type.
      - year, start_year, end_year must be integers (not strings).
      - start_year must be <= end_year.
    Raises SystemExit with a descriptive message on any violation.
    """
    # ── data_path / input type check ──────────────────────────────────────
    input_type = config.get("input", "").strip().lower()
    data_path  = config.get("data_path", "").strip()

    if not input_type:
        raise SystemExit("[Config Error] 'input' field is missing or empty in config.json.")

    if input_type not in VALID_EXTENSIONS:
        supported = ", ".join(VALID_EXTENSIONS.keys())
        raise SystemExit(
            f"[Config Error] Unsupported input type '{input_type}'. "
            f"Supported types: {supported}."
        )

    if not data_path:
        raise SystemExit("[Config Error] 'data_path' field is missing or empty in config.json.")

    _, ext = os.path.splitext(data_path)
    ext = ext.lower()

    expected_exts = VALID_EXTENSIONS[input_type]

    if ext not in expected_exts:
        raise SystemExit(
            f"[Config Error] data_path extension '{ext}' does not match "
            f"input type '{input_type}' (expected: {expected_exts[0]}).\n"
            f"  data_path : {data_path}\n"
            f"  input     : {input_type}\n"
            f"Please make both fields consistent in config.json."
        )

    # ── year / start_year / end_year type check ───────────────────────────
    year_fields = ["year", "start_year", "end_year"]

    for field in year_fields:
        if field not in config:
            raise SystemExit(f"[Config Error] '{field}' field is missing in config.json.")

        value = config[field]

        if not isinstance(value, int) or isinstance(value, bool):
            raise SystemExit(
                f"[Config Error] '{field}' must be an integer, "
                f"but got {type(value).__name__}: {value!r}.\n"
                f"  Fix: use a plain number with no quotes, e.g.  \"{field}\": 2020"
            )

    if config["start_year"] > config["end_year"]:
        raise SystemExit(
            f"[Config Error] 'start_year' ({config['start_year']}) must be "
            f"less than or equal to 'end_year' ({config['end_year']})."
        )


def main():
    base_dir = os.path.dirname(__file__)
    config_path = os.path.join(base_dir, "config.json")
    config = load_config(config_path)

    # ── Validate that data_path extension matches the declared input type ──
    validate_config(config)

    # Driver Factories
    INPUT_DRIVERS = {
        "json": JsonReader,
        "csv": CsvReader
    }

    OUTPUT_DRIVERS = {
        "console": ConsoleWriter,
        "charts": GraphicsChartWriter
    }

    # Create Output dynamically
    output_type = config.get("output", "console")   
    output_driver = OUTPUT_DRIVERS[output_type]()

    # Inject output + config into engine
    engine = TransformationEngine(output_driver, config)

    # Create Input dynamically
    input_type = config.get("input", "json")
    input_class = INPUT_DRIVERS[input_type]
    input_driver = input_class(config["data_path"], engine)

    input_driver.run()


if __name__ == "__main__":
    main()