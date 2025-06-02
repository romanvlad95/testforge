# 🧪 TestForge

![Python](https://img.shields.io/badge/python-3.12+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

**TestForge** is a Python-powered CLI toolkit for generating and validating test cases based on CSV schemas.
It’s built to automate QA processes, sanity checks, and input validation for CSV-based workflows — fast, clean, and real-world useful.

---

## 🚀 Features

* ✅ Schema-driven CSV validation (type enforcement, required fields)
* 🧬 Auto-generation of valid CSV test data
* ⚠️ Catch invalid rows and log detailed error reports
* 🧾 Custom JSON schema format for flexibility
* 🧪 CLI support with `argparse` for single-file or batch runs
* 📂 Organized output: logs, test cases, inputs

---

## 📦 Installation

```bash
# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 📁 Folder Structure

```
testforge/
├── main.py                 # CLI entry point
├── schema_definition.json  # Expected schema for CSVs
├── test_cases/             # Auto-generated test CSVs
│   ├── generated/
│   └── templates/
├── csv_inputs/             # Manually prepared CSVs
├── reports/                # Output validation logs
│   └── validation_logs/
└── utils/                  # Generator, validator, logger
    ├── csv_generator.py
    ├── csv_validator.py
    └── report_writer.py
```

---

## ⚙️ Usage

### 🧪 Generate a Test CSV

```bash
python utils/csv_generator.py
```

Creates a new `test_case_XX.csv` file in `test_cases/generated/`.

---

### ✅ Validate the Latest File

```bash
python main.py
```

Or validate a specific one:

```bash
python main.py --file test_cases/generated/test_case_02.csv
```

---

## 📷 Preview

<img src="https://user-images.githubusercontent.com/your-id/testforge-demo.gif" width="700" alt="TestForge CLI Demo">

---

## 📄 Schema Format

```json
{
  "columns": [
    { "name": "id", "type": "int" },
    { "name": "username", "type": "str" },
    { "name": "score", "type": "int" }
  ]
}
```

You can extend this schema in the future to support:

* Required vs optional fields
* Uniqueness constraints
* Regex validation
* Custom types

---

## 🛠️ Tech Stack

* Python 3.12+
* `argparse`, `csv`, `json`
* Fully standalone (no third-party libs required)

---

## 📌 Roadmap

* [ ] Invalid test case generator (edge cases)
* [ ] Schema validator with field constraints
* [ ] Rich CLI output with `colorama`
* [ ] Pytest-based unit tests
* [ ] Packaged as `pip`-installable CLI

---

## 💡 Why TestForge?

Because manually validating CSVs is boring and error-prone.
TestForge makes it **repeatable**, **automated**, and **developer-friendly**.

---

## 📜 License

MIT — free to use, abuse, and fork.

---
