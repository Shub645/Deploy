import json
from pathlib import Path

from .response.response_engine import execute_response


# ============================================================
# PROJECT PATH
# ============================================================

APP_DIR = Path(__file__).resolve().parent
PROJECT_DIR = APP_DIR.parent.parent


# ============================================================
# FIND PLAYBOOK FILE AUTOMATICALLY
# ============================================================

def find_playbook_file():

    possible_paths = [
        APP_DIR / "data" / "playbooks" / "attack_playbooks.json",
        APP_DIR / "playbooks" / "attack_playbooks.json",
        PROJECT_DIR / "data" / "playbooks" / "attack_playbooks.json",
        PROJECT_DIR / "playbooks" / "attack_playbooks.json",
    ]

    for path in possible_paths:

        if path.exists() and path.is_file():
            return path

    # Final fallback: search entire project
    try:

        matches = list(
            PROJECT_DIR.rglob("attack_playbooks.json")
        )

        if matches:
            return matches[0]

    except OSError:
        pass

    return None


PLAYBOOK_FILE = find_playbook_file()


# ============================================================
# LOAD PLAYBOOKS
# ============================================================

def load_playbooks():

    if PLAYBOOK_FILE is None:

        print()
        print("ERROR: attack_playbooks.json was not found.")
        print(
            "Search location:",
            PROJECT_DIR
        )

        return []

    try:

        with open(
            PLAYBOOK_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if isinstance(data, list):
            return data

        if isinstance(data, dict):

            if isinstance(
                data.get("playbooks"),
                list
            ):
                return data["playbooks"]

            if isinstance(
                data.get("attack_playbooks"),
                list
            ):
                return data["attack_playbooks"]

            if isinstance(
                data.get("data"),
                list
            ):
                return data["data"]

        print("ERROR: Invalid playbook JSON structure.")

        return []

    except json.JSONDecodeError as error:

        print("ERROR: Invalid JSON:")
        print(error)

        return []

    except OSError as error:

        print("ERROR reading playbook file:")
        print(error)

        return []


# ============================================================
# NORMALIZE
# ============================================================

def normalize(value):

    return (
        str(value)
        .lower()
        .strip()
        .replace("-", "_")
        .replace(" ", "_")
    )


# ============================================================
# RISK CLASSIFICATION
# ============================================================

def classify_risk(event):

    text = json.dumps(event).lower()

    critical_indicators = [

        "attack_chain",
        "attack chain",

        "data_exfiltration",
        "data exfiltration",

        "privilege_escalation",
        "privilege escalation",

        "lateral movement",
        "ransomware",

        "credential theft",
        "credential_theft"
    ]

    high_indicators = [

        "malware",

        "brute force",
        "brute_force",

        "multiple failed login",

        "phishing",

        "credential harvesting"
    ]

    medium_indicators = [

        "endpoint_anomaly",
        "endpoint anomaly",

        "suspicious login",
        "suspicious_login",

        "failed login",

        "unknown process",

        "suspicious activity"
    ]

    for indicator in critical_indicators:

        if indicator in text:
            return "critical"

    for indicator in high_indicators:

        if indicator in text:
            return "high"

    for indicator in medium_indicators:

        if indicator in text:
            return "medium"

    return "low"


# ============================================================
# EVENT TYPE MAPPING
# ============================================================

EVENT_TYPE_MAPPING = {

    "ssh_login_anomaly": "brute_force",

    "phishing_email": "phishing",

    "endpoint_anomaly": "endpoint_anomaly",

    "privilege_escalation": "privilege_escalation",

    "data_exfiltration": "data_exfiltration",

    "attack_chain": "attack_chain",

    "malware_detection": "malware",

    "c2_activity": "command_and_control",

    "account_takeover": "account_compromise"
}


# ============================================================
# FIND PLAYBOOK
# ============================================================

def find_playbook(event):

    playbooks = load_playbooks()

    if not playbooks:
        return None

    event_type = normalize(
        event.get("type", "")
    )

    mapped_type = EVENT_TYPE_MAPPING.get(
        event_type,
        event_type
    )

    event_text = normalize(
        json.dumps(event)
    )

    # --------------------------------------------------------
    # 1. EXACT / MAPPED TYPE MATCH
    # --------------------------------------------------------

    for playbook in playbooks:

        if not isinstance(playbook, dict):
            continue

        playbook_type = normalize(
            playbook.get("type", "")
        )

        if mapped_type == playbook_type:
            return playbook

    # --------------------------------------------------------
    # 2. ATTACK CHAIN EXPLICIT MATCH
    # --------------------------------------------------------

    if event_type == "attack_chain":

        for playbook in playbooks:

            if not isinstance(playbook, dict):
                continue

            if normalize(
                playbook.get("type", "")
            ) == "attack_chain":

                return playbook

    # --------------------------------------------------------
    # 3. NAME MATCH
    # --------------------------------------------------------

    for playbook in playbooks:

        if not isinstance(playbook, dict):
            continue

        name = normalize(
            playbook.get("name", "")
        )

        if name and name in event_text:
            return playbook

    # --------------------------------------------------------
    # 4. KEYWORD MATCH
    # --------------------------------------------------------

    for playbook in playbooks:

        if not isinstance(playbook, dict):
            continue

        keywords = playbook.get(
            "keywords",
            []
        )

        if isinstance(keywords, str):
            keywords = [keywords]

        if isinstance(keywords, list):

            for keyword in keywords:

                keyword_normalized = normalize(
                    keyword
                )

                if (
                    keyword_normalized
                    and keyword_normalized in event_text
                ):
                    return playbook

    # --------------------------------------------------------
    # 5. ATTACK CHAIN STAGE MATCH
    # --------------------------------------------------------

    for playbook in playbooks:

        if not isinstance(playbook, dict):
            continue

        attack_chain = playbook.get(
            "attack_chain",
            []
        )

        if not isinstance(
            attack_chain,
            list
        ):
            continue

        matched_stages = 0

        for stage in attack_chain:

            stage_normalized = normalize(
                stage
            )

            if (
                stage_normalized
                and stage_normalized in event_text
            ):
                matched_stages += 1

        # For a multi-stage attack chain,
        # two or more matching stages indicate correlation.
        if matched_stages >= 2:

            return playbook

    return None


# ============================================================
# SECURITY DECISION
# ============================================================

def get_security_decision(event):

    risk = classify_risk(event)

    playbook = find_playbook(event)

    if playbook:

        risk = normalize(
            playbook.get(
                "risk_tier",
                risk
            )
        )

        action = playbook.get(
            "recommended_action",
            playbook.get(
                "action",
                "Investigate the event and continue monitoring."
            )
        )

        playbook_name = playbook.get(
            "name",
            "Matched Security Playbook"
        )

        human_approval_required = playbook.get(
            "human_approval_required",
            risk in [
                "medium",
                "high",
                "critical"
            ]
        )

    else:

        action = (
            "Investigate the event and continue monitoring."
        )

        playbook_name = "No matching playbook"

        human_approval_required = risk in [
            "medium",
            "high",
            "critical"
        ]

    response = execute_response(

        {
            "risk_tier": risk,

            "recommended_action": action,

            "human_approval_required":
                human_approval_required
        },

        approved=False
    )

    return {

        "event": event,

        "risk_tier": risk,

        "playbook": playbook_name,

        "recommended_action": action,

        "human_approval_required":
            human_approval_required,

        "response": response
    }


# ============================================================
# TEST
# ============================================================

def run_test():

    print()
    print("=" * 70)
    print("        SENTINEL-X PLAYBOOK ENGINE TEST")
    print("=" * 70)
    print()

    print("Using Playbook File:")

    if PLAYBOOK_FILE:

        print(PLAYBOOK_FILE)

    else:

        print("NOT FOUND")

    print()

    playbooks = load_playbooks()

    print(
        "Loaded Playbooks:",
        len(playbooks)
    )

    print()

    events = [

        {
            "type": "ssh_login_anomaly",

            "description":
                "Multiple failed SSH login attempts from 192.168.1.58 followed by a successful login.",

            "source_ip":
                "192.168.1.58",

            "target":
                "server-01"
        },

        {
            "type": "phishing_email",

            "description":
                "Suspicious phishing email containing a credential harvesting link.",

            "sender":
                "external@example.com",

            "target":
                "employee@example.com"
        },

        {
            "type": "endpoint_anomaly",

            "description":
                "Unknown process communicating with a suspicious external destination.",

            "endpoint":
                "WIN-001",

            "destination":
                "185.10.20.15"
        },

        {
            "type": "privilege_escalation",

            "description":
                "Suspicious process attempting privilege escalation."
        },

        {
            "type": "data_exfiltration",

            "description":
                "Large amount of sensitive data sent to an external destination."
        },

        {
            "type": "attack_chain",

            "description":
                "Phishing followed by suspicious login, endpoint anomaly, privilege escalation and data exfiltration."
        }
    ]

    for event in events:

        result = get_security_decision(
            event
        )

        print(
            "Event:",
            result["event"]
        )

        print(
            "Risk Tier:",
            result["risk_tier"]
        )

        print(
            "Playbook:",
            result["playbook"]
        )

        print(
            "Recommended Action:",
            result["recommended_action"]
        )

        print(
            "Human Approval Required:",
            result["human_approval_required"]
        )

        response = result.get(
            "response"
        )

        if isinstance(
            response,
            dict
        ):

            print(
                "Response Status:",
                response.get(
                    "status",
                    "unknown"
                )
            )

        else:

            print(
                "Response Status:",
                response
            )

        print("-" * 70)

    print()
    print("=" * 70)
    print("PLAYBOOK ENGINE TEST COMPLETED")
    print("=" * 70)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    run_test()