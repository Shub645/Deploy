"""
SENTINEL-X
AI-Powered Human-Governed Autonomous SOC

Final orchestration layer connecting:

1. Attack Chain Engine
2. Playbook Engine
3. LLM Engine
4. Response Engine
"""

import sys
import json
from pathlib import Path


# ============================================================
# PATH SETUP
# ============================================================

APP_DIR = Path(__file__).resolve().parent

if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))


# ============================================================
# IMPORTS
# ============================================================

from attack_chain_engine import correlate_events
from core.llm_engine import analyze_security_event
from response.response_engine import (
    execute_response,
    approve_response
)


# ============================================================
# LOAD PLAYBOOK ENGINE
# ============================================================

def load_playbook_engine():

    playbook_file = APP_DIR / "playbook_engine.py"

    source = playbook_file.read_text(
        encoding="utf-8"
    )

    # Convert the relative import used by playbook_engine
    # into an absolute import for direct execution.

    source = source.replace(
        "from .response.response_engine import execute_response",
        "from response.response_engine import execute_response"
    )

    namespace = {
        "__name__": "sentinel_playbook_engine",
        "__file__": str(playbook_file)
    }

    exec(
        compile(
            source,
            str(playbook_file),
            "exec"
        ),
        namespace
    )

    return namespace["get_security_decision"]


get_security_decision = load_playbook_engine()


# ============================================================
# SENTINEL-X ORCHESTRATOR
# ============================================================

class SentinelX:

    def __init__(self):

        self.name = "SENTINEL-X"

        self.version = "1.0"


    # ========================================================
    # COMPLETE SECURITY ANALYSIS
    # ========================================================

    def analyze(self, events):

        if not isinstance(events, list):

            events = [events]

        if not events:

            return {
                "status": "error",
                "message": "No security events supplied."
            }


        # ====================================================
        # STEP 1 — ATTACK CHAIN CORRELATION
        # ====================================================

        attack_chain = correlate_events(
            events
        )


        # ====================================================
        # STEP 2 — CREATE CORRELATED EVENT
        # ====================================================

        if (
            attack_chain.get("status")
            == "attack_chain_detected"
        ):

            event = {

                "type": "attack_chain",

                "description":
                    "Correlated multi-stage attack: "
                    + " -> ".join(
                        attack_chain.get(
                            "attack_chain",
                            []
                        )
                    ),

                "scenario":
                    attack_chain.get(
                        "scenario"
                    ),

                "mitre_attack":
                    attack_chain.get(
                        "mitre_attack"
                    )
            }

        else:

            event = events[-1]


        # ====================================================
        # STEP 3 — PLAYBOOK ENGINE
        # ====================================================

        playbook = get_security_decision(
            event
        )


        # ====================================================
        # STEP 4 — LLM SECURITY ANALYSIS
        # ====================================================

        llm_input = {

            "events": events,

            "attack_chain":
                attack_chain,

            "playbook":
                playbook
        }

        try:

            llm_result = analyze_security_event(

                json.dumps(
                    llm_input,
                    indent=2
                )

            )

        except Exception as error:

            llm_result = (
                "LLM analysis unavailable: "
                + str(error)
            )


        # ====================================================
        # STEP 5 — FINAL SECURITY DECISION
        # ====================================================

        risk_tier = playbook.get(
            "risk_tier",
            attack_chain.get(
                "risk_tier",
                "low"
            )
        )

        recommended_action = playbook.get(
            "recommended_action",
            attack_chain.get(
                "recommended_action",
                "Continue monitoring."
            )
        )

        human_approval_required = playbook.get(
            "human_approval_required",
            risk_tier in [
                "medium",
                "high",
                "critical"
            ]
        )


        decision = {

            "risk_tier":
                risk_tier,

            "recommended_action":
                recommended_action,

            "human_approval_required":
                human_approval_required,

            "playbook":
                playbook.get(
                    "playbook"
                ),

            "attack_chain":
                attack_chain.get(
                    "scenario"
                )
        }


        # ====================================================
        # STEP 6 — RESPONSE ENGINE
        # ====================================================

        response = execute_response(

            decision,

            approved=False

        )


        # ====================================================
        # FINAL RESULT
        # ====================================================

        return {

            "system":
                self.name,

            "version":
                self.version,

            "status":
                "analysis_completed",

            "events":
                events,

            "attack_chain":
                attack_chain,

            "playbook":
                playbook,

            "llm_analysis":
                llm_result,

            "decision":
                decision,

            "response":
                response
        }


# ============================================================
# DEMO
# ============================================================

def run_demo():

    print()

    print("=" * 75)

    print(
        "             SENTINEL-X AUTONOMOUS SOC"
    )

    print("=" * 75)

    print()

    print(
        "AI-Powered Human-Governed Autonomous Security Operations"
    )

    print()


    # ========================================================
    # ATTACK SIMULATION
    # ========================================================

    events = [

        {
            "type": "phishing_email",

            "description":
                "Suspicious phishing email containing "
                "a credential harvesting link.",

            "sender":
                "attacker@example.com",

            "target":
                "employee@example.com"
        },


        {
            "type": "suspicious_login",

            "description":
                "Login detected from an unusual "
                "location and device.",

            "user":
                "employee@example.com",

            "source_ip":
                "185.10.20.15"
        },


        {
            "type": "endpoint_anomaly",

            "description":
                "Unknown process communicating with "
                "a suspicious external destination.",

            "endpoint":
                "WIN-001",

            "destination":
                "185.10.20.15"
        },


        {
            "type": "privilege_escalation",

            "description":
                "Suspicious process attempting "
                "privilege escalation.",

            "endpoint":
                "WIN-001"
        },


        {
            "type": "data_exfiltration",

            "description":
                "Large amount of sensitive data sent "
                "to an external destination.",

            "endpoint":
                "WIN-001",

            "destination":
                "185.10.20.15"
        }

    ]


    # ========================================================
    # START SENTINEL-X
    # ========================================================

    sentinel = SentinelX()

    result = sentinel.analyze(
        events
    )


    # ========================================================
    # ATTACK CHAIN OUTPUT
    # ========================================================

    print()

    print("=" * 75)

    print(
        "1. ATTACK CHAIN CORRELATION"
    )

    print("=" * 75)

    chain = result[
        "attack_chain"
    ]

    print(
        "Status:",
        chain.get(
            "status"
        )
    )

    print(
        "Scenario:",
        chain.get(
            "scenario"
        )
    )

    print(
        "Risk:",
        chain.get(
            "risk_tier"
        )
    )

    print(
        "Chain:",
        " -> ".join(
            chain.get(
                "attack_chain",
                []
            )
        )
    )

    print(
        "MITRE ATT&CK:",
        chain.get(
            "mitre_attack"
        )
    )


    # ========================================================
    # PLAYBOOK OUTPUT
    # ========================================================

    print()

    print("=" * 75)

    print(
        "2. SECURITY PLAYBOOK"
    )

    print("=" * 75)

    playbook = result[
        "playbook"
    ]

    print(
        "Playbook:",
        playbook.get(
            "playbook"
        )
    )

    print(
        "Risk Tier:",
        playbook.get(
            "risk_tier"
        )
    )

    print(
        "Recommended Action:",
        playbook.get(
            "recommended_action"
        )
    )

    print(
        "Human Approval:",
        playbook.get(
            "human_approval_required"
        )
    )


    # ========================================================
    # LLM OUTPUT
    # ========================================================

    print()

    print("=" * 75)

    print(
        "3. AI SECURITY ANALYSIS"
    )

    print("=" * 75)

    print(
        result[
            "llm_analysis"
        ]
    )


    # ========================================================
    # RESPONSE ENGINE
    # ========================================================

    print()

    print("=" * 75)

    print(
        "4. RESPONSE ENGINE"
    )

    print("=" * 75)

    response = result[
        "response"
    ]

    print(
        "Status:",
        response.get(
            "status"
        )
    )

    print(
        "Message:",
        response.get(
            "message"
        )
    )

    print(
        "Risk Tier:",
        response.get(
            "risk_tier"
        )
    )

    print(
        "Human Approval Required:",
        response.get(
            "human_approval_required"
        )
    )


    # ========================================================
    # HUMAN APPROVAL
    # ========================================================

    if (
        response.get(
            "status"
        )
        == "pending_approval"
    ):

        print()

        print("=" * 75)

        print(
            "5. HUMAN APPROVAL"
        )

        print("=" * 75)

        print(
            "Human approval required before containment."
        )

        approved = approve_response(
            result[
                "decision"
            ]
        )

        print(
            "Approved Status:",
            approved.get(
                "status"
            )
        )

        print(
            "Approved:",
            approved.get(
                "approved"
            )
        )


    # ========================================================
    # COMPLETE
    # ========================================================

    print()

    print("=" * 75)

    print(
        "             SENTINEL-X DEMO COMPLETED"
    )

    print("=" * 75)

    print()


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    run_demo()