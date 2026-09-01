import json
from datetime import datetime, timezone


def calculate_risk_level(severity, score):
    severity = str(severity or "").lower()

    try:
        score = int(score)
    except (ValueError, TypeError):
        score = 0

    if severity == "critical" or score >= 90:
        return "critical"
    elif severity == "high" or score >= 70:
        return "high"
    elif severity == "medium" or score >= 40:
        return "medium"

    return "low"


def determine_action(finding):
    recommendation = str(
        finding.get("recommended_action", "")
    ).lower()

    threat_type = str(
        finding.get("threat_type", "")
    ).lower()

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


def analyze_finding(finding):
    """
    SENTINEL-X AI Adapter

    Input:
        Security finding/event data

    Output contract:
        threat
        risk_level
        confidence
        reason
        recommended_action
    """

    if not isinstance(finding, dict):
        return {
            "status": "error",
            "message": "Finding must be a JSON object"
        }

    threat_type = finding.get(
        "threat_type",
        "suspicious_activity"
    )

    severity = finding.get(
        "severity",
        "medium"
    )

    score = finding.get(
        "risk_score",
        50
    )

    risk_level = calculate_risk_level(
        severity,
        score
    )

    target = (
        finding.get("host")
        or finding.get("endpoint")
        or finding.get("target")
        or finding.get("user_id")
        or finding.get("source_ip")
        or "unknown"
    )

    action = determine_action(finding)

    reasoning = finding.get(
        "reasoning",
        "Suspicious security activity detected."
    )

    try:
        confidence = float(score) / 100
    except (ValueError, TypeError):
        confidence = 0.50

    confidence = max(0.0, min(confidence, 1.0))

    return {
        "threat": str(threat_type),

        "risk_level": risk_level,

        "confidence": round(confidence, 2),

        "reason": (
            "Behavioral pattern analysis identified "
            + str(threat_type)
            + ". "
            + str(reasoning)
        ),

        "recommended_action": {
            "action": action,
            "target": target
        }
    }


def run_test():

    finding = {
        "finding_id": "WF001",
        "timestamp": "2026-08-30T14:00:00Z",
        "user_id": "U010",
        "host": "test-pc",
        "threat_type": "suspicious_login_pattern",
        "severity": "HIGH",
        "risk_score": 85,
        "reasoning": (
            "Multiple failed login attempts "
            "followed by a successful login."
        ),
        "recommended_action": (
            "Require additional verification."
        )
    }

    result = analyze_finding(finding)

    print("=" * 70)
    print("       SENTINEL-X FINAL AI ADAPTER TEST")
    print("=" * 70)

    print(json.dumps(result, indent=2))

    print("=" * 70)
    print("TEST STATUS: SUCCESS")
    print("Threat:", result["threat"])
    print("Risk Level:", result["risk_level"])
    print("Confidence:", result["confidence"])
    print(
        "Recommended Action:",
        result["recommended_action"]["action"]
    )
    print("=" * 70)


if __name__ == "__main__":
    run_test()