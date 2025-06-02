"""Utility script to generate a snapshot of the project's Python files.

This script recursively finds all Python files within the project root,
excludes specified directories (e.g., virtual environments, cache),
and concatenates their content into a single output file.
"""

from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent.parent
output_file = project_root / "project_snapshot.txt"


def should_include(file_path: Path) -> bool:
    """Determines if a file should be included in the project snapshot.

    Args:
        file_path (Path): The path to the file.

    Returns:
        bool: True if the file should be included, False otherwise.
    """
    is_in_excluded_dir = any(
        part in [".venv_clean_test", "__pycache__"] or part.endswith(".egg-info")
        for part in file_path.parts
    )

    return file_path.suffix == ".py" and not is_in_excluded_dir


with open(output_file, "w", encoding="utf-8") as outfile:
    for path in sorted(
        project_root.rglob("*.py")
    ):  # Using sorted() for consistent order
        if should_include(path):
            try:
                rel_path = path.relative_to(project_root)
                outfile.write(f"\n\n### FILE: {rel_path} ###\n\n")
                with open(path, "r", encoding="utf-8") as f:
                    outfile.write(f.read())
            except Exception as e:
                print(f"Error processing file {path}: {e}")

print(f"Project snapshot written to: {output_file}")
