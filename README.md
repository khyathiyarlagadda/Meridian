# Meridian — Commercial Intelligence & Multi-Agent Execution Platform

> **Meridian** is an intelligent e-commerce commercial analytics and insight execution platform built for modern D2C merchants in India. It pairs **pure deterministic pandas analytics** with a **5-agent intelligence workflow**, **bootstrap predictive simulations**, **risk-tier policy governance**, and **Razorpay test-mode execution**.

---

## Executive Screenshots

### 1. Commercial Intelligence Dashboard (`http://localhost:3000`)
![Meridian Commercial Opportunities Dashboard](file:///C:/Users/User/.gemini/antigravity/brain/449d913b-aff4-429b-87b7-df20ea995eaa/real_dashboard_final.png)

### 2. Campaign Manager & Approval Hub (`http://localhost:3000/campaigns`)
![Campaign Builder & Simulator](file:///C:/Users/User/.gemini/antigravity/brain/449d913b-aff4-429b-87b7-df20ea995eaa/campaign_builder_populated.png)

### 3. Deliberate Supervisor Policy Rejection Guardrail
![Supervisor Policy Rejection](file:///C:/Users/User/.gemini/antigravity/brain/449d913b-aff4-429b-87b7-df20ea995eaa/supervisor_policy_rejection.png)

### 4. Live AI Activity Audit Trail (`http://localhost:3000/ai-activity`)
![AI Activity Timeline](file:///C:/Users/User/.gemini/antigravity/brain/449d913b-aff4-429b-87b7-df20ea995eaa/ai_activity_timeline_styled.png)

### 5. Design System Showcase (`http://localhost:3000/design-system`)
![Meridian Design System](file:///C:/Users/User/.gemini/antigravity/brain/449d913b-aff4-429b-87b7-df20ea995eaa/design_system_final.png)

---

## Problem Statement & Architecture

Indian D2C merchants operating on Shopify or custom storefronts face three core challenges:
1. **Unidentified Cross-Sell / Bundle Opportunities**: Earbud buyers converting to Phone Cases at 5.6x baseline rates go unnoticed.
2. **At-Risk VIP Churn**: High-value repeat customers becoming inactive past 60 days without proactive intervention.
3. **Unsafe Automated AI Execution**: Opaque AI models launching unauthorized discounts or budget-exceeding campaigns.

### Meridian Solution Architecture
- **Deterministic Analytics Engine**: Zero LLM hallucination for mathematical calculations (RFM segmentation, market-basket lift, SKU velocity).
- **Multi-Agent Intelligence Layer**: 5 specialized Python agents (`OpportunityAgent`, `StrategyAgent`, `CampaignAgent`, `EvaluationAgent`, `Assistant`).
- **Supervisor Policy Engine**: Plain Python rules engine enforcing max budget (₹50,000) and max discount (25%) guardrails.
- **Razorpay Sandbox Integration**: Creates official test-mode orders (`order_rzp_test_...`) upon merchant campaign approval.

---

## Quick Start & Setup Instructions

> **IMPORTANT SETUP RULE**: Run `npm install` and `npm run dev` **from inside the `/frontend` directory**, NOT the monorepo root.

### 1. Seed Demo Data & Initialize Backend

```powershell
# 1. Navigate to backend directory
cd backend

# 2. Activate Python virtual environment & install dependencies
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 3. One-command seed demo data (regenerates clean NOVA dataset & pre-computes opportunities)
python ..\data\seed_demo_data.py

# 4. Launch FastAPI REST Backend (Port 8000)
uvicorn main:app --reload --port 8000
```

### 2. Launch Next.js 14 Frontend

```powershell
# Open a second terminal window and navigate to /frontend
cd frontend

# Install Node dependencies (run inside /frontend)
npm install

# Start Next.js Development Server (Port 3000)
npm run dev
```

*Open your browser at*: `http://localhost:3000`

---

## Verification & Test Commands

### 1. Run Multi-Agent Workflow Test
```powershell
python backend\run_agent_chain.py
```

### 2. Run Predictive Simulation & Controlled A/B Test
```powershell
python backend\run_simulation_and_experiment.py
```

### 3. Run Razorpay Test-Mode Verification
```powershell
python backend\run_razorpay_verification.py
```

### 4. Verify Frontend Production Build
```powershell
cd frontend
npm run build
```

---

## Repository Structure

```text
C:\Dev\Meridian
├── frontend/             # Next.js 14 (App Router) + TypeScript + Tailwind CSS
│   ├── app/
│   │   ├── page.tsx      # Commercial Intelligence Dashboard
│   │   ├── campaigns/    # Campaign Manager & Approval Hub
│   │   ├── ai-activity/  # Live AI Activity & Audit Trail
│   │   └── design-system/# Design System Showcase
│   └── components/       # Reusable Component Library (Button, Badge, Card, StatNumber, Sidebar, ChatPanel)
│
├── backend/              # Python FastAPI REST Backend & Analytics
│   ├── main.py           # FastAPI Endpoints
│   ├── analytics.py      # Deterministic Pandas Engine (RFM, Market-Basket, Velocity)
│   ├── simulation.py     # 1,000-sample Bootstrap Simulation Engine
│   ├── experiment.py     # 500 vs 500 Controlled A/B Experiment
│   ├── razorpay_client.py# Razorpay Test-Mode Integration (rzp_test_)
│   ├── assistant.py      # Function-Calling AI Assistant
│   └── agents/           # 5-Agent Architecture (Opportunity, Strategy, Campaign, Evaluation, Supervisor)
│
├── data/                 # Demo Synthetic Dataset for NOVA Merchant
│   ├── nova/             # 35 SKUs, 2,000 Customers, 10,000 Transactions
│   └── seed_demo_data.py # One-command clean data seed script
│
└── docs/                 # Architecture Specifications & Diagram
    ├── BRIEF.md
    ├── ARCHITECTURE.md
    ├── razorpay-integration.md
    └── architecture_diagram.svg
```
