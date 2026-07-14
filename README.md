# Vera Deterministic Message Engine - Submission

## Approach

This submission implements a **highly modular, configuration-driven deterministic orchestration engine**. Rather than relying on a generative LLM to dynamically invent responses in real-time, the engine uses a robust feature extraction and scoring pipeline to guarantee deterministic, safe, and context-grounded outputs.

The architecture strictly separates the **decision layer** from the **rendering layer**:

1. **Context Management (Idempotent Store)**: Incoming payloads (Merchant, Customer) are version-controlled and stored locally.
2. **Feature Extractor**: Dynamically extracts critical features (e.g., `is_low_conversion`, `stale_posts`) using declarative rules defined in JSON configs, avoiding hardcoded logic.
3. **Rule & Ranking Engine**: Matches features against weighted rules to rank strategies (e.g., `Push Offer` vs `Research Insight`). Tie-breakers ensure consistent selection.
4. **Strategy Registry**: Resolves the winning strategy and computes the required variables.
5. **Renderer**: Selects a tone-appropriate template variant deterministically via a stable `SHA-256` hash of the `merchant_id`.
6. **Policy Validator**: Ensures the final rendered payload strictly adheres to constraints (e.g., exact maximum word counts, exactly one CTA, no hallucinatory data) before returning the response.

## Model Choice
No runtime LLM is utilized in the critical path for decision making or message rendering. 
**Why?** 
- **Determinism:** LLMs inherently introduce variance and hallucination risks, especially under tight timeouts (30s) or when handling edge-case injections.
- **Latency:** The rule-based engine resolves the entire pipeline in <100ms.
- **Safety:** It guarantees that Vera never invents a discount or ignores the category's tone constraints.

*(Note: An LLM could optionally be injected strictly as a post-render stylistic formatter with rigid system prompts, but the pure template approach already achieves high specificity and compulsion).*

## Tradeoffs

1. **Scalability vs Flexibility**: The system scales effortlessly and deterministically across millions of merchants, but adapting to entirely novel, unstructured trigger types requires adding a new strategy class and config entry.
2. **Conversation State**: The current implementation utilizes a lightweight state machine (e.g., `Idle -> Offer Suggested -> Waiting Reply`). While excellent for the challenge's replay testing, a full production CRM might require deeper conversational branching logic.
3. **Storage**: Currently abstracted behind a `Store` interface using `SQLite` for easy standalone evaluation. It can be instantly swapped to `RedisStore` in production for distributed caching.

## API Endpoints
All required endpoints are fully functional and stateless at the application layer:
- `POST /v1/context`
- `POST /v1/tick`
- `POST /v1/reply`
- `GET /v1/healthz`
- `GET /v1/metadata`
