import json
import re
from typing import Dict, Any

class IntentEngine:
    def __init__(self, config_path: str = "app/config/v1/intents.json"):
        with open(config_path, "r") as f:
            self.intents = json.load(f)

    def evaluate(self, message: str) -> Dict[str, Any]:
        """Evaluates a message against intents and returns the configured action."""
        
        for intent in self.intents:
            matched = False
            for pattern in intent.get("patterns", []):
                if re.search(pattern, message):
                    matched = True
                    break
            
            if matched:
                # Check anti-patterns
                anti_matched = False
                for anti_pattern in intent.get("anti_patterns", []):
                    if re.search(anti_pattern, message):
                        anti_matched = True
                        break
                
                if not anti_matched:
                    # Match found! Construct the response action
                    result = {"action": intent["action"]}
                    if "wait_seconds" in intent:
                        result["wait_seconds"] = intent["wait_seconds"]
                    if "body" in intent:
                        result["body"] = intent["body"]
                    if "cta" in intent:
                        result["cta"] = intent["cta"]
                    return result
                    
        # Default fallback
        return {
            "action": "send",
            "body": "Got it. How else can I help?",
            "cta": "Reply YES"
        }
