from utils import csv_validator

def test_valid_csv():
    test_file = "test_cases/generated/test_case_01.csv"
    schema_file = "schema_definition.json"

    # Act
    result = csv_validator.validate_csv(test_file, schema_file)

    # Assert that result is an empty list (no errors)
    assert result == []