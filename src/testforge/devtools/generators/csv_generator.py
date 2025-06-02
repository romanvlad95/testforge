import argparse
import csv
import random
import string
from pathlib import Path


def generate_row(headers: list[str]) -> list[str]:
    """Generates a single row of synthetic CSV data.

    The data generated is based on simple heuristics for common column names
    like "id", "email", "name", and "age".

    Args:
        headers: A list of column headers.

    Returns:
        A list of strings representing a single row of data.
    """
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


def generate_csv(template_path: Path, output_path: Path, rows: int) -> None:
    """Generates a CSV file with synthetic data.

    This function uses a template file to get the header row and then generates
    the specified number of data rows.

    Args:
        template_path: The path to the CSV template file, which must
            contain a header row.
        output_path: The path to write the generated CSV file to.
        rows: The number of data rows to generate.
    """
    with open(template_path, newline="") as f:
        reader = csv.reader(f)
        headers = next(reader)

    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for _ in range(rows):
            writer.writerow(generate_row(headers))

    print(f"Generated CSV at: {output_path} with {rows} rows.")


def run_generate_cli(args: argparse.Namespace) -> None:
    """Command-line interface for generating synthetic CSV data.

    This function handles file I/O and calls the core CSV generation logic.

    Args:
        args: An `argparse.Namespace` object with the following attributes:
            - `template`: Path to the input CSV template file.
            - `output`: Path to save the generated CSV file.
            - `rows`: The number of data rows to generate.
    """
    if not args.template.exists():
        print(f"Template file not found: {args.template}")
        return

    generate_csv(args.template, args.output, args.rows)
