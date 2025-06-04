from setuptools import setup, find_packages

setup(
    name="testforge",
    version="0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "csv-validator=main:main",
            "csv-generator=utils.csv_generator:cli",
            "schema-generator=utils.schema_generator:cli",
        ],
    },
)