from typing import Dict, Any, List, Tuple
from app.strategies.registry import StrategyRegistry

class RankingEngine:
    def rank(self, scores: Dict[str, float]) -> List[Tuple[str, float]]:
        # Sort by score descending
        return sorted(scores.items(), key=lambda item: item[1], reverse=True)

class StrategyResolver:
    def resolve(self, ranked_strategies: List[Tuple[str, float]]) -> str:
        if not ranked_strategies:
            return "default_strategy"
        # Just pick the top one for now. Tie breakers can be added here.
        return ranked_strategies[0][0]
