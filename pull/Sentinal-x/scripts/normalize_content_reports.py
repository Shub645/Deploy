import json
from pathlib import Path


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Input and output files
RAW_FILE = BASE_DIR / "data" / "raw" / "content_reports.json"
NORMALIZED_FILE = BASE_DIR / "data" / "normalized" / "content_reports_normalized.json"


def normalize_report(report):
    """
    Convert one raw content report into a clean, consistent format.
    """

    return {
        "report_id": str(report.get("report_id", "")).strip(),
        "user_id": str(report.get("user_id", "")).strip(),
        "content_id": str(report.get("content_id", "")).strip(),
        "timestamp": str(report.get("timestamp", "")).strip(),
        "report_type": str(report.get("report_type", "")).strip().lower(),
        "description": str(report.get("description", "")).strip(),
        "platform": str(report.get("platform", "")).strip().lower(),
        "status": str(report.get("status", "")).strip().lower()
    }


def main():
    if not RAW_FILE.exists():
        print(f"Error: Raw file not found: {RAW_FILE}")
        return

    with open(RAW_FILE, "r", encoding="utf-8") as file:
        raw_reports = json.load(file)

    normalized_reports = []

    for report in raw_reports:
        normalized_report = normalize_report(report)
        normalized_reports.append(normalized_report)

    NORMALIZED_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(NORMALIZED_FILE, "w", encoding="utf-8") as file:
        json.dump(normalized_reports, file, indent=2)

    print(f"Successfully normalized {len(normalized_reports)} content reports.")
    print(f"Saved to: {NORMALIZED_FILE}")


if __name__ == "__main__":
    main()