import argparse
from pathlib import Path
from utils.csv_validator import validate_csv
from utils.report_writer import write_validation_report

def validate_batch(csv_dir: Path, schema_file: Path, output_dir: Path):
    csv_files = list(csv_dir.glob("*.csv"))
    results = []

    for csv_file in csv_files:
        errors = validate_csv(csv_file, schema_file)
        output_file = output_dir / f"{csv_file.stem}_validation.log"
        write_validation_report(output_file, errors)
        results.append((csv_file.name, len(errors)))

    return results

def cli():
    parser = argparse.ArgumentParser(
        description="📦 Validate a batch of CSV files in a folder against a single JSON schema."
    )
    parser.add_argument(
        "csv_dir",
        type=Path,
        help="Directory containing CSV files to validate."
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
        help="Directory to save validation logs (default: reports/validation_logs/)."
    )

    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    if not args.csv_dir.exists():
        print(f"❌ CSV directory not found: {args.csv_dir}")
        return
    if not args.schema.exists():
        print(f"❌ Schema file not found: {args.schema}")
        return

    print(f"📂 Validating all CSVs in: {args.csv_dir}")
    results = validate_batch(args.csv_dir, args.schema, args.output)

    print("\n🧪 Validation Summary:")
    for name, error_count in results:
        status = "✅" if error_count == 0 else f"❌ {error_count} error(s)"
        print(f"- {name}: {status}")