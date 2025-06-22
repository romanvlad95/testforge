🧪 TestForge
TestForge is a powerful yet lightweight Python CLI toolkit for generating, validating, and managing synthetic CSV datasets. Designed for testing and automation workflows, it enables fast schema inference, batch validation, and structured reporting — all via your terminal.

🚀 Features
🔍 Validate CSV files against a flexible JSON schema

🧬 Generate synthetic test CSVs from templates

🧠 Infer schemas from existing CSVs

📋 Enforce constraints:

min / max

regex

enum

💾 Generate reports in plaintext, Markdown, and HTML formats

🔪 Batch validation mode via csv-tester

✅ Fully CLI-driven — perfect for CI/CD, scripting, and pipelines

📂 All logs saved in /reports/validation_logs/

⚙️ Getting Started
Prerequisites

Python 3.13+

Installation

Clone the repository:

git clone https://github.com/romanvlad95/testforge.git
cd testforge

Create and activate a virtual environment:

# For macOS/Linux
python3 -m venv .venv
source .venv/bin/activate

# For Windows
python -m venv .venv
.venv\Scripts\activate

Install the project in editable mode:
This command installs the package and its command-line scripts while allowing you to edit the source code directly. This is essential for development and running tests.

pip install -e .

After installation, the CLI tools will be available in your shell.

✅ Running Tests
This project uses pytest for testing and pytest-cov for coverage analysis.

Run the full test suite:

pytest

Check test coverage with an HTML report:
This will generate an interactive report in a new htmlcov/ directory.

pytest --cov --cov-report=html
open htmlcov/index.html

🛠️ CLI Tools
Once installed, the following tools become available globally:

Command

Description

csv-validator

Validate a single CSV against schema

csv-generator

Generate synthetic CSVs from template

schema-generator

Infer JSON schema from sample CSV

csv-tester

Validate all CSVs in a folder

💡 Example Usage
✅ Validate a CSV file:

csv-validator test.csv --schema schema_definition.json

📄 With Markdown & HTML reports:

csv-validator test.csv --schema schema_definition.json --markdown --html

🔄 Batch validate a folder:

csv-tester test_cases/batch --schema schema_definition.json

🧬 Generate test data:

csv-generator test_cases/templates/template.csv output.csv --rows 25

🧠 Infer schema from CSV:

schema-generator sample.csv inferred_schema.json

📐 JSON Schema Format
Each schema defines a list of columns, each with optional constraints:

{
  "columns": [
    {"name": "age", "type": "int", "constraints": {"min": 18, "max": 99}},
    {"name": "email", "type": "str", "constraints": {"regex": "^[^@]+@[^@]+\\.[^@]+$"}},
    {"name": "country", "type": "str", "constraints": {"enum": ["US", "UK", "BG"]}}
  ]
}

📦 Output Files
📄 .log files written to reports/validation_logs/

📜 Optional .md and .html reports for readable summaries

📚 License
MIT License — Free to use, modify, and distribute.

🙏 Author
Built with intent by romanvlad95

