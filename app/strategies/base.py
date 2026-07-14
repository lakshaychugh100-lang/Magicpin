from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple
from app.models.merchant import Merchant
from app.models.trigger import Trigger

class Strategy(ABC):
    @abstractmethod
    def prepare_variables(self, merchant: Merchant, trigger: Trigger) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_template_path(self) -> str:
        pass
