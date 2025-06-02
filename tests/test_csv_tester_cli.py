import csv
import json
import os
import subprocess
import sys
from pathlib import Path


def run_csv_tester(args: list[str]) -> tuple[int, str, str]:
    """Helper to run the batch validation CLI command and capture its output.

    Args:
        args (list[str]): A list of command-line arguments to execute.

    Returns:
        tuple[int, str, str]: A tuple containing the exit code, stdout, and stderr.
    """
    try:
        stdout_content = subprocess.check_output(
            [sys.executable, "-m", "testforge.cli.__main__", "batch"] + args,
            stderr=subprocess.PIPE,
            text=True,
            env=os.environ,
        )
        return 0, stdout_content, ""
    except subprocess.CalledProcessError as e:
        print(f"Stderr: {e.stderr}")
        return e.returncode, e.stdout, e.stderr


def test_cli_missing_csv_dir(tmp_path: Path):
    """Tests the CLI's behavior when the CSV directory is missing.

    Args:
        tmp_path (Path): pytest fixture for a temporary directory.
    """
    schema = tmp_path / "schema.json"
    schema.write_text(json.dumps({"columns": [{"name": "name", "type": "string"}]}))
    code, out, _ = run_csv_tester([str(tmp_path / "missing"), "--schema", str(schema)])
    assert "CSV directory not found" in out


def test_cli_missing_schema_file(tmp_path: Path):
    """Tests the CLI's behavior when the schema file is missing.

    Args:
        tmp_path (Path): pytest fixture for a temporary directory.
    """
    csv_dir = tmp_path / "csvs"
    csv_dir.mkdir()
    code, out, _ = run_csv_tester(
        [str(csv_dir), "--schema", str(tmp_path / "ghost_schema.json")]
    )
    assert "Schema file not found" in out


def test_cli_creates_output_dir_and_logs(tmp_path: Path):
    """Tests that the CLI correctly creates output directories and log files.

    Args:
        tmp_path (Path): pytest fixture for a temporary directory.
    """
    schema_path = tmp_path / "schema.json"
    csv_dir = tmp_path / "data"
    output_dir = tmp_path / "logs"

    csv_dir.mkdir()
    schema = {"columns": [{"name": "name", "type": "string"}]}
    schema_path.write_text(json.dumps(schema))

    csv_file = csv_dir / "valid.csv"
    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["name"])
        writer.writerow(["Alice"])

    code, out, _ = run_csv_tester(
        [str(csv_dir), "--schema", str(schema_path), "--output", str(output_dir)]
    )
    assert code == 0
    assert output_dir.exists()
    log = output_dir / "valid_validation.log"
    assert log.exists()
    assert "No issues found" in log.read_text()
