from typing import Dict

class PolicyValidator:
    def validate(self, rendered: Dict[str, str], category: str) -> bool:
        message = rendered.get("message", "")
        cta = rendered.get("cta", "")
        
        # Check Length
        if len(message.split()) > 55:
            return False
            
        # Check for unformatted placeholders
        if "{" in message or "}" in message:
            return False
            
        return True
