import json
from pathlib import Path


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Input and output files
RAW_FILE = BASE_DIR / "data" / "raw" / "user_activity.json"
NORMALIZED_FILE = BASE_DIR / "data" / "normalized" / "user_activity_normalized.json"


def normalize_activity(activity):
    """
    Convert one raw user activity record into a clean,
    consistent format.
    """

    content_id = activity.get("content_id")

    if content_id is not None:
        content_id = str(content_id).strip()

    return {
        "activity_id": str(activity.get("activity_id", "")).strip(),
        "user_id": str(activity.get("user_id", "")).strip(),
        "timestamp": str(activity.get("timestamp", "")).strip(),
        "activity_type": str(
            activity.get("activity_type", "")
        ).strip().lower(),
        "content_id": content_id,
        "duration_seconds": int(
            activity.get("duration_seconds", 0)
        ),
        "device": str(activity.get("device", "")).strip().lower()
    }


def main():
    if not RAW_FILE.exists():
        print(f"Error: Raw file not found: {RAW_FILE}")
        return

    with open(RAW_FILE, "r", encoding="utf-8") as file:
        raw_activities = json.load(file)

    normalized_activities = []

    for activity in raw_activities:
        normalized_activity = normalize_activity(activity)
        normalized_activities.append(normalized_activity)

    NORMALIZED_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(NORMALIZED_FILE, "w", encoding="utf-8") as file:
        json.dump(normalized_activities, file, indent=2)

    print(
        f"Successfully normalized "
        f"{len(normalized_activities)} user activities."
    )

    print(f"Saved to: {NORMALIZED_FILE}")


if __name__ == "__main__":
    main()