import csv
import json
import sys
from pathlib import Path
from typing import Callable

import pytest
from testforge.cli.__main__ import main as cli_main


@pytest.fixture
def run_cli(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture):
    """Helper to run the CLI and return exit code, stdout, stderr.

    Args:
        monkeypatch: pytest fixture to modify system state.
        capsys: pytest fixture to capture stdout/stderr.

    Returns:
        Callable: A function that takes command_args and returns
            (exit_code, stdout, stderr).
    """

    def _run_cli(command_args: list[str]) -> tuple[int, str, str]:
        monkeypatch.setattr(sys, "argv", ["testforge"] + command_args)
        with pytest.raises(SystemExit) as excinfo:
            cli_main()

        stdout, stderr = capsys.readouterr()
        return excinfo.value.code, stdout, stderr

    return _run_cli


def test_help_output(run_cli: Callable[[list[str]], tuple[int, str, str]]):
    """Tests the help output of the main CLI."""
    code, out, err = run_cli(["--help"])
    assert code == 0
    assert "usage:" in out.lower()


def test_version_flag(run_cli: Callable[[list[str]], tuple[int, str, str]]):
    """Tests the --version flag of the main CLI."""
    code, out, err = run_cli(["--version"])
    assert code == 0
    assert "0.1.0" in out


def test_missing_csv_file(run_cli: Callable[[list[str]], tuple[int, str, str]]):
    """Tests the CLI's behavior when the CSV file is missing."""
    code, out, err = run_cli(["validate", "missing.csv"])
    assert code != 0
    assert "CSV file not found" in out


def test_valid_csv_validation(
    tmp_path: Path, run_cli: Callable[[list[str]], tuple[int, str, str]]
):
    """Tests successful CSV validation via the CLI.

    Args:
        tmp_path (Path): pytest fixture for a temporary directory.
        run_cli: Custom fixture to run CLI commands.
    """
    csv_path = tmp_path / "good.csv"
    schema_path = tmp_path / "schema.json"

    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "email"])
        writer.writerow(["123", "test@example.com"])

    schema = {
        "columns": [{"name": "id", "type": "int"}, {"name": "email", "type": "str"}]
    }
    schema_path.write_text(json.dumps(schema, indent=2))

    code, out, err = run_cli(["validate", str(csv_path), "--schema", str(schema_path)])
    assert "CSV is valid!" in out


def test_invalid_csv(
    tmp_path: Path, run_cli: Callable[[list[str]], tuple[int, str, str]]
):
    """Tests CSV validation with an invalid CSV file.

    Args:
        tmp_path (Path): pytest fixture for a temporary directory.
        run_cli: Custom fixture to run CLI commands.
    """
    csv_path = tmp_path / "bad.csv"
    schema_path = tmp_path / "schema.json"

    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id"])
        writer.writerow(["abc"])  # not int

    schema = {
        "columns": [{"name": "id", "type": "int"}, {"name": "email", "type": "str"}]
    }
    schema_path.write_text(json.dumps(schema, indent=2))

    code, out, err = run_cli(["validate", str(csv_path), "--schema", str(schema_path)])

    assert code == 1, (
        f"Expected CLI to fail due to invalid CSV, but got exit code "
        f"{code}\nstdout:\n{out}\nstderr:\n{err}"
    )

    log_path = None
    for line in out.splitlines():
        if "Report written to:" in line:
            log_path = line.split("Report written to:")[-1].strip()
            break

    assert log_path, "Log path not found in CLI output"
    log_file = Path(log_path)
    assert log_file.exists(), f"Expected log file not found at: {log_file}"
    log_content = log_file.read_text()

    assert "Missing field 'email'" in log_content or "Header mismatch" in log_content


def test_missing_csv_and_schema_triggers_exit(
    tmp_path: Path, run_cli: Callable[[list[str]], tuple[int, str, str]]
):
    """Tests that the CLI exits with an error if both CSV and schema files are missing.

    Args:
        tmp_path (Path): pytest fixture for a temporary directory.
        run_cli: Custom fixture to run CLI commands.
    """
    code, out, err = run_cli(
        [
            "validate",
            str(tmp_path / "nope.csv"),
            "--schema",
            str(tmp_path / "nope.json"),
        ]
    )
    assert code != 0
    assert "CSV file not found" in out


def test_markdown_and_html_report(
    tmp_path: Path, run_cli: Callable[[list[str]], tuple[int, str, str]]
):
    """Tests the generation of Markdown and HTML reports.

    Args:
        tmp_path (Path): pytest fixture for a temporary directory.
        run_cli: Custom fixture to run CLI commands.
    """
    csv_path = tmp_path / "data.csv"
    schema_path = tmp_path / "schema.json"

    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["name"])
        writer.writerow(["Bob"])

    schema = {"columns": [{"name": "name", "type": "string"}]}
    schema_path.write_text(json.dumps(schema))

    code, out, err = run_cli(
        [
            "validate",
            str(csv_path),
            "--schema",
            str(schema_path),
            "--markdown",
            "--html",
        ]
    )

    assert code == 0
    assert "Markdown report saved to:" in out
    assert "HTML report saved to:" in out
