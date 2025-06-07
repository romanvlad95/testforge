import csv
import json
import re
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
                constraints = col.get("constraints", {})

                # Check if the field is completely missing from the row
                if field not in row:
                    errors.append(f"Row {i}: Missing field '{field}'")
                    continue

                # Get value and normalize
                value = row.get(field, "")
                if value is None:
                    value = ""

                # Empty string check
                if expected_type == "str" and value.strip() == "":
                    errors.append(f"Row {i}: Field '{field}' is an empty string")

                # Type validation
                if expected_type == "int":
                    if not value.isdigit():
                        errors.append(f"Row {i}: Field '{field}' expected int but got '{value}'")
                        continue  # skip constraints if type is wrong

                # Min/max for numeric fields
                if expected_type in ["int", "float"]:
                    try:
                        val = float(value)
                        if "min" in constraints and val < constraints["min"]:
                            errors.append(f"Row {i}: Field '{field}' below min {constraints['min']}")
                        if "max" in constraints and val > constraints["max"]:
                            errors.append(f"Row {i}: Field '{field}' above max {constraints['max']}")
                    except ValueError:
                        pass  # Already handled above

                # Regex check
                if expected_type == "str" and "regex" in constraints:
                    if not re.match(constraints["regex"], value):
                        errors.append(f"Row {i}: Field '{field}' does not match pattern")

                # Enum check
                if "enum" in constraints and value not in constraints["enum"]:
                    errors.append(f"Row {i}: Field '{field}' not in allowed values: {constraints['enum']}")

    return errors