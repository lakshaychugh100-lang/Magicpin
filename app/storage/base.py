from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class Store(ABC):
    @abstractmethod
    def save_context(self, scope: str, context_id: str, payload: Dict[str, Any], version: int, timestamp: str) -> bool:
        pass

    @abstractmethod
    def get_context(self, scope: str, context_id: str) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def save_conversation_state(self, merchant_id: str, state: str) -> None:
        pass

    @abstractmethod
    def get_conversation_state(self, merchant_id: str) -> str:
        pass
