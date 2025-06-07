import json
from utils.csv_validator import validate_csv

def create_test_files(tmp_path, csv_content, schema_dict):
    csv_path = tmp_path / "input.csv"
    schema_path = tmp_path / "schema.json"

    csv_path.write_text(csv_content)
    schema_path.write_text(json.dumps(schema_dict))

    return str(csv_path), str(schema_path)

def test_empty_csv_file(tmp_path):
    csv_content = ""
    schema = {"columns": [{"name": "id", "type": "int"}]}
    csv_path, schema_path = create_test_files(tmp_path, csv_content, schema)

    errors = validate_csv(csv_path, schema_path)
    assert any("Header mismatch" in e for e in errors)

def test_extra_column(tmp_path):
    csv_content = "id,name\n1,Alice"
    schema = {"columns": [{"name": "id", "type": "int"}]}
    csv_path, schema_path = create_test_files(tmp_path, csv_content, schema)

    errors = validate_csv(csv_path, schema_path)
    assert "Header mismatch" in errors[0]

def test_wrong_type_int(tmp_path):
    csv_content = "id\nnot_an_int"
    schema = {"columns": [{"name": "id", "type": "int"}]}
    csv_path, schema_path = create_test_files(tmp_path, csv_content, schema)

    errors = validate_csv(csv_path, schema_path)
    assert "expected int" in errors[0]

def test_valid_csv(tmp_path):
    csv_content = "id\n42"
    schema = {"columns": [{"name": "id", "type": "int"}]}
    csv_path, schema_path = create_test_files(tmp_path, csv_content, schema)

    errors = validate_csv(csv_path, schema_path)
    assert not errors

def test_constraints_min_max_and_regex(tmp_path):
    csv_content = "age,email\n17,not-an-email\n120,good@bad\n42,wrong_format"
    schema = {
        "columns": [
            {"name": "age", "type": "int", "constraints": {"min": 18, "max": 99}},
            {"name": "email", "type": "str", "constraints": {"regex": r"^[^@]+@[^@]+\.[^@]+$"}}
        ]
    }
    csv_path, schema_path = create_test_files(tmp_path, csv_content, schema)
    errors = validate_csv(csv_path, schema_path)
    assert len(errors) == 5
    assert any("below min" in e for e in errors)
    assert any("above max" in e for e in errors)
    assert sum("does not match pattern" in e for e in errors) == 3

def test_enum_constraint(tmp_path):
    csv_content = "color\nred\nblue\nyellow"
    schema = {
        "columns": [
            {"name": "color", "type": "str", "constraints": {"enum": ["red", "blue", "green"]}}
        ]
    }
    csv_path, schema_path = create_test_files(tmp_path, csv_content, schema)
    errors = validate_csv(csv_path, schema_path)
    assert len(errors) == 1
    assert "not in allowed values" in errors[0]

def test_enum_with_empty_string(tmp_path):
    csv_content = "color\nred\n\"\"\nblue"
    schema = {
        "columns": [
            {"name": "color", "type": "str", "constraints": {"enum": ["red", "blue", "green"]}}
        ]
    }
    csv_path, schema_path = create_test_files(tmp_path, csv_content, schema)
    errors = validate_csv(csv_path, schema_path)
    assert len(errors) == 2
    assert any("empty string" in e for e in errors)
    assert any("not in allowed values" in e for e in errors)

def test_missing_field_with_regex(tmp_path):
    csv_content = "email\njohn@example.com\n"
    schema = {
        "columns": [
            {"name": "email", "type": "str", "constraints": {"regex": r"^[^@]+@[^@]+\.[^@]+$"}},
            {"name": "username", "type": "str", "constraints": {"regex": r"^\w+$"}}
        ]
    }
    csv_path, schema_path = create_test_files(tmp_path, csv_content, schema)
    errors = validate_csv(csv_path, schema_path)
    assert any("Missing field 'username'" in e for e in errors)

def test_csv_with_extra_valid_columns(tmp_path):
    csv_content = "id,name,extra\n1,Alice,surplus"
    schema = {
        "columns": [
            {"name": "id", "type": "int"},
            {"name": "name", "type": "str"}
        ]
    }
    csv_path, schema_path = create_test_files(tmp_path, csv_content, schema)
    errors = validate_csv(csv_path, schema_path)
    assert any("Header mismatch" in e for e in errors)