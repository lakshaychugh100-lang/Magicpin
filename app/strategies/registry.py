from typing import Dict, Type
from app.strategies.base import Strategy

class StrategyRegistry:
    _strategies: Dict[str, Type[Strategy]] = {}

    @classmethod
    def register(cls, name: str, strategy_class: Type[Strategy]):
        cls._strategies[name] = strategy_class

    @classmethod
    def resolve(cls, name: str) -> Strategy:
        if name not in cls._strategies:
            raise ValueError(f"Strategy {name} not found")
        return cls._strategies[name]()
