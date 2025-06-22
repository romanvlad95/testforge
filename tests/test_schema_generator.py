import csv
import subprocess
from pathlib import Path
from utils.core import schema as schema_generator

def test_infer_schema_typing(tmp_path):
    csv_path = tmp_path / "mixed.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "email", "price", "comment"])
        writer.writerow(["123", "user@example.com", "10.5", "Nice"])
        writer.writerow(["456", "another@test.com", "7.2", "Okay"])
        writer.writerow(["789", "test@x.com", "9.9", "Cool"])

    schema = schema_generator.infer_schema(csv_path)

    expected = [
        {"name": "id", "type": "int"},
        {"name": "email", "type": "email"},
        {"name": "price", "type": "float"},
        {"name": "comment", "type": "string"},
    ]
    assert schema == expected

def test_infer_schema_raises_without_headers(tmp_path):
    csv_path = tmp_path / "no_headers.csv"
    # Write empty file to simulate header-less CSV
    csv_path.write_text("")

    try:
        schema_generator.infer_schema(csv_path)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "no headers" in str(e).lower()

def test_infer_schema_with_empty_and_mixed_data(tmp_path):
    csv_path = tmp_path / "fuzzy.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["score", "feedback"])
        writer.writerow(["", "Excellent"])
        writer.writerow(["", ""])
        writer.writerow(["42", "Good"])
        writer.writerow(["", "Average"])

    schema = schema_generator.infer_schema(csv_path)

    expected = [
        {"name": "score", "type": "int"},      # one valid int, rest empty
        {"name": "feedback", "type": "string"} # mix of empty and text
    ]
    assert schema == expected

def test_infer_schema_edge_cases(tmp_path):
    csv_path = tmp_path / "edge.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["weird", "emailish", "blank"])
        writer.writerow(["1.0", "test@example.com", ""])
        writer.writerow(["2", "another@test.com", "  "])
        writer.writerow(["3.3", "fake@email.com", ""])

    schema = schema_generator.infer_schema(csv_path)

    expected = [
        {"name": "weird", "type": "float"},     # mix of int + float, float wins
        {"name": "emailish", "type": "email"},  # all emails
        {"name": "blank", "type": "string"}     # only empty = default
    ]
    assert schema == expected

def test_infer_schema_type_resolution_conflict(tmp_path):
    csv_path = tmp_path / "conflict.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["conflict"])
        writer.writerow(["1"])                # int
        writer.writerow(["2.5"])              # float
        writer.writerow(["hello"])            # string
        writer.writerow(["user@example.com"]) # email
        writer.writerow(["3"])                # int again

    schema = schema_generator.infer_schema(csv_path)

    # int appears twice, so it should win
    expected = [{"name": "conflict", "type": "int"}]
    assert schema == expected

def test_schema_generator_fails_on_headerless_csv(tmp_path):
    csv_path = tmp_path / "broken.csv"
    out_path = tmp_path / "schema.json"

    csv_path.write_text("")  # empty file

    result = subprocess.run(
        ["schema-generator", str(csv_path), str(out_path)],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0  # CLI does not crash
    assert "❌ Failed to infer schema" in result.stdout

def test_cli_success(tmp_path):
    csv_path = tmp_path / "template.csv"
    out_path = tmp_path / "schema.json"

    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "name"])
        writer.writerow(["1", "Alice"])

    result = subprocess.run(
        ["schema-generator", str(csv_path), str(out_path)],
        capture_output=True, text=True
    )

    assert result.returncode == 0
    assert "🧬 Schema generated and saved to:" in result.stdout
    assert out_path.exists()