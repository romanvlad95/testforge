from datetime import datetime
from pathlib import Path

LOG_DIR = Path("reports/validation_logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

def write_log(errors, filename):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    log_filename = f"validation_{timestamp}.log"
    log_path = LOG_DIR / log_filename

    with open(log_path, "w") as f:
        f.write(f"Validation Report for {filename}\n")
        f.write("=" * 40 + "\n\n")

        if errors:
            for err in errors:
                f.write(f"{err}\n")
        else:
            f.write("No issues found.\n")

    print(f"📄 Report written to: {log_path}")