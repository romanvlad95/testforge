import argparse
import sys
from pathlib import Path

from testforge.cli.main import run_validate_cli
from testforge.cli.splash import get_splash_screen
from testforge.core.schema import run_schema_cli
from testforge.devtools.batch_tests.batch_runner import run_batch_cli
from testforge.devtools.generators.csv_generator import run_generate_cli
from testforge.version import __version__


def main() -> None:
    """Main entry point for the TestForge command-line interface.

    This function is responsible for parsing command-line arguments and dispatching
    them to the appropriate handler function. It sets up the main parser and
    subparsers for all available commands.
    """
    print(get_splash_screen())
    if "--version" in sys.argv:
        print(f"TestForge {__version__}")
        sys.exit(0)

    parser = argparse.ArgumentParser(
        description="TestForge: A powerful CLI toolkit for CSV testing and validation.",
        add_help=True,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    validate_parser = subparsers.add_parser(
        "validate", help="Validate a CSV file against a JSON schema."
    )
    validate_parser.add_argument(
        "csv_file",
        type=Path,
        help="Path to the CSV file to validate.",
    )
    validate_parser.add_argument(
        "--schema",
        type=Path,
        default=Path(__file__).resolve().parent.parent.parent
        / "examples"
        / "schema_definition.json",
        help="Path to the schema JSON file (default: examples/schema_definition.json).",
    )
    validate_parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent.parent.parent
        / "reports"
        / "validation_logs",
        help="Directory to save the validation log (default: "
        "reports/validation_logs/).",
    )
    validate_parser.add_argument(
        "--markdown",
        action="store_true",
        help="Also generate a Markdown (.md) version of the validation report.",
    )
    validate_parser.add_argument(
        "--html",
        action="store_true",
        help="Also generate an HTML (.html) version of the validation report.",
    )
    validate_parser.add_argument(
        "--fail-fast",
        action="store_true",
        help="(Placeholder) Stop at first validation error (not yet implemented).",
    )
    validate_parser.set_defaults(func=run_validate_cli)

    generate_parser = subparsers.add_parser(
        "generate", help="Generate dummy CSV data from a template file."
    )
    generate_parser.add_argument(
        "template",
        type=Path,
        help="Path to the CSV template with headers.",
    )
    generate_parser.add_argument(
        "output",
        type=Path,
        help="Output path for the generated CSV.",
    )
    generate_parser.add_argument(
        "--rows",
        type=int,
        default=10,
        help="Number of rows to generate (default: 10).",
    )
    generate_parser.set_defaults(func=run_generate_cli)

    schema_parser = subparsers.add_parser(
        "schema", help="Infer a JSON schema from a sample CSV file."
    )
    schema_parser.add_argument(
        "csv_file",
        type=Path,
        help="Path to the CSV file to infer schema from.",
    )
    schema_parser.add_argument(
        "output_file",
        type=Path,
        help="Path to save the generated schema JSON.",
    )
    schema_parser.add_argument(
        "--rows",
        type=int,
        default=10,
        help="Number of rows to sample (default: 10).",
    )
    schema_parser.set_defaults(func=run_schema_cli)

    batch_parser = subparsers.add_parser(
        "batch", help="Validate a batch of CSV files in a folder."
    )
    batch_parser.add_argument(
        "csv_dir",
        type=Path,
        help="Directory containing CSV files to validate.",
    )
    batch_parser.add_argument(
        "--schema",
        type=Path,
        default=Path(__file__).resolve().parent.parent.parent
        / "examples"
        / "schema_definition.json",
        help="Path to the schema JSON file (default: examples/schema_definition.json).",
    )
    batch_parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent.parent.parent
        / "reports"
        / "validation_logs",
        help="Directory to save validation logs (default: reports/validation_logs/).",
    )
    batch_parser.set_defaults(func=run_batch_cli)

    args = parser.parse_args(sys.argv[1:])

    if hasattr(args, "func"):
        args.func(args)
    else:
        # This part may now be redundant due to the help handling above,
        # but it's good practice to keep it as a fallback.
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
