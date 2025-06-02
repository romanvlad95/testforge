import csv
import json
import re
from collections.abc import Sequence
from pathlib import Path
from typing import Any


def load_schema(schema_path: str | Path) -> dict[str, Any]:
    """Loads a JSON schema from a file.

    Args:
        schema_path: The file path to the JSON schema.

    Returns:
        A dictionary representing the loaded JSON schema.
    """
    with open(schema_path, "r") as f:
        return json.load(f)  # type: ignore[no-any-return]


def validate_field(
    value: str, expected_type: str, row_num: int, field_name: str
) -> list[str]:
    """Validates the data type of a single field.

    Args:
        value: The value of the field to validate.
        expected_type: The expected data type (e.g., "int", "str").
        row_num: The row number where the field appears.
        field_name: The name of the field.

    Returns:
        A list of error messages. An empty list means the field is valid.
    """
    errors = []

    if expected_type == "str" and value.strip() == "":
        errors.append(f"Row {row_num}: Field '{field_name}' is an empty string")

    if expected_type == "int" and not value.isdigit():
        errors.append(
            f"Row {row_num}: Field '{field_name}' expected int but got '{value}'"
        )

    return errors


def parse_constraints(
    value: str,
    constraints: dict[str, Any],
    expected_type: str,
    row_num: int,
    field_name: str,
) -> list[str]:
    """Validates a field's value against a set of constraints.

    This function checks for various constraints such as minimum and maximum
    values, regular expression patterns, and enumerated values.

    Args:
        value: The field's value to validate.
        constraints: A dictionary of constraints to apply.
        expected_type: The expected data type of the field.
        row_num: The row number where the field appears.
        field_name: The name of the field.

    Returns:
        A list of error messages. An empty list means the constraints are met.
    """
    errors = []

    try:
        val = float(value) if expected_type in ["int", "float"] else value
    except ValueError:
        return []

    if "min" in constraints and val < constraints["min"]:
        errors.append(
            f"Row {row_num}: Field '{field_name}' below min " f"{constraints['min']}"
        )

    if "max" in constraints and val > constraints["max"]:
        errors.append(
            f"Row {row_num}: Field '{field_name}' above max " f"{constraints['max']}"
        )

    if "regex" in constraints and expected_type == "str":
        if not re.match(constraints["regex"], value):
            errors.append(f"Row {row_num}: Field '{field_name}' does not match pattern")

    if "enum" in constraints and value not in constraints["enum"]:
        errors.append(
            f"Row {row_num}: Field '{field_name}' not in allowed values: "
            f"{constraints['enum']}"
        )

    return errors


def validate_header(
    reader_fields: Sequence[str] | None, expected_fields: list[str]
) -> list[str]:
    """Validates the CSV header against the expected schema fields.

    Args:
        reader_fields: The list of field names from the CSV header.
        expected_fields: The list of expected field names from the schema.

    Returns:
        A list of error messages. An empty list means the header is valid.
    """
    errors = []

    if reader_fields is None:
        errors.append("Header mismatch: None vs expected headers")
        for field in expected_fields:
            errors.append(f"Missing field '{field}'")
        return errors

    if reader_fields != expected_fields:
        errors.append(f"Header mismatch: {reader_fields} vs {expected_fields}")

        missing = [f for f in expected_fields if f not in reader_fields]
        extra = [f for f in reader_fields if f not in expected_fields]

        for f in missing:
            errors.append(f"Missing field '{f}'")
        for f in extra:
            errors.append(f"Unexpected extra field '{f}'")

    return errors


def validate_csv(csv_path: str | Path, schema_path: str | Path) -> list[str]:
    """Validates a CSV file against a JSON schema.

    This function reads a CSV file and a schema, then validates the CSV's
    header and each row against the schema's definitions and constraints.

    Args:
        csv_path: The path to the CSV file to validate.
        schema_path: The path to the JSON schema file.

    Returns:
        A list of all validation error messages. An empty list indicates that
        the CSV is fully valid.
    """
    schema = load_schema(schema_path)
    columns = schema.get("columns")
    errors = []

    if columns is None:
        return ["Schema is missing 'columns' key."]

    expected_fields = [col["name"] for col in columns]

    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        errors += validate_header(reader.fieldnames, expected_fields)

        for i, row in enumerate(reader, start=1):
            for col in columns:
                field = col["name"]
                expected_type = col["type"]
                constraints = col.get("constraints", {})
                value = row.get(field, "") or ""

                errors += validate_field(value, expected_type, i, field)
                errors += parse_constraints(value, constraints, expected_type, i, field)

    return errors
