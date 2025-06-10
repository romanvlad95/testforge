# MIT License
# Copyright (c) 2025 Vlad
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND...

from pathlib import Path
from colorama import init, Fore
init(autoreset=True)

LOG_DIR = Path(__file__).resolve().parent.parent / "reports" / "validation_logs"
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
    if errors:
        print(Fore.RED + f"❗ Found {len(errors)} error(s). See report: {output_file}")
    else:
        print(Fore.GREEN + f"✅ No issues found. Report saved to: {output_file}")

def generate_markdown_report(errors: list[str]) -> str:
    md = "# Validation Report\n\n"
    if errors:
        md += "## Errors:\n"
        for e in errors:
            md += f"- {e}\n"
    else:
        md += "✅ No errors found.\n"
    return md

