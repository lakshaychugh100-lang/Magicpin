import json
from typing import Dict, Any, List

class RuleEngine:
    def __init__(self, config_path: str = "app/config/v1/rules.json"):
        with open(config_path, "r") as f:
            self.rules = json.load(f)

    def score(self, features: Dict[str, Any]) -> Dict[str, float]:
        scores = {}
        for rule in self.rules:
            condition = rule["condition"]
            strategy = rule["strategy"]
            weight = rule["weight"]
            
            if features.get(condition):
                scores[strategy] = scores.get(strategy, 0.0) + weight
                
        return scores
