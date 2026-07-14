from typing import Dict, Any
from app.models.merchant import Merchant
from app.models.customer import Customer
from app.models.trigger import Trigger

class Normalizer:
    @staticmethod
    def normalize_merchant(payload: Dict[str, Any]) -> Merchant:
        return Merchant(**payload)

    @staticmethod
    def normalize_customer(payload: Dict[str, Any]) -> Customer:
        return Customer(**payload)

    @staticmethod
    def normalize_trigger(payload: Dict[str, Any]) -> Trigger:
        return Trigger(**payload)
