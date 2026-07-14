import json
import os
import hashlib
from typing import Dict, Any

class Renderer:
    def __init__(self, templates_dir: str = "app/templates/v1"):
        self.templates_dir = templates_dir
        # In a real app we would cache all templates at startup
        # self.cache = self._preload_templates()

    def render(self, strategy_name: str, category_slug: str, merchant_id: str, variables: Dict[str, Any]) -> Dict[str, str]:
        path = os.path.join(self.templates_dir, category_slug, strategy_name)
        
        # fallback if category doesn't have it
        if not os.path.exists(path):
            path = os.path.join(self.templates_dir, "default", strategy_name)
            
        if not os.path.exists(path):
            return {"message": "Hello, how can we help your business today?", "cta": "Reply YES"}
            
        variants = [f for f in os.listdir(path) if f.endswith(".json")]
        if not variants:
            return {"message": "Hello, how can we help your business today?", "cta": "Reply YES"}
            
        variant_idx = int(hashlib.sha256(merchant_id.encode()).hexdigest(), 16) % len(variants)
        selected_file = variants[variant_idx]
        
        with open(os.path.join(path, selected_file), "r") as f:
            template = json.load(f)
            
        message = template.get("message", "")
        cta = template.get("cta", "")
        
        try:
            message = message.format(**variables)
            cta = cta.format(**variables)
        except KeyError as e:
            # simple fallback or leave it unformatted
            pass
            
        return {"message": message, "cta": cta, "template_used": f"{category_slug}/{strategy_name}/{selected_file}"}
