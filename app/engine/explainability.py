from typing import Dict, Any, List

class ExplainabilityBuilder:
    def build_rationale(self, features: Dict[str, Any], winner: str) -> str:
        reasons = []
        for feat, val in features.items():
            if val:
                reasons.append(feat)
        
        reasons_str = ", ".join(reasons)
        return f"Selected {winner} based on {reasons_str}"
