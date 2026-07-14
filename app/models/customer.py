from typing import List, Optional, Any
from pydantic import BaseModel

class CustomerIdentity(BaseModel):
    name: str
    phone_redacted: str
    language_pref: Optional[str] = None
    age_band: Optional[str] = None

class CustomerRelationship(BaseModel):
    first_visit: Optional[str] = None
    last_visit: Optional[str] = None
    visits_total: int
    services_received: List[str] = []
    lifetime_value: Optional[float] = None

class CustomerPreferences(BaseModel):
    preferred_slots: Optional[str] = None
    channel: str
    reminder_opt_in: bool

class CustomerConsent(BaseModel):
    opted_in_at: str
    scope: List[str] = []

class Customer(BaseModel):
    customer_id: str
    merchant_id: str
    identity: CustomerIdentity
    relationship: CustomerRelationship
    state: str
    preferences: CustomerPreferences
    consent: CustomerConsent
