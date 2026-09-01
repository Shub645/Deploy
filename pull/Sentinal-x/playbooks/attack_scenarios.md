"""
SENTINEL-X Attack Chain Engine

Correlates related security events into known attack scenarios.

Supported scenarios:
1. Phishing to Account Compromise
2. SSH Brute Force to Account Access
3. Endpoint Command and Control

Human approval is required for all scenarios.
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

        "reason":
            "A phishing attempt can lead to credential theft. "
            "If the stolen credentials are subsequently used "
            "for an unusual login, the events should be correlated "
            "as a potential account-compromise chain.",

        "recommended_action":
            "Alert the SOC analyst. Investigate the phishing "
            "indicator and login activity. Temporarily restrict "
            "the affected account if compromise is confirmed. "
            "Require human approval before containment actions.",

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

        "reason":
            "Repeated authentication failures followed by "
            "a successful login may indicate password guessing "
            "or credential compromise.",

        "recommended_action":
            "Investigate the source IP and authentication logs. "
            "Rate-limit or temporarily block suspicious "
            "authentication attempts. Review the affected account. "
            "Require human approval before blocking or isolating systems.",

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

        "reason":
            "The combination of suspicious process execution "
            "and unexpected external communication may indicate "
            "command-and-control activity.",

        "recommended_action":
            "Investigate the process and destination. Preserve "
            "relevant endpoint and network evidence. Isolate "
            "the endpoint only after human approval. Continue "
            "monitoring related activity.",

        "human_approval_required": True
    }
]


# ============================================================
# EVENT NORMALIZATION
# ============================================================

def normalize_event_type(event_type):

    value = str(event_type).lower().strip()

    mapping = {

        # Scenario 1
        "phishing_email": "phishing_email",
        "phishing": "phishing_email",

        "credential_theft": "credential_theft",
        "credential theft": "credential_theft",

        "suspicious_login": "suspicious_login",
        "suspicious login": "suspicious_login",

        "account_compromise": "account_compromise",
        "account compromise": "account_compromise",

        # Scenario 2
        "failed_ssh_login": "failed_ssh_login",
        "failed_login": "failed_ssh_login",
        "ssh_failed_login": "failed_ssh_login",

        "successful_ssh_login": "successful_ssh_login",
        "ssh_successful_login": "successful_ssh_login",

        "suspicious_account_activity":
            "suspicious_account_activity",

        # Scenario 3
        "suspicious_endpoint_process":
            "suspicious_endpoint_process",

        "endpoint_anomaly":
            "suspicious_endpoint_process",

        "external_communication":
            "external_communication",

        "suspicious_network_connection":
            "external_communication",

        "command_and_control":
            "command_and_control",

        "c2_activity":
            "command_and_control",

        "potential_data_transfer":
            "potential_data_transfer"
    }

    return mapping.get(
        value,
        value
    )


# ============================================================
# MATCH SCENARIO
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

        normalized_events.append(
            event_type
        )

    # --------------------------------------------------------
    # CHECK EACH SCENARIO
    # --------------------------------------------------------

    for scenario in ATTACK_SCENARIOS:

        chain = scenario["chain"]

        position = 0

        for event_type in normalized_events:

            if position >= len(chain):
                break

            if event_type == chain[position]:

                position += 1

        # Complete ordered chain detected
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

        "scenario_id":
            scenario["id"],

        "scenario":
            scenario["name"],

        "attack_chain":
            scenario["chain"],

        "mitre_attack":
            scenario["mitre"],

        "risk_tier":
            scenario["risk_tier"],

        "reason":
            scenario["reason"],

        "recommended_action":
            scenario["recommended_action"],

        "human_approval_required":
            scenario["human_approval_required"],

        "timestamp":
            get_timestamp()
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
    print("[TEST 1] PHISHING → ACCOUNT COMPROMISE")

    events_1 = [

        {
            "type": "phishing_email"
        },

        {
            "type": "credential_theft"
        },

        {
            "type": "suspicious_login"
        },

        {
            "type": "account_compromise"
        }
    ]

    result = correlate_events(events_1)

    print(result)

    # --------------------------------------------------------
    # TEST 2
    # --------------------------------------------------------

    print()
    print("[TEST 2] SSH BRUTE FORCE