# MIT License
# Copyright (c) 2025 Vlad

import argparse
import sys
from datetime import datetime
from pathlib import Path

from utils.csv_validator import validate_csv
from utils.report_writer import write_validation_report
from utils.report_writer import generate_markdown_report

VERSION = "1.0.0"

def parse_args():
    parser = argparse.ArgumentParser(
        description="🧪 Validate a CSV file against a JSON schema with support for constraints, Markdown, and HTML reporting."
    )
    parser.add_argument("csv_file", type=Path, help="Path to the CSV file to validate.")
    parser.add_argument("--schema", type=Path, default=Path(__file__).resolve().parent.parent / "schema_definition.json",
                        help="Path to the schema JSON file (default: schema_definition.json).")
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent.parent / "reports" / "validation_logs",
                        help="Directory to save the validation log (default: reports/validation_logs/).")
    parser.add_argument("--markdown", action="store_true", help="Also generate a Markdown (.md) version of the validation report.")
    parser.add_argument("--html", action="store_true", help="Also generate an HTML (.html) version of the validation report.")
    parser.add_argument("--fail-fast", action="store_true", help="(Placeholder) Stop at first validation error (not yet implemented).")
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    return parser.parse_args()

def main():
    args = parse_args()

    csv_file = args.csv_file
    schema_file = args.schema
    output_dir = args.output

    if not csv_file.exists():
        print(f"❌ CSV file not found: {csv_file}")
        sys.exit(1)
    if not schema_file.exists():
        print(f"❌ Schema file not found: {schema_file}")
        sys.exit(1)

    print(f"🔍 Validating '{csv_file}' using schema '{schema_file}'...")
    errors = validate_csv(csv_file, schema_file)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"validation_{timestamp}.log"

    write_validation_report(output_file, errors)
    print(f"✅ Report written to: {output_file}")  # <-- test relies on this line

    if args.markdown:
        md_str = generate_markdown_report(errors)
        md_path = output_file.with_suffix(".md")
        with open(md_path, "w") as f:
            f.write(md_str)
        print(f"📝 Markdown report saved to: {md_path}")

    if args.html:
        md_str = generate_markdown_report(errors)
        html_path = output_file.with_suffix(".html")
        html_str = (
            "<html><head><title>Validation Report</title></head><body>\n"
            + md_str.replace("\n", "<br>").replace("## ", "<h2>").replace("# ", "<h1>")
            + "\n</body></html>"
        )
        with open(html_path, "w") as f:
            f.write(html_str)
        print(f"🌐 HTML report saved to: {html_path}")

    if errors:
        print(f"❗ Found {len(errors)} error(s).")
        sys.exit(1)
    else:
        print("✅ CSV is valid!")
        sys.exit(0)

if __name__ == "__main__":
    main()