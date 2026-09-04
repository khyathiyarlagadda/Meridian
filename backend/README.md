# Meridian Backend

FastAPI Python backend for Meridian Commercial Intelligence Engine.

## Structure
- `agents/` — Specialized multi-agent system (`OpportunityAgent`, `StrategyAgent`, `CampaignAgent`, `EvaluationAgent`, `SupervisorAgent`, `AuditLogger`)
- `services/` — Core business logic, analytics calculations, and external integrations
  - `analytics.py` — Pure deterministic pandas calculations (RFM, Market Basket, SKU Velocity)
  - `ai_memory.py` — Analytical memory layer and trend aggregations
  - `alerts.py` — Opportunity detection alerts
  - `assistant.py` — Natural language AI commercial assistant
  - `compute_attribution.py` — Campaign vs organic revenue attribution engine
  - `experiment.py` — 3-way multivariate controlled experiment simulator
  - `merchant_settings.py` — Merchant operational guardrails manager
  - `razorpay_client.py` — Razorpay test mode integration client with HMAC verification
  - `simulation.py` — Bootstrap predictive campaign simulation engine
  - `supabase_db.py` — Supabase Cloud PostgreSQL database persistent client
- `models/` — Pydantic request/response data schemas (`schemas.py`)
- `utils/` — Seeding & automated verification test scripts (`seed_supabase.py`, `run_supabase_verification.py`, `run_razorpay_verification.py`)
- `main.py` — Main FastAPI REST API entry point

## Getting Started

```powershell
# Activate Python virtual environment
.\venv\Scripts\Activate.ps1

# Launch REST API server
uvicorn main:app --reload --port 8000
```

## Key API Endpoints
- `GET /api/health` — Health check endpoint (`{"status": "ok"}`)
- `GET /api/opportunities` — Discovered commercial opportunities
- `GET /api/campaigns` — Current active/pending campaigns
- `POST /api/campaigns` — Create/evaluate campaign with Supervisor policy guardrails
- `POST /api/campaigns/{id}/checkout/create-order` — Create Razorpay Test Mode order
- `POST /api/campaigns/{id}/checkout/verify-payment` — Server-side HMAC signature verification
- `GET /api/settings/guardrails` — Merchant operational policy limits
