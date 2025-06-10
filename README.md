# 🧪 TestForge

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)
![Version](https://img.shields.io/badge/version-1.0.0-green)
![CI](https://github.com/romanvlad95/testforge/actions/workflows/validate-csv.yml/badge.svg)

**TestForge** is a powerful yet lightweight Python CLI toolkit for generating, validating, and managing synthetic CSV datasets. Designed for testing and automation workflows, it enables fast schema inference, batch validation, and structured reporting — all via your terminal.

---

## 🚀 Features

* 🔍 Validate CSV files against a flexible JSON schema
* 🧬 Generate synthetic test CSVs from templates
* 🧠 Infer schemas from existing CSVs
* 📋 Enforce constraints:

  * `min` / `max`
  * `regex`
  * `enum`
* 💾 Generate reports in plaintext, Markdown, and HTML formats
* 🔪 Batch validation mode via `csv-tester`
* ✅ Fully CLI-driven — perfect for CI/CD, scripting, and pipelines
* 📂 All logs saved in `/reports/validation_logs/`

---

## 🛠️ CLI Tools

Once installed with `pip install .` or from the wheel, the following tools become available globally:

| Command            | Description                           |
| ------------------ | ------------------------------------- |
| `csv-validator`    | Validate a single CSV against schema  |
| `csv-generator`    | Generate synthetic CSVs from template |
| `schema-generator` | Infer JSON schema from sample CSV     |
| `csv-tester`       | Validate all CSVs in a folder         |

---

## 💡 Example Usage

### ✅ Validate a CSV file:

```bash
csv-validator test.csv --schema schema_definition.json
```

### 📄 With Markdown & HTML reports:

```bash
csv-validator test.csv --schema schema_definition.json --markdown --html
```

### 🔄 Batch validate a folder:

```bash
csv-tester test_cases/batch --schema schema_definition.json
```

### 🧬 Generate test data:

```bash
csv-generator test_cases/templates/template.csv output.csv --rows 25
```

### 🧠 Infer schema from CSV:

```bash
schema-generator sample.csv inferred_schema.json
```

<!-- 📹 TODO: Add demo GIF here -->

---

## 📐 JSON Schema Format

Each schema defines a list of `columns`, each with optional constraints:

```json
{
  "columns": [
    {"name": "age", "type": "int", "constraints": {"min": 18, "max": 99}},
    {"name": "email", "type": "str", "constraints": {"regex": "^[^@]+@[^@]+\\.[^@]+$"}},
    {"name": "country", "type": "str", "constraints": {"enum": ["US", "UK", "BG"]}}
  ]
}
```

---

## 📦 Output Files

* 📄 `.log` files written to `reports/validation_logs/`
* 📜 Optional `.md` and `.html` reports for readable summaries

---

## 📚 License

MIT License — Free to use, modify, and distribute.

---

## 🙏 Author

Built with intent by [romanvlad95](https://github.com/romanvlad95)
