import json
from pathlib import Path


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Input and output files
RAW_FILE = BASE_DIR / "data" / "raw" / "login_events.json"
NORMALIZED_FILE = BASE_DIR / "data" / "normalized" / "login_events_normalized.json"


def normalize_event(event):
    """
    Convert one raw login event into a clean, consistent format.
    """

    return {
        "event_id": str(event.get("event_id", "")).strip(),
        "user_id": str(event.get("user_id", "")).strip(),
        "timestamp": str(event.get("timestamp", "")).strip(),
        "ip_address": str(event.get("ip_address", "")).strip(),
        "login_status": str(event.get("login_status", "")).strip().lower(),
        "device": str(event.get("device", "")).strip(),
        "location": str(event.get("location", "")).strip()
    }


def main():
    # Check that the raw file exists
    if not RAW_FILE.exists():
        print(f"Error: Raw file not found: {RAW_FILE}")
        return

    # Read raw login events
    with open(RAW_FILE, "r", encoding="utf-8") as file:
        raw_events = json.load(file)

    # Normalize all events
    normalized_events = []

    for event in raw_events:
        normalized_event = normalize_event(event)
        normalized_events.append(normalized_event)

    # Make sure the normalized directory exists
    NORMALIZED_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Save normalized data
    with open(NORMALIZED_FILE, "w", encoding="utf-8") as file:
        json.dump(normalized_events, file, indent=2)

    print(f"Successfully normalized {len(normalized_events)} login events.")
    print(f"Saved to: {NORMALIZED_FILE}")


if __name__ == "__main__":
    main()