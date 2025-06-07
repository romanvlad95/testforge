# 🔪 TestForge

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)
![Version](https://img.shields.io/badge/version-0.1.0-yellow)

TestForge is a lightweight Python CLI toolkit for generating, validating, and managing synthetic CSV datasets. Built to streamline testing and automation workflows, it enables fast schema inference, data validation, and batch reporting — all via terminal.

---

## 🚀 Features

* 🔍 Validate CSV files against a flexible JSON schema
* 🧬 Generate synthetic test CSVs from templates
* 🧠 Infer schema from existing CSVs
* 📋 Enforce schema constraints:

  * `min` / `max`
  * `regex`
  * `enum`
* 💾 Create plaintext, Markdown, and HTML validation reports
* 🔪 Validate CSVs in **batch mode** using `csv-tester`
* ✅ Fully CLI-based — ideal for scripting, CI, and pipelines
* 📂 Structured logs in `/reports/validation_logs/`

---

## 🛠️ CLI Tools

Once installed via `pip install -e .`, these commands become available:

| Command            | Description                          |
| ------------------ | ------------------------------------ |
| `csv-validator`    | Validate a CSV against a JSON schema |
| `csv-generator`    | Generate test CSVs from a template   |
| `schema-generator` | Infer JSON schema from a sample CSV  |
| `csv-tester`       | Validate multiple CSVs in a folder   |

---

## 🤪 Example Usage

### Validate a single CSV file:

```bash
csv-validator test.csv --schema schema_definition.json
```

### With Markdown + HTML reports:

```bash
csv-validator test.csv --schema schema_definition.json --markdown --html
```

### Batch validate all CSVs in a folder:

```bash
csv-tester test_cases/batch --schema schema_definition.json
```

### Generate synthetic CSV data:

```bash
csv-generator test_cases/templates/template.csv output.csv --rows 25
```

### Infer a schema from a CSV:

```bash
schema-generator sample.csv inferred_schema.json
```
<!-- TODO: Add demo GIF here -->
---

## 🤪 Schema Example

```json
{
  "columns": [
    { "name": "age", "type": "int", "constraints": { "min": 18, "max": 99 } },
    { "name": "email", "type": "str", "constraints": { "regex": "^[^@]+@[^@]+\\.[^@]+$" } },
    { "name": "country", "type": "str", "constraints": { "enum": ["US", "UK", "BG"] } }
  ]
}
```


---
### 📐 JSON Schema Format

Each schema defines an array of `columns`, with optional constraints:

```json
{
  "columns": [
    {"name": "age", "type": "int", "constraints": {"min": 18, "max": 99}},
    {"name": "email", "type": "str", "constraints": {"regex": "^[^@]+@[^@]+\\.[^@]+$"}},
    {"name": "color", "type": "str", "constraints": {"enum": ["red", "blue", "green"]}}
  ]
}
---

## 📆 Output

* ✅ Plaintext `.log` reports in `reports/validation_logs/`
* 📜 Optional `.md` and `.html` reports for human-friendly validation summaries

---

## 📚 License

MIT — Use it, hack it, ship it.

---

## 🙏 Credits

Developed by [romanvlad95](https://github.com/romanvlad95)
