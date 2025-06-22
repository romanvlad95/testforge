# MIT License
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

import os
from pathlib import Path

# Set project root to the parent of the 'utils' folder, which is the top-level directory.
# This makes the script's location independent.
project_root = Path(__file__).resolve().parent.parent.parent.parent
output_file = project_root / "project_snapshot.txt"


def should_include(file_path: Path) -> bool:
    """Determines if a file should be included in the project snapshot."""
    # Exclude files in __pycache__, virtual environments, and egg-info directories
    is_in_excluded_dir = any(
        part in [".venv_clean_test", "__pycache__"] or part.endswith(".egg-info")
        for part in file_path.parts
    )

    return file_path.suffix == ".py" and not is_in_excluded_dir


with open(output_file, "w", encoding="utf-8") as outfile:
    # Use rglob to recursively find all Python files starting from the corrected project_root
    for path in sorted(project_root.rglob("*.py")):  # Using sorted() for consistent order
        if should_include(path):
            try:
                rel_path = path.relative_to(project_root)
                outfile.write(f"\n\n### FILE: {rel_path} ###\n\n")
                with open(path, "r", encoding="utf-8") as f:
                    outfile.write(f.read())
            except Exception as e:
                print(f"Error processing file {path}: {e}")

print(f"✅ Project snapshot written to: {output_file}")