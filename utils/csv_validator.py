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
                constraints = col.get("constraints", {})
                # TODO: Add logic for min/max, regex, enum checks
                if value is None:
                    errors.append(f"Row {i}: Missing field '{field}'")
                    continue

                if expected_type == "int":
                    if not value.isdigit():
                        errors.append(f"Row {i}: Field '{field}' expected int but got '{value}'")
                elif expected_type == "str":
                    # Allow strings but still check for null-like values
                    if value.strip() == "":
                        errors.append(f"Row {i}: Field '{field}' is an empty string")

    return errors