import argparse
from pathlib import Path

from colorama import Fore

from testforge.core.report import write_validation_report
from testforge.core.validator import validate_csv


def validate_batch(
    csv_dir: Path, schema_file: Path, output_dir: Path
) -> list[tuple[str, int]]:
    """Validates all CSV files in a directory against a schema.

    For each CSV file found, it performs validation and writes a separate
    log file to the specified output directory.

    Args:
        csv_dir: The directory containing the CSV files to validate.
        schema_file: The path to the JSON schema file.
        output_dir: The directory where validation logs will be saved.

    Returns:
        A list of tuples, where each tuple contains the name of a CSV file
        and the number of validation errors found for it.
    """
    csv_files = list(csv_dir.glob("*.csv"))
    results = []

    for csv_file in csv_files:
        errors = validate_csv(csv_file, schema_file)
        output_file = output_dir / f"{csv_file.stem}_validation.log"
        write_validation_report(output_file, errors)
        results.append((csv_file.name, len(errors)))

    return results


def run_batch_cli(args: argparse.Namespace) -> None:
    """Command-line interface for batch validating CSV files.

    This function handles file I/O and calls the core batch validation logic,
    then prints a summary of the results to the console.

    Args:
        args: An `argparse.Namespace` object with the following attributes:
            - `csv_dir`: The directory containing CSV files.
            - `schema`: The path to the JSON schema file.
            - `output`: The directory to save validation reports.
    """
    args.output.mkdir(parents=True, exist_ok=True)

    if not args.csv_dir.exists():
        print(Fore.RED + f"CSV directory not found: {args.csv_dir}")
        return
    if not args.schema.exists():
        print(Fore.RED + f"Schema file not found: {args.schema}")
        return

    print(f"Validating all CSVs in: {args.csv_dir}")
    results = validate_batch(args.csv_dir, args.schema, args.output)

    print("\nValidation Summary:")
    for name, error_count in results:
        if error_count == 0:
            status = Fore.GREEN + "0 errors"
        else:
            status = Fore.RED + f"{error_count} error(s)"
        print(f"- {name}: {status}")
