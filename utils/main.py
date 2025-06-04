import argparse
from datetime import datetime
from pathlib import Path

from utils.csv_validator import validate_csv
from utils.report_writer import write_validation_report

VERSION = "1.0.0"

def parse_args():
    parser = argparse.ArgumentParser(
        description="🧪 CSV Validator: Validate CSV files against a JSON schema."
    )
    parser.add_argument(
        "csv_file",
        type=Path,
        help="Path to the CSV file to validate."
    )
    parser.add_argument(
        "--schema",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "schema_definition.json",
        help="Path to the schema JSON file (default: schema_definition.json)."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "reports" / "validation_logs",
        help="Directory to save the validation log (default: reports/validation_logs)."
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {VERSION}"
    )
    return parser.parse_args()

def main():
    args = parse_args()

    csv_file = args.csv_file
    schema_file = args.schema
    output_dir = args.output

    if not csv_file.exists():
        print(f"❌ CSV file not found: {csv_file}")
        return
    if not schema_file.exists():
        print(f"❌ Schema file not found: {schema_file}")
        return

    print(f"🔍 Validating '{csv_file}' using schema '{schema_file}'...")
    errors = validate_csv(csv_file, schema_file)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"validation_{timestamp}.log"

    write_validation_report(output_file, errors)

    if errors:
        print(f"❗ Found {len(errors)} error(s). See report: {output_file}")
    else:
        print(f"✅ CSV is valid! Report saved to: {output_file}")

if __name__ == "__main__":
    main()