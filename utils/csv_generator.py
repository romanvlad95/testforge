import csv
import json
import random
import re
from pathlib import Path

def generate_random_row(schema):
    row = []
    for col in schema['columns']:
        if col['type'] == 'int':
            row.append(str(random.randint(0, 100)))
        elif col['type'] == 'str':
            row.append('user_' + str(random.randint(1000, 9999)))
        else:
            row.append('')
    return row

def get_next_filename(directory: Path, prefix: str = "test_case_", suffix: str = ".csv") -> Path:
    existing = [f.name for f in directory.glob(f"{prefix}*{suffix}")]
    numbers = [
        int(re.search(rf"{prefix}(\d+){suffix}", name).group(1))
        for name in existing
        if re.search(rf"{prefix}(\d+){suffix}", name)
    ]
    next_index = max(numbers) + 1 if numbers else 1
    filename = f"{prefix}{next_index:02d}{suffix}"
    return directory / filename

def generate_csv(schema_path: Path, output_dir: Path, num_rows: int = 10):
    with open(schema_path) as f:
        schema = json.load(f)

    output_path = get_next_filename(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        headers = [col['name'] for col in schema['columns']]
        writer.writerow(headers)
        for _ in range(num_rows):
            writer.writerow(generate_random_row(schema))

    print(f"✅ Generated: {output_path.name}")

# Example usage
if __name__ == "__main__":
    schema = Path("./schema_definition.json")
    output_dir = Path("./test_cases/generated")
    generate_csv(schema, output_dir)