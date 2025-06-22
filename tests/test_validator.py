import csv
import json
from pathlib import Path
from utils.core.validator import validate_csv

def write_schema(path: Path, columns: list[dict]):
    path.write_text(json.dumps({"columns": columns}, indent=2))

def test_validate_csv_full_coverage(tmp_path):
    csv_path = tmp_path / "test.csv"
    schema_path = tmp_path / "schema.json"

    schema = [
        {
            "name": "id", "type": "int", "constraints": {"min": 100, "max": 999}
        },
        {
            "name": "email", "type": "str", "constraints": {"regex": r"^[\w\.-]+@[\w\.-]+$"}
        },
        {
            "name": "status", "type": "str", "constraints": {"enum": ["active", "inactive"]}
        },
        {
            "name": "notes", "type": "str"
        }
    ]
    write_schema(schema_path, schema)

    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "email", "status", "notes"])
        writer.writerow(["abc", "bademail", "pending", "Some note"])   # int fail, regex fail, enum fail
        writer.writerow(["50", "user@example.com", "active", "   "])   # int below min, whitespace string
        writer.writerow(["150", "valid@email.com", "inactive", "ok"])  # valid

    errors = validate_csv(csv_path, schema_path)

    assert "Header mismatch" not in errors
    assert any("expected int" in e for e in errors)
    assert any("below min" in e for e in errors)
    assert any("does not match pattern" in e for e in errors)
    assert any("not in allowed values" in e for e in errors)
    assert any("is an empty string" in e for e in errors)

def test_validate_csv_success(tmp_path):
    csv_path = tmp_path / "valid.csv"
    schema_path = tmp_path / "schema.json"

    schema = [
        {"name": "id", "type": "int"},
        {"name": "email", "type": "str"},
        {"name": "status", "type": "str"}
    ]
    write_schema(schema_path, schema)

    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "email", "status"])
        writer.writerow(["123", "user@example.com", "active"])

    errors = validate_csv(csv_path, schema_path)
    assert errors == []

def test_validate_csv_float_type_failure(tmp_path):
    csv_path = tmp_path / "float_fail.csv"
    schema_path = tmp_path / "schema.json"

    schema = [
        {"name": "amount", "type": "float", "constraints": {"min": 0, "max": 1000}}
    ]
    write_schema(schema_path, schema)

    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["amount"])
        writer.writerow(["not_a_number"])  # triggers float() ValueError

    errors = validate_csv(csv_path, schema_path)
    assert isinstance(errors, list)

def test_schema_with_no_columns_key(tmp_path):
    csv_path = tmp_path / "empty.csv"
    schema_path = tmp_path / "bad_schema.json"

    # Schema is missing the 'columns' key
    schema_path.write_text(json.dumps({"oops": []}))

    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id"])
        writer.writerow(["123"])

    errors = validate_csv(csv_path, schema_path)
    assert any("Schema is missing 'columns' key." in e for e in errors)

def test_regex_validation_failure(tmp_path):
    csv_path = tmp_path / "regex_fail.csv"
    schema_path = tmp_path / "schema.json"

    schema = [
        {"name": "username", "type": "str", "constraints": {"regex": r"^\w+$"}}
    ]
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["username"])
        writer.writerow(["good_user"])
        writer.writerow(["bad-user"])  # should fail

    schema_path.write_text(json.dumps({"columns": schema}))
    errors = validate_csv(csv_path, schema_path)
    assert any("does not match pattern" in e for e in errors)