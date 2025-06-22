import tempfile
from pathlib import Path

from utils.core.report import write_validation_report

def test_write_validation_report_creates_log_file():
    test_errors = [
        "Row 2: Field 'age' expected int but got 'abc'",
        "Row 5: Missing field 'email'"
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "test_manual.log"
        write_validation_report(output_path, test_errors)

        assert output_path.exists(), "Log file was not created"
        contents = output_path.read_text()
        assert "Row 2" in contents
        assert "Row 5" in contents