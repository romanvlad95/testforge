# MIT License
# Copyright (c) 2025 Vlad
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND...

import csv
import json
import re
from pathlib import Path


def load_schema(schema_path: str | Path) -> dict:
    with open(schema_path, "r") as f:
        return json.load(f)


def validate_csv(csv_path: str | Path, schema_path: str | Path) -> list[str]:
    schema = load_schema(schema_path)
    columns = schema.get("columns")

    errors = []

    if columns is None:
        errors.append("Schema is missing 'columns' key.")
        return errors

    expected_fields = [col["name"] for col in columns]

    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)

        # === Handle empty file or missing header ===
        if reader.fieldnames is None:
            errors.append("Header mismatch: None vs expected headers")
            for field in expected_fields:
                errors.append(f"Missing field '{field}'")
            return errors

        # === Check for header mismatch ===
        if reader.fieldnames != expected_fields:
            errors.append(f"Header mismatch: {reader.fieldnames} vs {expected_fields}")

            missing = [field for field in expected_fields if field not in reader.fieldnames]
            extra = [field for field in reader.fieldnames if field not in expected_fields]

            for field in missing:
                errors.append(f"Missing field '{field}'")
            for field in extra:
                errors.append(f"Unexpected extra field '{field}'")

        # === Row-wise validation ===
        for i, row in enumerate(reader, start=1):
            for col in columns:
                field = col["name"]
                expected_type = col["type"]
                constraints = col.get("constraints", {})

                value = row.get(field, "")
                if value is None:
                    value = ""

                if expected_type == "str" and value.strip() == "":
                    errors.append(f"Row {i}: Field '{field}' is an empty string")

                if expected_type == "int":
                    if not value.isdigit():
                        errors.append(f"Row {i}: Field '{field}' expected int but got '{value}'")
                        continue

                if expected_type in ["int", "float"]:
                    try:
                        val = float(value)
                        if "min" in constraints and val < constraints["min"]:
                            errors.append(f"Row {i}: Field '{field}' below min {constraints['min']}")
                        if "max" in constraints and val > constraints["max"]:
                            errors.append(f"Row {i}: Field '{field}' above max {constraints['max']}")
                    except ValueError:
                        pass

                if expected_type == "str" and "regex" in constraints:
                    if not re.match(constraints["regex"], value):
                        errors.append(f"Row {i}: Field '{field}' does not match pattern")

                if "enum" in constraints and value not in constraints["enum"]:
                    errors.append(f"Row {i}: Field '{field}' not in allowed values: {constraints['enum']}")

    return errors