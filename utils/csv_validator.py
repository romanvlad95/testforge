import csv
import json
from pathlib import Path

def load_schema(schema_path):
    with open(schema_path, "r") as f:
        return json.load(f)

def validate_csv(csv_path, schema_path):
    schema = load_schema(schema_path)
    columns = schema["columns"]
    expected_fields = [col["name"] for col in columns]

    errors = []

    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != expected_fields:
            errors.append(f"Header mismatch: {reader.fieldnames} vs {expected_fields}")

        for i, row in enumerate(reader, start=1):
            for col in columns:
                field = col["name"]
                expected_type = col["type"]
                value = row[field]

                if expected_type == "int":
                    if not value.isdigit():
                        errors.append(f"Row {i}: Field '{field}' expected int but got '{value}'")
                elif expected_type == "str":
                    if not isinstance(value, str):
                        errors.append(f"Row {i}: Field '{field}' expected str but got '{value}'")

    return errors