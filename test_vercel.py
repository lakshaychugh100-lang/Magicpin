import requests
import json
import time

BOT_URL = "http://localhost:8000/v1"

def print_section(title):
    print(f"\n{'='*50}\n{title}\n{'='*50}")

def test_health():
    print_section("1. Endpoint Health")
    try:
        r = requests.get(f"{BOT_URL}/healthz", timeout=10)
        print(f"Status: {r.status_code}")
        print(f"Response: {r.text}")
    except Exception as e:
        print(f"Failed to connect: {e}")

def test_triggers():
    print_section("2. Trigger Coverage & Schema (Tick)")
    triggers_to_test = [
        "research_digest", 
        "regulation_change", 
        "recall_due", 
        "perf_dip", 
        "festival_upcoming", 
        "review_theme_emerged"
    ]
    
    # Push a dummy merchant
    requests.post(f"{BOT_URL}/context", json={
        "scope": "merchant", "context_id": "001", "version": 999,
        "payload": {
            "merchant_id": "001",
            "category_slug": "health_medical",
            "identity": {
                "name": "Test Merchant",
                "city": "Test City",
                "locality": "Test Locality",
                "place_id": "P123",
                "verified": True
            }
        },
        "delivered_at": "2026-07-15T00:00:00Z"
    })
    
    for kind in triggers_to_test:
        tid = f"test_fresh_{kind}"
        
        # Push the trigger context
        requests.post(f"{BOT_URL}/context", json={
            "scope": "trigger", "context_id": tid, "version": 999,
            "payload": {
                "id": tid,
                "scope": "merchant",
                "kind": kind,
                "source": "system",
                "merchant_id": "001",
                "urgency": 5,
                "suppression_key": "test",
                "expires_at": "2026-07-15T00:00:00Z"
            },
            "delivered_at": "2026-07-15T00:00:00Z"
        })
        
        # Tick
        r = requests.post(f"{BOT_URL}/tick", json={
            "now": "2026-07-15T00:00:00Z",
            "available_triggers": [tid]
        })
        
        print(f"\n--- Trigger: {kind} ---")
        print(f"HTTP {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            actions = data.get("actions", [])
            if not actions:
                print(f"[FAIL] Schema error: 'actions' list is empty!")
            else:
                action = actions[0]
                if "body" in action:
                    print(f"[PASS] Schema has 'body'")
                    print(f"Body length: {len(action['body'])} chars")
                    print(f"Body content: {action['body']}")
                elif "message" in action:
                    print(f"[FAIL] Schema error: Returned 'message' instead of 'body'")
                else:
                    print(f"[FAIL] Schema error: No 'body' or 'message' found. Keys: {list(action.keys())}")
        else:
            print(f"[FAIL] API Error: {r.text}")

def test_replies():
    print_section("3. Reply Handling (from_role & edge cases)")
    
    cases = [
        {
            "name": "Merchant Technical Follow-up",
            "payload": {
                "message": "Got it doc - need help auditing my X-ray setup. We have an old D-speed film unit.",
                "from_role": "merchant"
            }
        },
        {
            "name": "Customer Slot Pick",
            "payload": {
                "message": "Yes please book me for Wed 5 Nov, 6pm.",
                "from_role": "customer"
            }
        },
        {
            "name": "Hostile / Opt-out",
            "payload": {
                "message": "Stop messaging me. This is useless spam.",
                "from_role": "merchant"
            }
        }
    ]
    
    for case in cases:
        print(f"\n--- Test: {case['name']} ---")
        r = requests.post(f"{BOT_URL}/reply", json=case['payload'])
        print(f"HTTP {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            print(f"Action: {data.get('action')}")
            print(f"Body/Message: {data.get('body', data.get('message', ''))}")
        else:
            print(f"Error: {r.text}")

if __name__ == "__main__":
    test_health()
    test_triggers()
    test_replies()
