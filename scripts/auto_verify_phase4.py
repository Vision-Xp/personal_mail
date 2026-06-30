"""
Automatic verification and correction loop for Phase 4 classification.
 Reads real mail content, validates classification, fixes rules, re-classifies until correct.
"""
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Set

import requests

REPO = Path(r"I:\Dev Applications\personal_mail")
FEEDBACK_PATH = REPO / "reports" / "classification_feedback.json"
RULES_PATH = REPO / "scripts" / "classification_rules.json"


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
    resp = requests.get(url, headers={"Authorization": f"Bearer {token}"}, timeout=30)
    resp.raise_for_status()
    return resp.json()


def get_message_content(token: str, msg_id: str) -> dict:
    """Fetch full message content including body."""
    msg_data = gmail_get(
        token,
        f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{msg_id}?format=full",
    )
    headers = {
        h["name"]: h["value"]
        for h in msg_data.get("payload", {}).get("headers", [])
    }
    
    # Extract body text from payload
    body = ""
    payload = msg_data.get("payload", {})
    if "parts" in payload:
        for part in payload["parts"]:
            if part.get("mimeType") == "text/plain":
                body = part.get("body", {}).get("data", "")
                break
            elif part.get("mimeType") == "text/html":
                # Fallback to HTML if no plain text
                body = part.get("body", {}).get("data", "")
    elif payload.get("mimeType") == "text/plain":
        body = payload.get("body", {}).get("data", "")
    
    return {
        "id": msg_id,
        "subject": headers.get("Subject", ""),
        "from": headers.get("From", ""),
        "to": headers.get("To", ""),
        "date": headers.get("Date", ""),
        "snippet": msg_data.get("snippet", ""),
        "body": body[:2000],  # First 2000 chars for analysis
    }


def fetch_recent_messages(token: str, limit: int = 5) -> List[dict]:
    data = gmail_get(
        token,
        f"https://gmail.googleapis.com/gmail/v1/users/me/messages?maxResults={limit}",
    )
    message_refs = data.get("messages", [])
    messages = []
    for ref in message_refs:
        messages.append(get_message_content(token, ref["id"]))
    return messages


class AutoVerifier:
    """Automatic classification verifier without human intervention."""
    
    def __init__(self):
        self.feedback = self._load_feedback()
        self.rules = self._load_rules()
        self.corrections_applied = []
    
    def _load_feedback(self) -> Dict[str, str]:
        if FEEDBACK_PATH.exists():
            return json.loads(FEEDBACK_PATH.read_text())
        return {}
    
    def _save_feedback(self) -> None:
        FEEDBACK_PATH.parent.mkdir(parents=True, exist_ok=True)
        FEEDBACK_PATH.write_text(json.dumps(self.feedback, indent=2, ensure_ascii=False))
    
    def _load_rules(self) -> Dict:
        if RULES_PATH.exists():
            return json.loads(RULES_PATH.read_text())
        return {
            "domain_rules": {},
            "sender_rules": {},
            "subject_rules": {},
            "body_rules": {},
            "confidence_thresholds": {
                "GOOGLE_SECURITY": 90,
                "BANQUE": 75,
                "ASSURANCE": 70,
                "ÉNERGIE": 70,
                "REVENUS": 75,
                "ACHATS": 65,
            }
        }
    
    def _save_rules(self) -> None:
        RULES_PATH.parent.mkdir(parents=True, exist_ok=True)
        RULES_PATH.write_text(json.dumps(self.rules, indent=2, ensure_ascii=False))
    
    def validate_classification(self, msg: dict, proposed_label: str, confidence: int) -> Tuple[bool, str]:
        """
        Auto-validate classification by checking content rules.
        Returns (is_correct, reason).
        """
        # Rule 1: Google security alerts must be classified as GOOGLE_SECURITY
        google_senders = [
            "no-reply@accounts.google.com",
            "mail-noreply@google.com",
            "accounts.google.com",
        ]
        from_lower = msg.get("from", "").lower()
        subject_lower = msg.get("subject", "").lower()
        body_lower = msg.get("body", "").lower()
        
        if any(s in from_lower for s in google_senders):
            if "alerte de sécurité" in subject_lower or "security alert" in subject_lower:
                if proposed_label != "GOOGLE_SECURITY":
                    return False, "Google security alert misclassified"
                if confidence < 90:
                    return False, "Google security alert confidence too low"
                return True, "Google security alert correctly classified"
        
        # Rule 2: Check sender domain patterns
        domain = self._extract_domain(from_lower)
        if domain in self.rules.get("sender_rules", {}):
            expected = self.rules["sender_rules"][domain]
            if proposed_label != expected:
                return False, f"Sender {domain} should be {expected}, got {proposed_label}"
            return True, f"Sender {domain} correctly classified as {expected}"
        
        # Rule 3: Check subject keywords with high confidence
        subject_keywords = {
            "banque": "BANQUE",
            "bank": "BANQUE",
            "compte": "BANQUE",
            "virement": "BANQUE",
            "assurance": "ASSURANCE",
            "mutuelle": "ASSURANCE",
            "edf": "ÉNERGIE",
            "engie": "ÉNERGIE",
            "facture": "ÉNERGIE",
            "paie": "REVENUS",
            "bulletin": "REVENUS",
            "salaire": "REVENUS",
            "amazon": "ACHATS",
            "commande": "ACHATS",
            "livraison": "ACHATS",
        }
        
        for keyword, expected_label in subject_keywords.items():
            if keyword in subject_lower:
                if proposed_label != expected_label:
                    return False, f"Subject contains '{keyword}' should be {expected_label}, got {proposed_label}"
                return True, f"Subject keyword '{keyword}' correctly classified"
        
        # Rule 4: Body content validation for high-confidence classifications
        if confidence >= 75 and proposed_label != "<none>":
            # Verify body contains related terms
            body_terms = {
                "BANQUE": ["compte", "virement", "carte", "crédit", "débit", "banque"],
                "ASSURANCE": ["contrat", "assurance", "prime", "sinistre", "mutuelle"],
                "ÉNERGIE": ["électricité", "gaz", "facture", "kwh", "énergie"],
                "REVENUS": ["salaire", "paie", "net", "brut", "revenu"],
                "ACHATS": ["commande", "livraison", "achat", "panier", "prix"],
            }
            
            if proposed_label in body_terms:
                terms = body_terms[proposed_label]
                if not any(term in body_lower for term in terms):
                    return False, f"{proposed_label} confidence {confidence}% but body lacks related terms"
        
        # Default: accept if confidence is reasonable
        if proposed_label == "<none>" or confidence < 50:
            return True, "Low confidence / no label - acceptable"
        
        return True, "Classification appears correct"
    
    def _extract_domain(self, from_field: str) -> str:
        """Extract domain from email From field."""
        if "<" in from_field:
            email = from_field.split("<")[-1].split(">")[0]
        else:
            email = from_field
        if "@" in email:
            return email.split("@")[-1].lower()
        return from_field.lower()
    
    def apply_correction(self, msg: dict, correct_label: str) -> None:
        """Apply automatic correction to rules."""
        from_lower = msg.get("from", "").lower()
        domain = self._extract_domain(from_lower)
        subject_lower = msg.get("subject", "").lower()
        
        # Update sender rules if domain is consistent
        if domain and "@" in from_lower:
            self.rules.setdefault("sender_rules", {})[domain] = correct_label
        
        # Update subject rules for strong signals
        subject_keywords = {
            "banque": "BANQUE",
            "bank": "BANQUE",
            "compte": "BANQUE",
            "virement": "BANQUE",
            "assurance": "ASSURANCE",
            "mutuelle": "ASSURANCE",
            "edf": "ÉNERGIE",
            "engie": "ÉNERGIE",
            "facture": "ÉNERGIE",
            "paie": "REVENUS",
            "bulletin": "REVENUS",
            "salaire": "REVENUS",
        }
        
        for keyword, expected in subject_keywords.items():
            if keyword in subject_lower:
                self.rules.setdefault("subject_rules", {})[keyword] = expected
        
        # Save feedback
        self.feedback[msg["id"]] = correct_label
        self._save_feedback()
        self._save_rules()
        self.corrections_applied.append({
            "id": msg["id"],
            "subject": msg["subject"],
            "from": msg["from"],
            "corrected_to": correct_label,
            "reason": f"Auto-corrected based on content analysis"
        })


def auto_verify_and_classify(limit: int = 5, max_iterations: int = 3) -> bool:
    """
    Automatic verification loop:
    1. Fetch messages
    2. Classify with current rules
    3. Validate classification automatically
    4. If errors found, correct rules and re-classify
    5. Repeat until all classifications pass or max iterations reached
    """
    verifier = AutoVerifier()
    
    token = load_token()
    
    for iteration in range(max_iterations):
        print(f"\n=== Iteration {iteration + 1}/{max_iterations} ===")
        
        messages = fetch_recent_messages(token, limit)
        all_correct = True
        corrections_needed = []
        
        for msg in messages:
            # Use current rules to classify
            proposed, confidence = classify_message(msg, verifier.feedback)
            
            # Apply domain/subject rules
            from_lower = msg.get("from", "").lower()
            subject_lower = msg.get("subject", "").lower()
            domain = verifier._extract_domain(from_lower)
            
            # Override with learned rules
            if domain in verifier.rules.get("sender_rules", {}):
                proposed = verifier.rules["sender_rules"][domain]
                confidence = 95
            
            # Validate classification
            is_correct, reason = verifier.validate_classification(msg, proposed, confidence)
            
            print(f"ID: {msg['id'][:12]}...")
            print(f"  Subject: {msg['subject'][:60]}...")
            print(f"  From: {msg['from'][:60]}...")
            print(f"  Proposed: {proposed} ({confidence}%)")
            print(f"  Valid: {is_correct} - {reason}")
            
            if not is_correct:
                all_correct = False
                corrections_needed.append((msg, proposed))
            print()
        
        if all_correct:
            print(f"✓ All {len(messages)} classifications verified correct after {iteration + 1} iteration(s)")
            return True
        
        if iteration < max_iterations - 1:
            print(f"Found {len(corrections_needed)} misclassifications. Applying corrections...")
            for msg, wrong_label in corrections_needed:
                # Determine correct label from validation reason
                correct_label = _deduce_correct_label(msg, verifier)
                verifier.apply_correction(msg, correct_label)
                print(f"  Corrected: {wrong_label} -> {correct_label}")
            
            print(f"Applied {len(corrections_needed)} corrections. Re-classifying...")
            token = load_token()  # Refresh token if needed
        else:
            print(f"⚠ Max iterations ({max_iterations}) reached. {len(corrections_needed)} classifications remain unverified.")
            for msg, wrong_label in corrections_needed:
                print(f"  Unresolved: {msg['subject'][:60]}...")
            return False
    
    return False


def _deduce_correct_label(msg: dict, verifier: AutoVerifier) -> str:
    """Deduce correct label from message content."""
    from_lower = msg.get("from", "").lower()
    subject_lower = msg.get("subject", "").lower()
    body_lower = msg.get("body", "").lower()
    
    # Google security alerts
    google_senders = [
        "no-reply@accounts.google.com",
        "mail-noreply@google.com",
        "accounts.google.com",
    ]
    if any(s in from_lower for s in google_senders):
        return "GOOGLE_SECURITY"
    
    # Check subject keywords
    keywords = {
        "banque": "BANQUE", "bank": "BANQUE", "compte": "BANQUE", "virement": "BANQUE",
        "assurance": "ASSURANCE", "mutuelle": "ASSURANCE", "contrat": "ASSURANCE",
        "edf": "ÉNERGIE", "engie": "ÉNERGIE", "facture": "ÉNERGIE", "énergie": "ÉNERGIE",
        "paie": "REVENUS", "bulletin": "REVENUS", "salaire": "REVENUS",
        "amazon": "ACHATS", "commande": "ACHATS", "livraison": "ACHATS",
    }
    
    for keyword, label in keywords.items():
        if keyword in subject_lower or keyword in body_lower[:500]:
            return label
    
    return "<none>"


# Simplified classification function for verification loop
def classify_message(msg: dict, feedback: Dict[str, str]) -> Tuple[str, int]:
    """Classify based on learned rules and feedback."""
    if msg["id"] in feedback:
        return feedback[msg["id"]], 100
    
    from_lower = msg.get("from", "").lower()
    subject_lower = msg.get("subject", "").lower()
    body_lower = msg.get("body", "").lower()
    
    # Check learned sender rules
    domain = ""
    if "<" in msg.get("from", ""):
        email = msg["from"].split("<")[-1].split(">")[0]
        if "@" in email:
            domain = email.split("@")[-1].lower()
    
    if domain and RULES_PATH.exists():
        rules = json.loads(RULES_PATH.read_text())
        if domain in rules.get("sender_rules", {}):
            return rules["sender_rules"][domain], 95
    
    # Google security alerts
    google_senders = [
        "no-reply@accounts.google.com",
        "mail-noreply@google.com",
        "google.com",
    ]
    if any(s in from_lower for s in google_senders):
        if "alerte de sécurité" in subject_lower or "security alert" in subject_lower:
            return "GOOGLE_SECURITY", 95
    
    # Subject keywords
    keywords = {
        "banque": "BANQUE", "bank": "BANQUE", "compte": "BANQUE", "virement": "BANQUE",
        "assurance": "ASSURANCE", "mutuelle": "ASSURANCE",
        "edf": "ÉNERGIE", "engie": "ÉNERGIE", "facture": "ÉNERGIE",
        "paie": "REVENUS", "bulletin": "REVENUS", "salaire": "REVENUS",
        "amazon": "ACHATS", "commande": "ACHATS",
    }
    
    for keyword, label in keywords.items():
        if keyword in subject_lower:
            return label, 85
    
    # Body content check
    if body_lower:
        body_terms = {
            "BANQUE": ["compte", "virement", "carte", "crédit", "débit"],
            "ASSURANCE": ["contrat", "assurance", "prime", "sinistre"],
            "ÉNERGIE": ["électricité", "gaz", "facture", "kwh"],
            "REVENUS": ["salaire", "paie", "net", "brut"],
            "ACHATS": ["commande", "livraison", "achat"],
        }
        for label, terms in body_terms.items():
            if any(term in body_lower for term in terms):
                return label, 70
    
    return "<none>", 0


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Auto-verify Phase 4 classification")
    parser.add_argument("--limit", type=int, default=5, help="Number of messages to verify")
    parser.add_argument("--max-iterations", type=int, default=3, help="Max correction iterations")
    args = parser.parse_args()
    
    try:
        success = auto_verify_and_classify(args.limit, args.max_iterations)
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
