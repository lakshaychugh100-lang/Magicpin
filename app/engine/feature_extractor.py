import json
from typing import Dict, Any, List
from app.models.merchant import Merchant
from app.models.customer import Customer
from app.models.trigger import Trigger

class FeatureExtractor:
    def __init__(self, config_path: str = "app/config/v1/features.json"):
        with open(config_path, "r") as f:
            self.features_config = json.load(f)

    def extract(self, merchant: Merchant, trigger: Trigger, customer: Customer = None) -> Dict[str, Any]:
        features = {}
        for config in self.features_config:
            feat_name = config["feature"]
            field_path = config["field"]
            operator = config["operator"]
            threshold = config["threshold"]
            
            value = self._get_value_from_path(field_path, merchant, trigger, customer)
            features[feat_name] = self._evaluate(value, operator, threshold)
            
        return features

    def _get_value_from_path(self, path: str, merchant: Merchant, trigger: Trigger, customer: Customer = None) -> Any:
        parts = path.split(".")
        current = None
        if parts[0] == "merchant":
            current = merchant
        elif parts[0] == "trigger":
            current = trigger
        elif parts[0] == "customer":
            current = customer
            
        if current is None:
            return None
            
        for part in parts[1:]:
            if isinstance(current, dict):
                current = current.get(part)
            else:
                current = getattr(current, part, None)
            if current is None:
                break
        return current

    def _evaluate(self, value: Any, operator: str, threshold: Any) -> bool:
        if value is None:
            return False
            
        if operator == "<":
            return value < threshold
        elif operator == "==":
            return value == threshold
        elif operator == "has_status":
            if isinstance(value, list):
                return any(getattr(item, "status", None) == threshold for item in value)
            return False
        elif operator == "contains_prefix":
            if isinstance(value, list):
                return any(str(item).startswith(threshold) for item in value)
            return False
        return False
