from pathlib import Path
from utils.core import report as report_writer

def test_write_validation_report(tmp_path):
    output_file = tmp_path / "test_report.log"
    errors = ["Missing column 'name'", "Invalid age format"]

    report_writer.write_validation_report(output_file, errors)

    assert output_file.exists()
    content = output_file.read_text()
    assert "Validation Report" in content
    assert "Missing column 'name'" in content
    assert "Invalid age format" in content

def test_write_validation_report_no_errors(tmp_path):
    output_file = tmp_path / "clean_report.log"

    report_writer.write_validation_report(output_file, [])

    content = output_file.read_text()
    assert "No issues found." in content

def test_generate_markdown_report():
    errors = ["Field 'age' must be integer"]
    md = report_writer.generate_markdown_report(errors)

    assert "# Validation Report" in md
    assert "## Errors" in md
    assert "- Field 'age' must be integer" in md

def test_generate_markdown_report_clean():
    md = report_writer.generate_markdown_report([])

    assert "✅ No errors found." in md