import subprocess
import json
import csv
from pathlib import Path

def run_csv_tester(args: list[str]) -> tuple[int, str, str]:
    result = subprocess.run(
        ["csv-tester"] + args,
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout, result.stderr


def test_cli_missing_csv_dir(tmp_path):
    schema = tmp_path / "schema.json"
    schema.write_text(json.dumps({"columns": [{"name": "name", "type": "string"}]}))
    code, out, _ = run_csv_tester([str(tmp_path / "missing"), "--schema", str(schema)])
    assert "❌ CSV directory not found" in out


def test_cli_missing_schema_file(tmp_path):
    csv_dir = tmp_path / "csvs"
    csv_dir.mkdir()
    code, out, _ = run_csv_tester([str(csv_dir), "--schema", str(tmp_path / "ghost_schema.json")])
    assert "❌ Schema file not found" in out


def test_cli_creates_output_dir_and_logs(tmp_path):
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

    code, out, _ = run_csv_tester([
        str(csv_dir),
        "--schema", str(schema_path),
        "--output", str(output_dir)
    ])
    assert code == 0
    assert output_dir.exists()
    log = output_dir / "valid_validation.log"
    assert log.exists()
    assert "No issues found" in log.read_text()