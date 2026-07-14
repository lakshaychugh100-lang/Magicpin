import hashlib

class SuppressionEngine:
    @staticmethod
    def generate_key(merchant_id: str, strategy: str, trigger_kind: str, offer_id: str = "none", customer_id: str = "none", time_bucket: str = "") -> str:
        raw_key = f"{merchant_id}:{strategy}:{trigger_kind}:{offer_id}:{customer_id}:{time_bucket}"
        return hashlib.sha256(raw_key.encode()).hexdigest()
