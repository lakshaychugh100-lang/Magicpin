from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class MerchantIdentity(BaseModel):
    name: str
    city: str
    locality: str
    place_id: str
    verified: bool
    languages: List[str] = []
    owner_first_name: Optional[str] = None
    established_year: Optional[int] = None

class Subscription(BaseModel):
    status: str
    plan: str
    days_remaining: int
    renewed_at: str

class Delta7d(BaseModel):
    views_pct: float
    calls_pct: float
    ctr_pct: float

class Performance(BaseModel):
    window_days: int
    views: int
    calls: int
    directions: int
    ctr: float
    leads: int
    delta_7d: Optional[Delta7d] = None

class Offer(BaseModel):
    id: str
    title: str
    status: str
    started: Optional[str] = None
    ended: Optional[str] = None

class ConversationHistory(BaseModel):
    ts: str
    sender: str = Field(alias="from")
    body: str
    engagement: Optional[str] = None
    
    class Config:
        populate_by_name = True

class CustomerAggregate(BaseModel):
    total_unique_ytd: int
    lapsed_180d_plus: int
    retention_6mo_pct: float
    high_risk_adult_count: Optional[int] = None

class ReviewTheme(BaseModel):
    theme: str
    sentiment: str
    occurrences_30d: int
    common_quote: str

class Merchant(BaseModel):
    merchant_id: str
    category_slug: str
    identity: MerchantIdentity
    subscription: Optional[Subscription] = None
    performance: Optional[Performance] = None
    offers: List[Offer] = []
    conversation_history: List[ConversationHistory] = []
    customer_aggregate: Optional[CustomerAggregate] = None
    signals: List[str] = []
    review_themes: List[ReviewTheme] = []
