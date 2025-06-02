from pathlib import Path

from colorama import Fore, init

init(autoreset=True)

LOG_DIR = Path.cwd() / "reports" / "validation_logs"


def write_validation_report(output_file: Path, errors: list[str]) -> None:
    """Writes a validation report to a file.

    The report includes a header and a list of all validation errors. If no
    errors are present, it indicates that no issues were found.

    Args:
        output_file: The path to the output log file.
        errors: A list of validation error messages.
    """
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w") as f:
        f.write("Validation Report\n")
        f.write("=" * 40 + "\n\n")

        if errors:
            for err in errors:
                f.write(f"{err}\n")
        else:
            f.write("No issues found.\n")
    if errors:
        print(Fore.RED + f"Found {len(errors)} error(s). See report: {output_file}")
    else:
        print(Fore.GREEN + f"No issues found. Report saved to: {output_file}")


def generate_markdown_report(errors: list[str]) -> str:
    """Generates a Markdown-formatted report from a list of errors.

    Args:
        errors: A list of validation error messages.

    Returns:
        A string containing the report in Markdown format.
    """
    md = "# Validation Report\n\n"
    if errors:
        md += "## Errors:\n"
        for e in errors:
            md += f"- {e}\n"
    else:
        md += "No errors found.\n"
    return md
