import csv
import json
from pathlib import Path


def load_schema(schema_path: str | Path) -> dict:
    with open(schema_path, "r") as f:
        return json.load(f)


def validate_csv(csv_path: str | Path, schema_path: str | Path) -> list[str]:
    schema = load_schema(schema_path)
    expected_fields = [col["name"] for col in schema.get("columns", [])]

    errors = []

    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)

        if reader.fieldnames != expected_fields:
            errors.append(f"Header mismatch: {reader.fieldnames} vs {expected_fields}")

        for i, row in enumerate(reader, start=1):
            for col in schema["columns"]:
                field = col["name"]
                expected_type = col["type"]
                value = row.get(field)

                # Check if field is missing
                if value is None:
                    errors.append(f"Row {i}: Missing field '{field}'")
                    continue

                # Type validation
                if expected_type == "int":
                    if not value.isdigit():
                        errors.append(f"Row {i}: Field '{field}' expected int but got '{value}'")
                        continue  # Don't run constraints if type is wrong
                elif expected_type == "str":
                    if value.strip() == "":
                        errors.append(f"Row {i}: Field '{field}' is an empty string")
                        continue

                # Load constraints only after passing type checks
                constraints = col.get("constraints", {})

                # Numeric range check
                if expected_type in ["int", "float"]:
                    try:
                        val = float(value)
                        if "min" in constraints and val < constraints["min"]:
                            errors.append(f"Row {i}: Field '{field}' below min {constraints['min']}")
                        if "max" in constraints and val > constraints["max"]:
                            errors.append(f"Row {i}: Field '{field}' above max {constraints['max']}")
                    except ValueError:
                        pass  # Already handled in type check

                # Regex pattern check
                if expected_type == "str" and "regex" in constraints:
                    import re
                    if not re.match(constraints["regex"], value):
                        errors.append(f"Row {i}: Field '{field}' does not match pattern")

                # Enum check (after type is valid)
                if "enum" in constraints and value not in constraints["enum"]:
                    errors.append(f"Row {i}: Field '{field}' not in allowed values: {constraints['enum']}")
    return errors