"""
Review classification on recent Gmail messages for human validation.
Usage: python scripts/review_phase4.py [--limit N] [--apply-feedback] [--headless] [--no-auto-verify]
"""
import subprocess
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple

try:
    import requests
except ImportError:
    print("Missing dependency: requests")
    print("Install with: pip install requests")
    sys.exit(1)

REPO = Path(r"I:\Dev Applications\personal_mail")
FEEDBACK_PATH = REPO / "reports" / "classification_feedback.json"
AUTO_VERIFY_SCRIPT = REPO / "scripts" / "auto_verify_phase4.py"


def load_token() -> str:
    token_file = Path(r"C:\Users\SMAD Inc\AppData\Local\personal_mail\google_oauth\token.json")
    if not token_file.exists():
        raise FileNotFoundError(f"Token file missing: {token_file}")
    data = json.loads(token_file.read_text())
    token = data.get("access_token")
    if not token:
        raise ValueError("No access_token in token file")
    return token


def gmail_get(token: str, url: str) -> dict:
    resp = requests.get(
        url,
        headers={"Authorization": f"Bearer {token}"},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def fetch_recent_messages(token: str, limit: int = 5) -> List[dict]:
    data = gmail_get(
        token,
        f"https://gmail.googleapis.com/gmail/v1/users/me/messages?maxResults={limit}",
    )
    message_refs = data.get("messages", [])
    messages = []
    for ref in message_refs:
        msg_id = ref["id"]
        msg_data = gmail_get(
            token,
            f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{msg_id}?format=metadata",
        )
        headers = {
            h["name"]: h["value"]
            for h in msg_data.get("payload", {}).get("headers", [])
        }
        messages.append({
            "id": msg_id,
            "subject": headers.get("Subject", ""),
            "from": headers.get("From", ""),
            "snippet": msg_data.get("snippet", ""),
        })
    return messages


def load_feedback() -> Dict[str, str]:
    if FEEDBACK_PATH.exists():
        return json.loads(FEEDBACK_PATH.read_text())
    return {}


def save_feedback(feedback: Dict[str, str]) -> None:
    FEEDBACK_PATH.parent.mkdir(parents=True, exist_ok=True)
    FEEDBACK_PATH.write_text(json.dumps(feedback, indent=2, ensure_ascii=False))


def classify_message(msg: dict, feedback: Dict[str, str]) -> Tuple[str, int]:
    """Simple scoring based on keywords and feedback overrides."""
    if msg["id"] in feedback:
        return feedback[msg["id"]], 100

    text = f"{msg['subject']} {msg['from']} {msg['snippet']}".lower()

    from_lower = msg.get("from", "").lower()
    subject_lower = msg.get("subject", "").lower()

    # Google security alerts (priority)
    google_senders = [
        "no-reply@accounts.google.com",
        "mail-noreply@google.com",
        "google.com",
    ]
    if any(s in from_lower for s in google_senders) or "alerte de sécurité" in subject_lower:
        return "GOOGLE_SECURITY", 95

    # Banking keywords
    if any(k in text for k in ["banque", "bank", "compte", "account", "virement", "transfer", "carte", "card"]):
        return "BANQUE", 80

    # Insurance keywords
    if any(k in text for k in ["assurance", "insurance", "mutuelle", "contrat", "policy"]):
        return "ASSURANCE", 75

    # Energy keywords
    if any(k in text for k in ["edf", "engie", "total", " énergie", "energy", "gaz", "électricité", "electricity"]):
        return "ÉNERGIE", 75

    # Revenue keywords
    if any(k in text for k in ["paie", "salary", "revenu", "income", "bulletin"]):
        return "REVENUS", 80

    # Shopping keywords
    if any(k in text for k in ["amazon", "commande", "order", "achat", "purchase"]):
        return "ACHATS", 70

    return "<none>", 0


def review_messages(limit: int = 5, apply_feedback: bool = False, headless: bool = False) -> None:
    token = load_token()
    messages = fetch_recent_messages(token, limit)
    feedback = load_feedback() if apply_feedback else {}

    print(f"\n=== Phase 4 classification review ({len(messages)} messages) ===\n")

    corrections: Dict[str, str] = {}
    for msg in messages:
        proposed, confidence = classify_message(msg, feedback)
        print(f"Subject: {msg['subject']}")
        print(f"From: {msg['from']}")
        print(f"Snippet: {msg['snippet'][:100]}...")
        print(f"Proposed class: {proposed} (confidence: {confidence}%)")

        if apply_feedback and msg["id"] in feedback:
            print(f"[CORRECTED] -> {feedback[msg['id']]}")
            print("-" * 40)
            continue

        if headless:
            print("[headless] skipped interactive correction")
            print("-" * 40)
            continue

        response = input("Correct? (Enter=accept, or type new label): ").strip()
        if response:
            corrections[msg["id"]] = response
            print(f"  -> saved correction: {response}")
        else:
            print("  -> accepted")
        print("-" * 40)

    if corrections:
        feedback.update(corrections)
        save_feedback(feedback)
        print(f"\nFeedback saved to: {FEEDBACK_PATH}")
        print(f"Total corrections: {len(corrections)}")
    else:
        print("\nNo corrections made.")


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Review Phase 4 classification")
    parser.add_argument("--limit", type=int, default=5, help="Number of messages to review")
    parser.add_argument("--apply-feedback", action="store_true", help="Apply saved feedback corrections")
    parser.add_argument("--headless", action="store_true", help="Skip interactive input (CI/non-interactive)")
    parser.add_argument("--no-auto-verify", action="store_true", help="Do not run auto verification after review")
    args = parser.parse_args()

    try:
        review_messages(args.limit, args.apply_feedback, args.headless)
        
        # Auto-verify after each review unless explicitly disabled
        if not args.no_auto_verify:
            print("\n=== Running auto verification ===")
            verify_cmd = [
                sys.executable,
                str(AUTO_VERIFY_SCRIPT),
                "--limit",
                str(args.limit),
                "--max-iterations",
                "3",
            ]
            verify_result = subprocess.run(verify_cmd, capture_output=True, text=True)
            print(verify_result.stdout)
            if verify_result.returncode != 0:
                print("Auto-verify failed. Adjusting rules...")
                if verify_result.stderr:
                    print(verify_result.stderr[:1000])
            else:
                print("Auto-verify passed.")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
