from typing import Dict, Any, Tuple
from app.models.merchant import Merchant
from app.models.customer import Customer
from app.models.trigger import Trigger
from app.models.response import EngineResponse, DecisionTrace
from app.engine.feature_extractor import FeatureExtractor
from app.engine.rule_engine import RuleEngine
from app.engine.ranking import RankingEngine, StrategyResolver
from app.engine.renderer import Renderer
from app.engine.policy import PolicyValidator
from app.engine.suppression import SuppressionEngine
from app.engine.explainability import ExplainabilityBuilder
from app.strategies.registry import StrategyRegistry
# Import strategies to ensure they are registered
import app.strategies.research_insight 

class ComposeEngine:
    def __init__(self):
        self.feature_extractor = FeatureExtractor()
        self.rule_engine = RuleEngine()
        self.ranking = RankingEngine()
        self.resolver = StrategyResolver()
        self.renderer = Renderer()
        self.policy = PolicyValidator()
        self.explainability = ExplainabilityBuilder()
        self.suppression = SuppressionEngine()
        
        # Register strategies (in real app, loaded dynamically)
        from app.strategies.research_insight import ResearchInsightStrategy
        from app.strategies.default_strategy import DefaultStrategy
        StrategyRegistry.register("research_insight", ResearchInsightStrategy)
        StrategyRegistry.register("default_strategy", DefaultStrategy)

    def process(self, merchant: Merchant, trigger: Trigger, customer: Customer = None) -> EngineResponse:
        features = self.feature_extractor.extract(merchant, trigger, customer)
        scores = self.rule_engine.score(features)
        
        ranked = self.ranking.rank(scores)
        winner_name = self.resolver.resolve(ranked)
        
        strategy = StrategyRegistry.resolve(winner_name)
        variables = strategy.prepare_variables(merchant, trigger)
        
        rendered = self.renderer.render(strategy.get_template_path(), merchant.category_slug, merchant.merchant_id, variables)
        
        if not self.policy.validate(rendered, merchant.category_slug):
            # Fallback
            rendered = {"message": "Hello, how can we help your business today?", "cta": "Reply YES", "template_used": "fallback"}
            
        suppression_key = self.suppression.generate_key(merchant.merchant_id, winner_name, trigger.kind)
        rationale = self.explainability.build_rationale(features, winner_name)
        
        trace = DecisionTrace(
            features=features,
            scores=scores,
            winner=winner_name,
            template=rendered.get("template_used", ""),
            confidence=1.0 # placeholder
        )
        
        # Enforce 320 char limit
        final_body = rendered["message"]
        if len(final_body) > 320:
            final_body = final_body[:317] + "..."
        
        return EngineResponse(
            body=final_body,
            cta=rendered["cta"],
            send_as="Vera",
            suppression_key=suppression_key,
            rationale=rationale,
            decision_trace=trace
        )
