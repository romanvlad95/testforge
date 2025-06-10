import subprocess
from pathlib import Path
import json
import csv

def run_cli(args):
    """Helper to run the CLI and return exit code, stdout, stderr."""
    result = subprocess.run(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return result.returncode, result.stdout, result.stderr

def test_help_output():
    code, out, err = run_cli(["csv-validator", "--help"])
    assert code == 0
    assert "usage:" in out.lower()

def test_version_flag():
    code, out, err = run_cli(["csv-validator", "--version"])
    assert code == 0
    assert "1.0.0" in out  # Adjust if version changes

def test_missing_csv_file():
    code, out, err = run_cli(["csv-validator", "missing.csv"])
    assert code != 0
    assert "CSV file not found" in out

def test_valid_csv_validation(tmp_path):
    # Setup schema + CSV
    csv_path = tmp_path / "good.csv"
    schema_path = tmp_path / "schema.json"

    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "email"])
        writer.writerow(["123", "test@example.com"])

    schema = {
        "columns": [
            {"name": "id", "type": "int"},
            {"name": "email", "type": "str"}
        ]
    }
    schema_path.write_text(json.dumps(schema, indent=2))

    code, out, err = run_cli([
        "csv-validator",
        str(csv_path),
        "--schema", str(schema_path)
    ])

    assert code == 0
    assert "✅ CSV is valid!" in out

def test_invalid_csv(tmp_path):
    # CSV missing a required column
    csv_path = tmp_path / "bad.csv"
    schema_path = tmp_path / "schema.json"

    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id"])
        writer.writerow(["abc"])  # not int

    schema = {
        "columns": [
            {"name": "id", "type": "int"},
            {"name": "email", "type": "str"}
        ]
    }
    schema_path.write_text(json.dumps(schema, indent=2))

    code, out, err = run_cli([
        "csv-validator",
        str(csv_path),
        "--schema", str(schema_path)
    ])

    assert code == 1, f"Expected CLI to fail due to invalid CSV, but got exit code {code}\nstdout:\n{out}\nstderr:\n{err}"

    # Strip emoji and get proper file path
    log_path = None
    for line in out.splitlines():
        if "Report written to:" in line:
            log_path = line.split("Report written to:")[-1].strip()
            break

    assert log_path, "Log path not found in CLI output"
    log_file = Path(log_path)
    assert log_file.exists(), f"Expected log file not found at: {log_path}"
    log_content = log_file.read_text()

    assert "Missing field 'email'" in log_content or "Header mismatch" in log_content

def test_missing_csv_and_schema_triggers_exit(tmp_path):
    result = subprocess.run(
        ["csv-validator", str(tmp_path / "nope.csv"), "--schema", str(tmp_path / "nope.json")],
        capture_output=True, text=True
    )
    assert result.returncode != 0
    assert "CSV file not found" in result.stdout

def test_markdown_and_html_report(tmp_path):
    csv_path = tmp_path / "data.csv"
    schema_path = tmp_path / "schema.json"

    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["name"])
        writer.writerow(["Bob"])

    schema = {"columns": [{"name": "name", "type": "string"}]}
    schema_path.write_text(json.dumps(schema))

    result = subprocess.run(
        ["csv-validator", str(csv_path), "--schema", str(schema_path), "--markdown", "--html"],
        capture_output=True, text=True
    )

    assert result.returncode == 0
    assert "📝 Markdown report saved to:" in result.stdout
    assert "🌐 HTML report saved to:" in result.stdout