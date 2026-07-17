import requests
import json
import time

BASE_URL = "https://magicpin-bot.up.railway.app/v1"

def print_result(name, passed, detail=""):
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name} | {detail}")

def test_reply_edge_cases():
    print("\n--- Testing /reply Edge Cases ---")
    cases = [
        # Hostile edge cases
        ("Hostile: unsubscribe", "unsubscribe from this list", "end"),
        ("Hostile: don't contact", "please don't contact me again", "end"),
        ("Hostile: f-bomb", "fuck off", "end"),
        
        # Auto-reply edge cases
        ("Auto-reply: away", "i am away from keyboard", "wait"),
        ("Auto-reply: team", "our team will respond shortly to your query", "wait"),
        
        # Intent transition (Actioning)
        ("Intent: done", "done, check it", "send"),
        ("Intent: confirm", "I confirm this", "send"),
        
        # Intent transition (Qualifying / Anti-patterns should NOT match as 'send' via intent_transition_action)
        ("Anti-pattern: what if", "what if we do it tomorrow?", "send"), # Generic fallback is also 'send', but let's check the body
        
        # Gibberish
        ("Gibberish", "asdfasdfasdf", "send")
    ]
    
    for name, msg, expected_action in cases:
        payload = {"message": msg}
        try:
            resp = requests.post(f"{BASE_URL}/reply", json=payload, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                action = data.get("action")
                passed = (action == expected_action)
                
                # Special check for anti-pattern to ensure it hit the fallback, not the intent_transition_action
                if name.startswith("Anti-pattern"):
                    passed = data.get("body") == "Got it. How else can I help?"
                    
                print_result(name, passed, f"Action: {action}, Body: {data.get('body', '')}")
            else:
                print_result(name, False, f"HTTP {resp.status_code}")
        except Exception as e:
            print_result(name, False, str(e))


def test_context_edge_cases():
    print("\n--- Testing /context Edge Cases ---")
    
    # 1. Unknown scope
    payload = {
        "scope": "aliens",
        "context_id": "ufo_1",
        "version": 1,
        "payload": {"data": "test"},
        "delivered_at": "2026-07-15T00:00:00Z"
    }
    resp = requests.post(f"{BASE_URL}/context", json=payload)
    passed = resp.status_code == 200 and resp.json().get("accepted") == True
    print_result("Unknown Scope (Generic Storage)", passed, resp.text)
    
    # 2. Missing fields (should 422 Unprocessable Entity)
    bad_payload = {"scope": "merchant"} # Missing context_id, version, etc.
    resp = requests.post(f"{BASE_URL}/context", json=bad_payload)
    passed = resp.status_code == 422
    print_result("Missing Fields (Validation)", passed, f"Expected 422, got {resp.status_code}")


def test_tick_edge_cases():
    print("\n--- Testing /tick Edge Cases ---")
    
    # Non-existent merchant
    payload = {
        "id": "test_trigger",
        "scope": "merchant",
        "kind": "test",
        "source": "test",
        "merchant_id": "non_existent_merchant_999",
        "urgency": 1,
        "suppression_key": "test",
        "expires_at": "2026-07-15T00:00:00Z"
    }
    resp = requests.post(f"{BASE_URL}/tick", json=payload)
    # The API should gracefully return a 404 for a missing merchant
    passed = resp.status_code == 404
    print_result("Non-existent Merchant", passed, f"Status: {resp.status_code}")

if __name__ == "__main__":
    test_reply_edge_cases()
    test_context_edge_cases()
    test_tick_edge_cases()
    print("\nTests complete.")
