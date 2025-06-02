import csv
import os
import subprocess
import sys
from pathlib import Path

from testforge.core import schema as schema_generator


def test_infer_schema_typing(tmp_path: Path):
    """Tests the schema inference for various data types.

    Args:
        tmp_path (Path): pytest fixture for a temporary directory.
    """
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


def test_infer_schema_raises_without_headers(tmp_path: Path):
    """Tests that schema inference raises an error for CSVs without headers.

    Args:
        tmp_path (Path): pytest fixture for a temporary directory.
    """
    csv_path = tmp_path / "no_headers.csv"
    csv_path.write_text("")

    try:
        schema_generator.infer_schema(csv_path)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "no headers" in str(e).lower()


def test_infer_schema_with_empty_and_mixed_data(tmp_path: Path):
    """Tests schema inference with empty and mixed data types.

    Args:
        tmp_path (Path): pytest fixture for a temporary directory.
    """
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
        {"name": "score", "type": "int"},
        {"name": "feedback", "type": "string"},
    ]
    assert schema == expected


def test_infer_schema_edge_cases(tmp_path: Path):
    """Tests schema inference with edge cases for type resolution.

    Args:
        tmp_path (Path): pytest fixture for a temporary directory.
    """
    csv_path = tmp_path / "edge.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["weird", "emailish", "blank"])
        writer.writerow(["1.0", "test@example.com", ""])
        writer.writerow(["2", "another@test.com", "  "])
        writer.writerow(["3.3", "fake@email.com", ""])

    schema = schema_generator.infer_schema(csv_path)

    expected = [
        {"name": "weird", "type": "float"},
        {"name": "emailish", "type": "email"},
        {"name": "blank", "type": "string"},
    ]
    assert schema == expected


def test_infer_schema_type_resolution_conflict(tmp_path: Path):
    """Tests schema inference when there are conflicting types in a column.

    Args:
        tmp_path (Path): pytest fixture for a temporary directory.
    """
    csv_path = tmp_path / "conflict.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["conflict"])
        writer.writerow(["1"])
        writer.writerow(["2.5"])
        writer.writerow(["hello"])
        writer.writerow(["user@example.com"])
        writer.writerow(["3"])

    schema = schema_generator.infer_schema(csv_path)

    expected = [{"name": "conflict", "type": "int"}]
    assert schema == expected


def test_schema_generator_fails_on_headerless_csv(tmp_path: Path):
    """Tests the CLI's behavior when inferring schema from a headerless CSV.

    Args:
        tmp_path (Path): pytest fixture for a temporary directory.
    """
    csv_path = tmp_path / "broken.csv"
    out_path = tmp_path / "schema.json"

    csv_path.write_text("")

    try:
        stdout_content = subprocess.check_output(
            [
                sys.executable,
                "-m",
                "testforge.cli.__main__",
                "schema",
                str(csv_path),
                str(out_path),
            ],
            stderr=subprocess.PIPE,
            text=True,
            env=os.environ,
        )
        result_code = 0
    except subprocess.CalledProcessError as e:
        print(f"Stderr: {e.stderr}")
        stdout_content = e.stdout
        result_code = e.returncode

    assert result_code == 0
    assert "Failed to infer schema" in stdout_content


def test_cli_success(tmp_path: Path):
    """Tests successful schema inference via the CLI.

    Args:
        tmp_path (Path): pytest fixture for a temporary directory.
    """
    csv_path = tmp_path / "template.csv"
    out_path = tmp_path / "schema.json"

    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "name"])
        writer.writerow(["1", "Alice"])

    try:
        stdout_content = subprocess.check_output(
            [
                sys.executable,
                "-m",
                "testforge.cli.__main__",
                "schema",
                str(csv_path),
                str(out_path),
            ],
            stderr=subprocess.PIPE,
            text=True,
            env=os.environ,
        )
        result_code = 0
    except subprocess.CalledProcessError as e:
        print(f"Stderr: {e.stderr}")
        stdout_content = e.stdout
        result_code = e.returncode

    assert result_code == 0
    assert "Schema generated and saved to:" in stdout_content
    assert out_path.exists()
