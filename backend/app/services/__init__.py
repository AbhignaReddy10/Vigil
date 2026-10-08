"""
Business logic lives here — kept separate from app/api/ routes so logic
is testable without spinning up HTTP, and reusable across endpoints,
background jobs, and the adversarial-testing/retraining scripts later.

Populated starting Month 1:
- nlp_service.py       — DistilBERT content scoring
- threat_intel_service.py — URL/domain reputation checks
- sender_service.py    — SPF/DKIM + sender history
- coordinator.py        — the deterministic decision policy
- evidence_fusion.py    — combines signals into one evidence object
- explanation_service.py — LLM-generated explanation (bounded role only)
"""
