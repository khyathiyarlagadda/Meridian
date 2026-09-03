# Meridian Technical Architecture & Multi-Agent Specifications

## Overview
Meridian is an intelligent commercial analytics and insight execution platform engineered for D2C e-commerce merchants in India. The platform combines **deterministic pandas analytics**, **multi-agent reasoning**, **bootstrap predictive simulation**, and a **deterministic policy supervisor**.

---

## 1. System Topology & Data Flow

![Meridian System Architecture](architecture_diagram.svg)

```text
[ Next.js 14 Dashboard / UI ]
             │ (HTTP / JSON)
             ▼
 [ FastAPI REST API Layer ]
   ├── /api/opportunities
   ├── /api/segments
   ├── /api/products/trends
   ├── /api/pipeline/run-campaign
   ├── /api/campaigns/{id}/simulate
   ├── /api/experiments
   ├── /api/audit-log
   └── /api/assistant
             │
   ┌─────────┴────────────────────────┐
   ▼                                  ▼
[ Pure Python Analytics ]    [ Multi-Agent Workflow Engine ]
  • RFM Segmentation           • OpportunityAgent
  • Market Basket Analysis     • StrategyAgent
  • Product Sales Velocity     • CampaignAgent
  • Priority Score Model       • EvaluationAgent
                               • MeridianAssistant
                                      │
                                      ▼
                      [ Supervisor Rules Engine ]
                        (Plain Python Policy Guardrails)
                        • Budget Limit: <= INR 50,000
                        • Discount Limit: <= 25%
                        • Duplicate Detection
                        • Risk-Tier Classification
                                      │
                                      ▼
                      [ Razorpay Test Sandbox ]
                        (rzp_test_ API Integration)
```

---

## 2. Multi-Agent System Specification (`C:\Dev\Meridian\backend\agents\`)

Meridian utilizes a 5-agent workflow designed for high interpretability and human-in-the-loop safety:

### 1. Opportunity Agent (`opportunity_agent.py`)
- **Role**: Translates raw pandas metrics into natural-language descriptions.
- **Rule**: Cites **ONLY** empirical evidence numbers strictly present in Phase 2/3 datasets. No metric hallucination or guessing.

### 2. Strategy Agent (`strategy_agent.py`)
- **Role**: Selects the optimal commercial tactic from 6 standard choices:
  1. `cross-sell`
  2. `bundle`
  3. `personalized offer`
  4. `win-back campaign`
  5. `product promotion`
  6. `loyalty incentive`

### 3. Campaign Agent (`campaign_agent.py`)
- **Role**: Generates structured campaign packages containing:
  - `target_audience`
  - `title`
  - `offer`
  - `discount_pct`
  - `budget_inr`
  - `message`
  - `timing`

### 4. Evaluation Agent (`evaluation_agent.py`)
- **Role**: Compares pre-campaign baseline vs post-campaign actual metrics.
- **Outputs**:
  $$\text{Incremental Revenue} = \text{Post Revenue} - \text{Baseline Revenue}$$
  $$\text{ROI \%} = \frac{\text{Incremental Revenue} - \text{Campaign Cost}}{\text{Campaign Cost}} \times 100$$

### 5. Supervisor Agent (`supervisor_agent.py`)
- **Role**: Deterministic, rules-based policy enforcement engine (**NOT an LLM call**).
- **Conditionals**:
  ```python
  if action_type in ["process_refund", "payment_config_change"]:
      return {"status": "REJECTED", "reason": "High-risk action has no execution path"}
  if budget > 50000.0:
      violations.append("Budget exceeds max INR 50,000.00")
  if discount > 25.0:
      violations.append("Discount exceeds max 25%")
  ```

---

## 3. Risk-Tier Classification Model

| Risk Tier | Conditions | Action / Execution Path |
|---|---|---|
| **Low Risk** | Budget <= INR 10,000 & Discount <= 10% | **AUTO_EXECUTED** by system without merchant pause. |
| **Medium Risk** | Budget <= INR 50,000 & Discount <= 25% | **PENDING_MERCHANT_APPROVAL** — Pauses for explicit merchant approval via API. |
| **High Risk** | Budget > INR 50,000, Discount > 25%, or Prohibited Action | **REJECTED** with explicit policy explanation banner. |

---

## 4. Predictive Simulation & Controlled Experiment Methodology

- **Bootstrap Resampling Engine** (`simulation.py`): Performs 1,000 non-parametric bootstrap resamples over historical segment purchase outcomes to generate 5th (conservative), 50th (expected median), and 95th (optimistic) percentile revenue and conversion rate bounds.
- **Controlled A/B Experiment Framework** (`experiment.py`): Randomly partitions target audience into Control (500) vs AI-Targeted (500) customers to compute real measured conversion lift (4.1x) and AOV difference (+INR 146.06).
