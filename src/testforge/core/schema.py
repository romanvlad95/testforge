import argparse
import csv
import json
from pathlib import Path
from typing import Any


def infer_type(value: str) -> str:
    """Infers the data type of a string value.

    The function checks if the value can be an integer, float, or email.
    If none of these match, it defaults to a string.

    Args:
        value: The string value to analyze.

    Returns:
        The inferred data type as a string (e.g., "int", "float", "email", "string").
    """
    try:
        int(value)
        return "int"
    except ValueError:
        pass
    try:
        float(value)
        return "float"
    except ValueError:
        pass
    if "@" in value:
        return "email"
    return "string"


def infer_schema(csv_path: Path, sample_size: int = 10) -> list[dict[str, Any]]:
    """Infers a JSON schema from a CSV file.

    It samples a specified number of rows from the CSV to determine the
    data type for each column.

    Args:
        csv_path: The path to the CSV file.
        sample_size: The number of rows to sample for type inference.

    Returns:
        A list of dictionaries, where each dictionary represents the schema
        for a column (e.g., `{"name": "column_name", "type": "int"}`).

    Raises:
        ValueError: If the CSV file does not contain a header row.
    """
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        if not headers:
            raise ValueError("CSV has no headers.")
        sample_rows = [row for _, row in zip(range(sample_size), reader)]

    schema = []
    for header in headers:
        sample_values = [row[header] for row in sample_rows if row[header].strip()]
        if not sample_values:
            col_type = "string"
        else:
            types = [infer_type(v) for v in sample_values]
            col_type = max(set(types), key=types.count)
        schema.append({"name": header, "type": col_type})

    return schema


def run_schema_cli(args: argparse.Namespace) -> None:
    """Command-line interface for inferring a JSON schema from a CSV file.

    This function handles file I/O and calls the core schema inference logic.
    The resulting schema is written to a specified output file.

    Args:
        args: An `argparse.Namespace` object with the following attributes:
            - `csv_file`: Path to the input CSV file.
            - `output_file`: Path to save the generated schema.
            - `rows`: The number of rows to sample for inference.
    """
    if not args.csv_file.exists():
        print(f"CSV file not found: {args.csv_file}")
        return

    try:
        schema = infer_schema(args.csv_file, args.rows)
    except Exception as e:
        print(f"Failed to infer schema: {e}")
        return

    with open(args.output_file, "w") as f:
        json.dump(schema, f, indent=4)

    print(f"Schema generated and saved to: {args.output_file}")
