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
        headers = reader.fieldnames  # Moved up before reading rows
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

def cli():
    parser = argparse.ArgumentParser(
        description="📄 Infer a JSON schema from a sample CSV file."
    )
    parser.add_argument(
        "csv_file",
        type=Path,
        help="Path to the CSV file to infer schema from."
    )
    parser.add_argument(
        "output_file",
        type=Path,
        help="Path to save the generated schema JSON."
    )
    parser.add_argument(
        "--rows",
        type=int,
        default=10,
        help="Number of rows to sample (default: 10)."
    )
    args = parser.parse_args()

    if not args.csv_file.exists():
        print(f"❌ CSV file not found: {args.csv_file}")
        return

    try:
        schema = infer_schema(args.csv_file, args.rows)
    except Exception as e:
        print(f"❌ Failed to infer schema: {e}")
        return

    with open(args.output_file, "w") as f:
        json.dump(schema, f, indent=4)

    print(f"🧬 Schema generated and saved to: {args.output_file}")