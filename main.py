import argparse
from pathlib import Path
from utils.csv_validator import validate_csv
from utils.report_writer import write_log

SCHEMA_PATH = Path("schema_definition.json")
DEFAULT_CSV_DIR = Path("test_cases/generated")

def get_latest_csv_file(directory: Path) -> Path:
    csv_files = sorted(directory.glob("*.csv"), key=lambda f: f.stat().st_mtime, reverse=True)
    return csv_files[0] if csv_files else None

def main():
    parser = argparse.ArgumentParser(description="CSV Validator Tool")
    parser.add_argument(
        "--file",
        type=str,
        default=None,
        help="Path to the CSV file to validate",
    )
    args = parser.parse_args()

    if args.file:
        csv_file = Path(args.file)
    else:
        csv_file = get_latest_csv_file(DEFAULT_CSV_DIR)

    if not csv_file or not csv_file.exists():
        print(f"❌ No valid CSV file found.")
        return

    print(f"Validating {csv_file.name}...")
    errors = validate_csv(csv_file, SCHEMA_PATH)

    if errors:
        for err in errors:
            print(f"  ❌ {err}")
    else:
        print("  ✅ No issues found.")

    write_log(errors, csv_file.name)

if __name__ == "__main__":
    main()