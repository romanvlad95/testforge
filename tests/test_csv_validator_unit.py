import pytest
from utils.core.validator import validate_field, parse_constraints, validate_header

# --------------------
# validate_field
# --------------------

def test_validate_field_empty_string():
    errors = validate_field("", "str", 1, "name")
    assert "Row 1: Field 'name' is an empty string" in errors

def test_validate_field_non_digit_for_int():
    errors = validate_field("abc", "int", 2, "age")
    assert "Row 2: Field 'age' expected int but got 'abc'" in errors

def test_validate_field_valid_values():
    assert validate_field("123", "int", 1, "id") == []
    assert validate_field("hello", "str", 1, "msg") == []

# --------------------
# parse_constraints
# --------------------

def test_constraints_min_max_inside_range():
    constraints = {"min": 10, "max": 100}
    assert parse_constraints("50", constraints, "int", 1, "amount") == []

def test_constraints_below_min():
    constraints = {"min": 10}
    errors = parse_constraints("5", constraints, "int", 1, "price")
    assert "below min" in errors[0]

def test_constraints_above_max():
    constraints = {"max": 20}
    errors = parse_constraints("50", constraints, "float", 2, "score")
    assert "above max" in errors[0]

def test_constraints_regex_match():
    constraints = {"regex": r"^\w+@\w+\.\w+$"}
    errors = parse_constraints("invalid_email", constraints, "str", 1, "email")
    assert "does not match pattern" in errors[0]

def test_constraints_enum_valid_and_invalid():
    constraints = {"enum": ["A", "B", "C"]}
    assert parse_constraints("B", constraints, "str", 1, "grade") == []
    errors = parse_constraints("Z", constraints, "str", 1, "grade")
    assert "not in allowed values" in errors[0]

# --------------------
# validate_header
# --------------------

def test_validate_header_none():
    expected = ["id", "email"]
    errors = validate_header(None, expected)
    assert "Header mismatch: None" in errors[0]
    assert len(errors) == 3  # header + 2 missing

def test_validate_header_exact_match():
    assert validate_header(["id", "email"], ["id", "email"]) == []

def test_validate_header_mismatch():
    reader = ["id", "name"]
    expected = ["id", "email"]
    errors = validate_header(reader, expected)
    assert "Header mismatch" in errors[0]
    assert "Missing field 'email'" in errors
    assert "Unexpected extra field 'name'" in errors