from pathlib import Path

LOG_DIR = Path("reports/validation_logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

def write_validation_report(output_file, errors):
    """
    Writes validation results to the specified log file.

    Parameters:
        output_file (Path): Full path to the output log file.
        errors (list[str]): List of validation error messages.
    """
    with open(output_file, "w") as f:
        f.write(f"Validation Report\n")
        f.write("=" * 40 + "\n\n")

        if errors:
            for err in errors:
                f.write(f"{err}\n")
        else:
            f.write("No issues found.\n")

    print(f"📄 Report written to: {output_file}")