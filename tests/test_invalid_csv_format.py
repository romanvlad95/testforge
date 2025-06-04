import json
from utils.csv_validator import validate_csv

def test_csv_with_missing_column(tmp_path):
    csv_file = tmp_path / "bad.csv"
    csv_file.write_text("name\nAlice\nBob")

    schema = {
        "columns": [
            {"name": "name", "type": "str"},
            {"name": "age", "type": "int"}
        ]
    }
    schema_file = tmp_path / "schema.json"
    schema_file.write_text(json.dumps(schema))

    errors = validate_csv(str(csv_file), str(schema_file))
    assert any("Missing field 'age'" in e for e in errors)