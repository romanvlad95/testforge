# TestForge

TestForge is a lightweight Python tool that helps you generate, validate, and log CSV test cases against a defined schema. Designed to be flexible and easy to integrate into your automation pipelines.

## Features

* Generate synthetic CSV files based on a defined schema
* Validate CSV files for type correctness and header structure
* Generate timestamped validation logs
* Integrate with GitHub Actions CI/CD

## Badges

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/github/license/romanvlad95/testforge)
![CI](https://github.com/romanvlad95/testforge/actions/workflows/validate-csv.yml/badge.svg)

## Directory Structure

```
.
├── csv_inputs/              # External input CSVs for validation
├── main.py                  # Main entry point (argparse CLI)
├── reports/validation_logs/ # Validation result logs
├── schema_definition.json   # Column names and types
├── test_cases/
│   ├── generated/           # Auto-generated test case files
│   └── templates/           # Optional manual CSV templates
├── utils/                   # Helper modules (generator, validator, reporter)
└── requirements.txt
```

## Installation

```bash
git clone https://github.com/romanvlad95/testforge.git
cd testforge
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

### Generate a test CSV:

```bash
python utils/csv_generator.py
```

This will create a file like `test_case_01.csv` inside `test_cases/generated/`.

### Validate a test case:

```bash
python main.py --file test_cases/generated/test_case_01.csv
```

Log will be written to `reports/validation_logs/validation_YYYY-MM-DD_HHMM.log`.

### Default Behavior:

If no `--file` is passed, it defaults to `test_cases/generated/test_case_01.csv`.

## GitHub Actions CI

GitHub Actions automatically runs `main.py` on each push to validate a generated test case file.

Workflow path:

```
.github/workflows/validate-csv.yml
```

## License

This project is licensed under the MIT License.
