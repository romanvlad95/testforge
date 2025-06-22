import csv
from pathlib import Path
from utils.devtools.generators import csv_generator

def test_generate_csv(tmp_path):
    # Create a fake template CSV with common headers
    template_path = tmp_path / "template.csv"
    output_path = tmp_path / "output.csv"

    headers = ["user_id", "email", "name", "age", "misc"]
    with open(template_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)

    # Generate 5 dummy rows
    csv_generator.generate_csv(template_path, output_path, rows=5)

    # Read output and verify structure
    assert output_path.exists()
    with open(output_path, newline="") as f:
        reader = list(csv.reader(f))
        assert reader[0] == headers             # Header row
        assert len(reader) == 6                 # 1 header + 5 rows
        for row in reader[1:]:
            assert len(row) == len(headers)     # Each row has all fields