import re
from typing import Dict, Any
from app.strategies.base import Strategy
from app.models.merchant import Merchant
from app.models.trigger import Trigger

class ResearchInsightStrategy(Strategy):
    def prepare_variables(self, merchant: Merchant, trigger: Trigger) -> Dict[str, Any]:
        stale_days = 0
        for signal in merchant.signals:
            if signal.startswith("stale_posts:"):
                match = re.search(r"stale_posts:(\d+)d", signal)
                if match:
                    stale_days = int(match.group(1))

        return {
            "owner_first_name": merchant.identity.owner_first_name or "Doctor",
            "insight_topic": "fluoride treatments" if "fluoride" in trigger.payload.get("top_item_id", "") else "oral health",
            "locality": merchant.identity.locality,
            "days_stale": stale_days
        }

    def get_template_path(self) -> str:
        return "research_insight"
