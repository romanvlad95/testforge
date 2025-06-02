"""Splash screen and welcome message for the CLI."""

import pyfiglet
from colorama import Fore, Style


def get_splash_screen() -> str:
    """Generates a formatted splash screen for the CLI.

    This function creates a welcome message that includes ASCII art, a brief
    description, and a summary of available commands and usage examples.

    Returns:
        A string containing the full, color-formatted splash screen.
    """
    title = pyfiglet.figlet_format("TestForge", font="slant")

    welcome_message = f"""
{Fore.CYAN}{title}{Style.RESET_ALL}
{Fore.YELLOW}Welcome to TestForge!{Style.RESET_ALL}
A lightweight CLI for CSV data generation and validation.

{Fore.GREEN}Available Commands:{Style.RESET_ALL}
  {Fore.WHITE}validate   {Style.RESET_ALL} Validate a CSV file against a JSON schema.
  {Fore.WHITE}generate   {Style.RESET_ALL} Generate synthetic CSV data from a template.
  {Fore.WHITE}schema     {Style.RESET_ALL} Infer a JSON schema from a CSV file.
  {Fore.WHITE}batch      {Style.RESET_ALL} Validate all CSV files in a directory.

{Fore.GREEN}Usage:{Style.RESET_ALL}
  testforge [COMMAND] --help

{Fore.BLUE}Example:{Style.RESET_ALL}
  testforge validate tests/test_case_data/ci_clean.csv \
    --schema examples/schema_definition.json
"""
    return welcome_message
