from pathlib import Path
from utils.report_writer import write_validation_report

test_errors = [
    "Row 2: Field 'age' expected int but got 'abc'",
    "Row 5: Missing field 'email'"
]

output_path = Path("reports/validation_logs/test_manual.log")
output_path.parent.mkdir(parents=True, exist_ok=True)

write_validation_report(output_path, test_errors)