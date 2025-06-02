import argparse
import sys
from datetime import datetime

from testforge.core.report import generate_markdown_report, write_validation_report
from testforge.core.validator import validate_csv
from testforge.version import __version__

VERSION = __version__


def run_validate_cli(args: argparse.Namespace) -> None:
    """Runs the CSV validation process based on command-line arguments.

    This function orchestrates the validation of a CSV file against a JSON schema.
    It handles file checks, calls the core validation logic, and generates
    output reports in various formats (log, Markdown, HTML). The program
    will exit with a status code of 1 if validation errors are found and 0
    otherwise.

    Args:
        args: An `argparse.Namespace` object containing the parsed command-line
            arguments. It is expected to have the following attributes:
            - `csv_file`: The path to the CSV file to be validated.
            - `schema`: The path to the JSON schema file.
            - `output`: The directory where output reports will be saved.
            - `markdown`: A boolean flag to enable Markdown report generation.
            - `html`: A boolean flag to enable HTML report generation.
    """
    csv_file = args.csv_file
    schema_file = args.schema
    output_dir = args.output

    if not csv_file.exists():
        print(f"CSV file not found: {csv_file}")
        sys.exit(1)
    if not schema_file.exists():
        print(f"Schema file not found: {schema_file}")
        sys.exit(1)

    print(f"Validating '{csv_file}' using schema '{schema_file}'...")
    errors = validate_csv(csv_file, schema_file)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"validation_{timestamp}.log"

    write_validation_report(output_file, errors)
    print(f"Report written to: {output_file}")

    if args.markdown:
        md_str = generate_markdown_report(errors)
        md_path = output_file.with_suffix(".md")
        with open(md_path, "w") as f:
            f.write(md_str)
        print(f"Markdown report saved to: {md_path}")

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
        print(f"HTML report saved to: {html_path}")

    if errors:
        print(f"Found {len(errors)} error(s). See report: {output_file}")
        sys.exit(1)
    else:
        print("CSV is valid!")
        sys.exit(0)
