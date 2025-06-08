import subprocess
import csv
from pathlib import Path


def test_csv_generator_help():
    result = subprocess.run(
        ["csv-generator", "--help"],
        capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "Generate dummy CSV data" in result.stdout


def test_csv_generator_with_rows(tmp_path):
    template = tmp_path / "template.csv"
    output = tmp_path / "out.csv"

    # Create template with some headers
    with open(template, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["user_id", "email", "name", "age", "misc"])

    result = subprocess.run(
        ["csv-generator", str(template), str(output), "--rows", "5"],
        capture_output=True, text=True
    )

    assert result.returncode == 0
    assert "✅ Generated CSV at:" in result.stdout
    assert output.exists()

    with open(output, newline="") as f:
        reader = list(csv.reader(f))

    assert reader[0] == ["user_id", "email", "name", "age", "misc"]
    assert len(reader) == 6  # header + 5 rows
    for row in reader[1:]:
        assert len(row) == 5


def test_csv_generator_missing_template():
    result = subprocess.run(
        ["csv-generator", "nonexistent.csv", "output.csv"],
        capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "❌ Template file not found" in result.stdout