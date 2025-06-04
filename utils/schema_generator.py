import argparse
import csv
import json
from pathlib import Path

def infer_type(value):
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

def infer_schema(csv_path: Path, sample_size=10):
    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        sample_rows = [row for _, row in zip(range(sample_size), reader)]

    headers = reader.fieldnames
    if not headers:
        raise ValueError("CSV has no headers.")

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

def cli():
    parser = argparse.ArgumentParser(description="Infer JSON schema from a sample CSV file.")
    parser.add_argument("csv_file", type=Path, help="Path to the CSV file to infer schema from.")
    parser.add_argument("output_file", type=Path, help="Path to save the generated schema JSON.")
    parser.add_argument("--rows", type=int, default=10, help="Number of rows to sample (default: 10)")
    args = parser.parse_args()

    schema = infer_schema(args.csv_file, args.rows)
    with open(args.output_file, "w") as f:
        json.dump(schema, f, indent=4)

    print(f"🧬 Schema generated and saved to: {args.output_file}")