from pathlib import Path

LICENSE_HEADER = """# MIT License
# Copyright (c) 2025 Vlad
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND...
"""

def insert_license(file_path: Path):
    content = file_path.read_text()
    if content.startswith("# MIT License"):
        print(f"✅ Skipped (already licensed): {file_path}")
        return

    file_path.write_text(LICENSE_HEADER.rstrip() + "\n\n" + content)
    print(f"✨ Added license: {file_path}")

def main():
    utils_dir = Path(__file__).resolve().parent.parent / "utils"
    py_files = list(utils_dir.glob("*.py"))

    for py_file in py_files:
        insert_license(py_file)

if __name__ == "__main__":
    main()