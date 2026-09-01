"""
SENTINEL-X Attack Chain Engine

Correlates security events into known attack scenarios.
"""

from datetime import datetime


# ============================================================
# TIMESTAMP
# ============================================================

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ============================================================
# ATTACK SCENARIOS
# ============================================================

ATTACK_SCENARIOS = [

    {
        "id": "SC-001",
        "name": "Phishing to Account Compromise",
        "chain": [
            "phishing_email",
            "credential_theft",
            "suspicious_login",
            "account_compromise"
        ],
        "mitre": [
            "T1566.002",
            "T1078"
        ],
        "risk_tier": "high",
        "reason": (
            "A phishing attempt can lead to credential theft. "
            "If the stolen credentials are subsequently used "
            "for an unusual login, the events should be correlated "
            "as a potential account-compromise chain."
        ),
        "recommended_action": (
            "Alert the SOC analyst. Investigate the phishing "
            "indicator and login activity. Temporarily restrict "
            "the affected account if compromise is confirmed. "
            "Require human approval before containment actions."
        ),
        "human_approval_required": True
    },

    {
        "id": "SC-002",
        "name": "SSH Brute Force to Account Access",
        "chain": [
            "failed_ssh_login",
            "successful_ssh_login",
            "suspicious_account_activity"
        ],
        "mitre": [
            "T1110",
            "T1078"
        ],
        "risk_tier": "high",
        "reason": (
            "Repeated authentication failures followed by "
            "a successful login may indicate password guessing "
            "or credential compromise."
        ),
        "recommended_action": (
            "Investigate the source IP and authentication logs. "
            "Rate-limit or temporarily block suspicious "
            "authentication attempts. Review the affected account. "
            "Require human approval before blocking or isolating systems."
        ),
        "human_approval_required": True
    },

    {
        "id": "SC-003",
        "name": "Endpoint Command and Control",
        "chain": [
            "suspicious_endpoint_process",
            "external_communication",
            "command_and_control",
            "potential_data_transfer"
        ],
        "mitre": [
            "T1059",
            "T1071"
        ],
        "risk_tier": "high",
        "reason": (
            "The combination of suspicious process execution "
            "and unexpected external communication may indicate "
            "command-and-control activity."
        ),
        "recommended_action": (
            "Investigate the process and destination. Preserve "
            "relevant endpoint and network evidence. Isolate "
            "the endpoint only after human approval. Continue "
            "monitoring related activity."
        ),
        "human_approval_required": True
    }
]


# ============================================================
# EVENT NORMALIZATION
# ============================================================

def normalize_event_type(event_type):

    value = str(event_type).lower().strip()

    mapping = {

        "phishing": "phishing_email",
        "phishing_email": "phishing_email",

        "credential theft": "credential_theft",
        "credential_theft": "credential_theft",

        "suspicious login": "suspicious_login",
        "suspicious_login": "suspicious_login",

        "account compromise": "account_compromise",
        "account_compromise": "account_compromise",

        "failed login": "failed_ssh_login",
        "failed_login": "failed_ssh_login",
        "failed_ssh_login": "failed_ssh_login",
        "ssh_failed_login": "failed_ssh_login",

        "successful login": "successful_ssh_login",
        "successful_login": "successful_ssh_login",
        "successful_ssh_login": "successful_ssh_login",

        "suspicious account activity":
            "suspicious_account_activity",

        "suspicious_account_activity":
            "suspicious_account_activity",

        "endpoint anomaly":
            "suspicious_endpoint_process",

        "endpoint_anomaly":
            "suspicious_endpoint_process",

        "suspicious endpoint process":
            "suspicious_endpoint_process",

        "suspicious_endpoint_process":
            "suspicious_endpoint_process",

        "external communication":
            "external_communication",

        "external_communication":
            "external_communication",

        "suspicious network connection":
            "external_communication",

        "suspicious_network_connection":
            "external_communication",

        "command and control":
            "command_and_control",

        "command_and_control":
            "command_and_control",

        "c2_activity":
            "command_and_control",

        "potential data transfer":
            "potential_data_transfer",

        "potential_data_transfer":
            "potential_data_transfer"
    }

    return mapping.get(value, value)


# ============================================================
# MATCH ATTACK SCENARIO
# ============================================================

def match_scenario(events):

    if not isinstance(events, list):
        return None

    normalized_events = []

    for event in events:

        if not isinstance(event, dict):
            continue

        event_type = normalize_event_type(
            event.get("type", "")
        )

        normalized_events.append(event_type)

    for scenario in ATTACK_SCENARIOS:

        chain = scenario["chain"]
        position = 0

        for event_type in normalized_events:

            if position >= len(chain):
                break

            if event_type == chain[position]:
                position += 1

        if position == len(chain):
            return scenario

    return None


# ============================================================
# CORRELATE EVENTS
# ============================================================

def correlate_events(events):

    scenario = match_scenario(events)

    if scenario is None:

        return {
            "status": "no_attack_chain",
            "scenario": None,
            "risk_tier": "low",
            "reason": "No known attack scenario matched.",
            "recommended_action":
                "Continue monitoring the events.",
            "human_approval_required": False,
            "timestamp": get_timestamp()
        }

    return {
        "status": "attack_chain_detected",
        "scenario_id": scenario["id"],
        "scenario": scenario["name"],
        "attack_chain": scenario["chain"],
        "mitre_attack": scenario["mitre"],
        "risk_tier": scenario["risk_tier"],
        "reason": scenario["reason"],
        "recommended_action":
            scenario["recommended_action"],
        "human_approval_required":
            scenario["human_approval_required"],
        "timestamp": get_timestamp()
    }


# ============================================================
# TEST
# ============================================================

def run_test():

    print()
    print("=" * 70)
    print("        SENTINEL-X ATTACK CHAIN ENGINE TEST")
    print("=" * 70)

    # --------------------------------------------------------
    # TEST 1
    # --------------------------------------------------------

    print()
    print("[TEST 1] PHISHING -> ACCOUNT COMPROMISE")

    events_1 = [
        {"type": "phishing_email"},
        {"type": "credential_theft"},
        {"type": "suspicious_login"},
        {"type": "account_compromise"}
    ]

    print(correlate_events(events_1))

    # --------------------------------------------------------
    # TEST 2
    # --------------------------------------------------------

    print()
    print("[TEST 2] SSH BRUTE FORCE -> ACCOUNT ACCESS")

    events_2 = [
        {"type": "failed_ssh_login"},
        {"type": "successful_ssh_login"},
        {"type": "suspicious_account_activity"}
    ]

    print(correlate_events(events_2))

    # --------------------------------------------------------
    # TEST 3
    # --------------------------------------------------------

    print()
    print("[TEST 3] ENDPOINT -> COMMAND AND CONTROL")

    events_3 = [
        {"type": "suspicious_endpoint_process"},
        {"type": "external_communication"},
        {"type": "command_and_control"},
        {"type": "potential_data_transfer"}
    ]

    print(correlate_events(events_3))

    # --------------------------------------------------------
    # TEST 4
    # --------------------------------------------------------

    print()
    print("[TEST 4] NORMAL EVENT")

    events_4 = [
        {"type": "normal_login"}
    ]

    print(correlate_events(events_4))

    print()
    print("=" * 70)
    print("ATTACK CHAIN ENGINE TEST COMPLETED")
    print("=" * 70)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    run_test()