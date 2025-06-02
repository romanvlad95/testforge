import csv
import os
import subprocess
import sys
from pathlib import Path


def run_cli_command(
    command_args: list[str], expected_return_code: int = 0
) -> tuple[int, str, str]:
    """Runs a CLI command and captures its output and exit code.

    Args:
        command_args (list[str]): A list of command-line arguments to execute.
        expected_return_code (int): The expected exit code of the command.
            Defaults to 0.

    Returns:
        tuple[int, str, str]: A tuple containing the exit code, stdout, and stderr.
    """
    try:
        full_command = [sys.executable, "-m", "testforge.cli.__main__"] + command_args
        stdout_content = subprocess.check_output(
            full_command, stderr=subprocess.PIPE, text=True, env=os.environ
        )
        return 0, stdout_content, ""
    except subprocess.CalledProcessError as e:
        print(f"Stderr: {e.stderr}")
        return e.returncode, e.stdout, e.stderr


def test_csv_generator_help():
    """Tests the help output of the CSV generator CLI."""
    code, out, err = run_cli_command(["generate", "--help"])
    assert code == 0
    assert "usage: __main__.py generate" in out


def test_csv_generator_with_rows(tmp_path: Path):
    """Tests CSV generation with a specified number of rows.

    Args:
        tmp_path (Path): pytest fixture for a temporary directory.
    """
    template = tmp_path / "template.csv"
    output = tmp_path / "out.csv"

    with open(template, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["user_id", "email", "name", "age", "misc"])

    code, out, err = run_cli_command(
        ["generate", str(template), str(output), "--rows", "5"]
    )

    assert code == 0
    assert "Generated CSV at:" in out
    assert output.exists()

    with open(output, newline="") as f:
        reader = list(csv.reader(f))

    assert reader[0] == ["user_id", "email", "name", "age", "misc"]
    assert len(reader) == 6  # header + 5 rows
    for row in reader[1:]:
        assert len(row) == 5


def test_csv_generator_missing_template():
    """Tests the CSV generator's behavior when the template file is missing."""
    code, out, err = run_cli_command(["generate", "nonexistent.csv", "output.csv"])
    assert code == 0
    assert "Template file not found" in out
