from typing import Dict, Any
from app.strategies.base import Strategy
from app.models.merchant import Merchant
from app.models.trigger import Trigger

class DefaultStrategy(Strategy):
    def prepare_variables(self, merchant: Merchant, trigger: Trigger) -> Dict[str, Any]:
        return {
            "merchant_name": merchant.identity.get("name", "there"),
            "trigger_kind": trigger.kind
        }

    def get_template_path(self) -> str:
        return "default_template"
