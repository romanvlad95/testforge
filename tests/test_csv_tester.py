import json
import csv
from pathlib import Path
from utils import csv_tester

def test_validate_batch(tmp_path):
    # === Setup test files ===
    schema_path = tmp_path / "schema.json"
    csv_dir = tmp_path / "csvs"
    output_dir = tmp_path / "output"
    csv_dir.mkdir()
    output_dir.mkdir()

    # Create schema expecting column "name"
    schema = {"columns": [{"name": "name", "type": "string"}]}
    schema_path.write_text(json.dumps(schema))

    # Create 2 CSVs — one valid, one missing required column
    valid_csv = csv_dir / "valid.csv"
    invalid_csv = csv_dir / "invalid.csv"

    with open(valid_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["name"])
        writer.writerow(["Alice"])

    with open(invalid_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["age"])
        writer.writerow(["30"])

    # === Run the batch validation ===
    results = csv_tester.validate_batch(csv_dir, schema_path, output_dir)

    # === Assert logs are created ===
    valid_log = output_dir / "valid_validation.log"
    invalid_log = output_dir / "invalid_validation.log"

    assert valid_log.exists()
    assert invalid_log.exists()

    # === Assert results contain correct error counts ===
    result_dict = dict(results)
    assert result_dict["valid.csv"] == 0
    assert result_dict["invalid.csv"] > 0