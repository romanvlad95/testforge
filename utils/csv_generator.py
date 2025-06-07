import argparse
import csv
from pathlib import Path
import random
import string

def generate_row(headers):
    row = []
    for header in headers:
        if "id" in header.lower():
            row.append(str(random.randint(1000, 9999)))
        elif "email" in header.lower():
            row.append(f"user{random.randint(1, 100)}@example.com")
        elif "name" in header.lower():
            row.append("".join(random.choices(string.ascii_letters, k=6)))
        elif "age" in header.lower():
            row.append(str(random.randint(18, 99)))
        else:
            row.append("dummy")
    return row

def generate_csv(template_path: Path, output_path: Path, rows: int):
    with open(template_path, newline='') as f:
        reader = csv.reader(f)
        headers = next(reader)

    with open(output_path, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for _ in range(rows):
            writer.writerow(generate_row(headers))

    print(f"✅ Generated CSV at: {output_path} with {rows} rows.")

def cli():
    parser = argparse.ArgumentParser(
        description="🛠 Generate dummy CSV data from a template file with headers."
    )
    parser.add_argument(
        "template",
        type=Path,
        help="Path to the CSV template with headers."
    )
    parser.add_argument(
        "output",
        type=Path,
        help="Output path for the generated CSV."
    )
    parser.add_argument(
        "--rows",
        type=int,
        default=10,
        help="Number of rows to generate (default: 10)."
    )
    args = parser.parse_args()

    if not args.template.exists():
        print(f"❌ Template file not found: {args.template}")
        return

    generate_csv(args.template, args.output, args.rows)