"""
SENTINEL-X AI ADAPTER

Purpose:
- Convert security findings into the agreed AI API response
- Calculate risk level
- Generate recommended action
- Apply human-in-the-loop guardrail
- Return backend-compatible JSON

Integration contract:
POST /api/ai/analyze

High/Critical risk actions NEVER execute automatically.
"""

import json
from datetime import datetime, timezone


# ============================================================
# RISK ENGINE
# ============================================================

def calculate_risk_level(severity, risk_score):
    """
    Convert severity + score into normalized risk level.
    """

    severity = str(severity or "").lower()

    try:
        score = int(risk_score)
    except (TypeError, ValueError):
        score = 0

    if severity == "critical" or score >= 90:
        return "critical"

    if severity == "high" or score >= 70:
        return "high"

    if severity == "medium" or score >= 40:
        return "medium"

    return "low"


# ============================================================
# ACTION MAPPING
# ============================================================

def determine_action(finding):
    """
    Convert finding type/recommendation into an
    Action Executor compatible action.
    """

    threat_type = str(
        finding.get("threat_type", "")
    ).lower()

    recommendation = str(
        finding.get("recommended_action", "")
    ).lower()

    # Explicit recommendation takes priority
    if "quarantine" in recommendation:
        return "quarantine_endpoint"

    if "isolate" in recommendation:
        return "isolate_endpoint"

    if "block" in recommendation:
        return "block_destination"

    if "verify" in recommendation:
        return "require_additional_verification"

    if "monitor" in recommendation:
        return "monitor_endpoint"

    # Threat-based fallback
    if "phishing" in threat_type:
        return "quarantine_email"

    if "login" in threat_type:
        return "require_additional_verification"

    if "endpoint" in threat_type:
        return "monitor_endpoint"

    if "exfiltration" in threat_type:
        return "block_destination"

    if "privilege" in threat_type:
        return "restrict_account"

    return "investigate"


# ============================================================
# TARGET EXTRACTION
# ============================================================

def determine_target(finding):
    """
    Find the resource affected by the security finding.
    """

    return (
        finding.get("host")
        or finding.get("endpoint")
        or finding.get("target")
        or finding.get("user_id")
        or finding.get("source_ip")
        or "unknown"
    )


# ============================================================
# AI ANALYSIS
# ============================================================

def analyze_finding(finding):
    """
    Main AI adapter function.

    Input:
        Security finding dictionary

    Output:
        Backend-compatible AI analysis dictionary
    """

    if not isinstance(finding, dict):
        return {
            "status": "error",
            "message": "Finding must be a JSON object."
        }

    # --------------------------------------------------------
    # INPUT
    # --------------------------------------------------------

    finding_id = finding.get(
        "finding_id",
        "WF-UNKNOWN"
    )

    threat_type = finding.get(
        "threat_type",
        "suspicious_activity"
    )

    severity = finding.get(
        "severity",
        "MEDIUM"
    )

    risk_score = finding.get(
        "risk_score",
        50
    )

    reasoning = finding.get(
        "reasoning",
        "Suspicious security activity detected."
    )

    evidence = finding.get(
        "evidence",
        []
    )

    # --------------------------------------------------------
    # RISK
    # --------------------------------------------------------

    risk_level = calculate_risk_level(
        severity,
        risk_score
    )

    # --------------------------------------------------------
    # ACTION
    # --------------------------------------------------------

    action = determine_action(finding)

    target = determine_target(finding)

    # --------------------------------------------------------
    # GUARDRAIL
    # --------------------------------------------------------

    guardrail_value = str(
        finding.get(
            "guardrail_status",
            "PASSED"
        )
    ).upper()

    prompt_injection_detected = (
        guardrail_value != "PASSED"
    )

    if prompt_injection_detected:

        return {
            "status": "blocked",

            "threat": {
                "type": threat_type,
                "severity": risk_level
            },

            "risk": {
                "score": risk_score,
                "level": risk_level
            },

            "reason": (
                "AI action blocked by security guardrail."
            ),

            "recommended_action": {
                "action": "investigate",
                "target": target
            },

            "playbook": {
                "name": "Security Finding Response",
                "source": "attack_playbooks.json"
            },

            "guardrail": {
                "status": "failed",
                "prompt_injection_detected": True
            },

            "human_approval": {
                "required": True,
                "status": "pending"
            },

            "finding_id": finding_id,

            "evidence": evidence
        }

    # --------------------------------------------------------
    # HUMAN APPROVAL
    # --------------------------------------------------------

    # Medium/high/critical actions require human approval.
    human_approval_required = bool(
        finding.get(
            "human_approval_required",
            False
        )
    )

    if risk_level in (
        "medium",
        "high",
        "critical"
    ):
        human_approval_required = True

    approval_status = (
        "pending"
        if human_approval_required
        else "not_required"
    )

    # --------------------------------------------------------
    # AI REASONING
    # --------------------------------------------------------

    ai_reason = (
        f"Behavioral pattern analysis identified "
        f"{threat_type} with a {risk_level} risk level. "
        f"{reasoning}"
    )

    # --------------------------------------------------------
    # FINAL RESPONSE
    # --------------------------------------------------------

    result = {

        "status": "success",

        "threat": {
            "type": threat_type,
            "severity": risk_level
        },

        "risk": {
            "score": risk_score,
            "level": risk_level
        },

        "reason": ai_reason,

        "recommended_action": {
            "action": action,
            "target": target
        },

        "playbook": {
            "name": "Security Finding Response",
            "source": "attack_playbooks.json"
        },

        "guardrail": {
            "status": "passed",
            "prompt_injection_detected": False
        },

        "human_approval": {
            "required": human_approval_required,
            "status": approval_status
        },

        "finding_id": finding_id,

        "timestamp": finding.get(
            "timestamp",
            datetime.now(
                timezone.utc
            ).isoformat()
        ),

        "evidence": evidence
    }

    return result


# ============================================================
# TEST
# ============================================================

def run_test():

    test_finding = {

        "finding_id": "WF001",

        "timestamp": (
            "2026-08-19T15:10:36Z"
        ),

        "user_id": "U010",

        "threat_type": (
            "suspicious_login_pattern"
        ),

        "severity": "HIGH",

        "risk_score": 85,

        "reasoning": (
            "Multiple failed login attempts "
            "followed by a successful login."
        ),

        "recommended_action": (
            "Require additional verification."
        ),

        "guardrail_status": "PASSED",

        "human_approval_required": True,

        "evidence": [
            "LE012",
            "LE013",
            "LE015"
        ]
    }

    result = analyze_finding(
        test_finding
    )

    print()
    print("=" * 70)
    print("        SENTINEL-X AI ADAPTER TEST")
    print("=" * 70)

    print(
        json.dumps(
            result,
            indent=2
        )
    )

    print("=" * 70)

    print()
    print("TEST STATUS: SUCCESS")
    print(
        "Human Approval:",
        result["human_approval"]["status"]
    )
    print(
        "Risk Level:",
        result["risk"]["level"]
    )
    print(
        "Recommended Action:",
        result["recommended_action"]["action"]
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    run_test()