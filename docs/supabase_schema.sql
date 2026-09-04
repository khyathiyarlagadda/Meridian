-- =============================================================================
-- MERIDIAN SUPABASE CENTRAL CLOUD DATABASE SCHEMA
-- Multi-Merchant Architecture with Demo Merchant (MERCHANT_NOVA_001) Support
-- =============================================================================

-- Enable UUID extension if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- -----------------------------------------------------------------------------
-- 1. MERCHANTS TABLE
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS merchants (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    domain TEXT,
    currency TEXT DEFAULT 'INR',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- -----------------------------------------------------------------------------
-- 2. CUSTOMERS TABLE
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS customers (
    customer_id TEXT PRIMARY KEY,
    merchant_id TEXT NOT NULL REFERENCES merchants(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    segment TEXT,
    total_spent NUMERIC DEFAULT 0.0,
    order_count INT DEFAULT 0,
    last_order_date TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_customers_merchant ON customers(merchant_id);
CREATE INDEX IF NOT EXISTS idx_customers_segment ON customers(segment);

-- -----------------------------------------------------------------------------
-- 3. PRODUCTS TABLE
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS products (
    product_id TEXT PRIMARY KEY,
    merchant_id TEXT NOT NULL REFERENCES merchants(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price_inr NUMERIC NOT NULL,
    stock_quantity INT DEFAULT 100,
    status TEXT DEFAULT 'active',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_products_merchant ON products(merchant_id);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);

-- -----------------------------------------------------------------------------
-- 4. ORDERS TABLE
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    merchant_id TEXT NOT NULL REFERENCES merchants(id) ON DELETE CASCADE,
    customer_id TEXT REFERENCES customers(customer_id) ON DELETE SET NULL,
    order_date TIMESTAMPTZ DEFAULT NOW(),
    total_amount_inr NUMERIC NOT NULL,
    status TEXT DEFAULT 'COMPLETED',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_orders_merchant ON orders(merchant_id);

-- -----------------------------------------------------------------------------
-- 5. TRANSACTIONS TABLE (Razorpay & Recorded Transactions)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id TEXT PRIMARY KEY,
    merchant_id TEXT NOT NULL REFERENCES merchants(id) ON DELETE CASCADE,
    campaign_id TEXT,
    customer_id TEXT,
    razorpay_order_id TEXT,
    razorpay_payment_id TEXT,
    razorpay_signature TEXT,
    product TEXT,
    amount NUMERIC NOT NULL,
    discount_applied TEXT,
    status TEXT DEFAULT 'COMPLETED',
    timestamp TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_transactions_merchant ON transactions(merchant_id);
CREATE INDEX IF NOT EXISTS idx_transactions_campaign ON transactions(campaign_id);

-- -----------------------------------------------------------------------------
-- 6. OPPORTUNITIES TABLE
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS opportunities (
    id TEXT PRIMARY KEY,
    merchant_id TEXT NOT NULL REFERENCES merchants(id) ON DELETE CASCADE,
    type TEXT NOT NULL,
    title TEXT NOT NULL,
    affected_customer_count INT DEFAULT 0,
    priority_score NUMERIC DEFAULT 0.0,
    estimated_revenue_potential JSONB DEFAULT '{}'::jsonb,
    recommended_strategy TEXT,
    cross_sell_lift_pct NUMERIC DEFAULT 0.0,
    status TEXT DEFAULT 'ACTIVE',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_opportunities_merchant ON opportunities(merchant_id);

-- -----------------------------------------------------------------------------
-- 7. STRATEGIES TABLE
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS strategies (
    id TEXT PRIMARY KEY,
    opportunity_id TEXT REFERENCES opportunities(id) ON DELETE CASCADE,
    strategy_type TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    expected_lift JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- -----------------------------------------------------------------------------
-- 8. CAMPAIGNS TABLE
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS campaigns (
    id TEXT PRIMARY KEY,
    merchant_id TEXT NOT NULL REFERENCES merchants(id) ON DELETE CASCADE,
    opportunity_id TEXT REFERENCES opportunities(id) ON DELETE SET NULL,
    title TEXT NOT NULL,
    strategy TEXT NOT NULL,
    target_audience TEXT,
    audience_size INT DEFAULT 0,
    offer TEXT,
    discount_pct NUMERIC DEFAULT 0.0,
    budget_inr NUMERIC DEFAULT 0.0,
    message TEXT,
    timing TEXT,
    status TEXT DEFAULT 'PENDING_MERCHANT_APPROVAL',
    risk_tier TEXT DEFAULT 'medium',
    roi_pct NUMERIC DEFAULT 0.0,
    incremental_revenue_inr NUMERIC DEFAULT 0.0,
    predicted_performance JSONB DEFAULT '{}'::jsonb,
    actual_performance JSONB DEFAULT '{}'::jsonb,
    performance_delta JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_campaigns_merchant ON campaigns(merchant_id);
CREATE INDEX IF NOT EXISTS idx_campaigns_status ON campaigns(status);

-- -----------------------------------------------------------------------------
-- 9. CAMPAIGN_RESULTS TABLE
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS campaign_results (
    id TEXT PRIMARY KEY,
    campaign_id TEXT NOT NULL REFERENCES campaigns(id) ON DELETE CASCADE,
    customers_reached INT DEFAULT 0,
    orders_count INT DEFAULT 0,
    revenue_inr NUMERIC DEFAULT 0.0,
    roi_multiple NUMERIC DEFAULT 0.0,
    summary_sentence TEXT,
    recorded_at TIMESTAMPTZ DEFAULT NOW()
);

-- -----------------------------------------------------------------------------
-- 10. EXPERIMENTS TABLE
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS experiments (
    id TEXT PRIMARY KEY,
    merchant_id TEXT NOT NULL REFERENCES merchants(id) ON DELETE CASCADE,
    opportunity_type TEXT NOT NULL,
    control_group JSONB DEFAULT '{}'::jsonb,
    ai_targeted_group JSONB DEFAULT '{}'::jsonb,
    measured_experiment_lift JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- -----------------------------------------------------------------------------
-- 11. AUDIT_LOGS TABLE (Agent Activity & Plain-Language Chain)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS audit_logs (
    id SERIAL PRIMARY KEY,
    merchant_id TEXT NOT NULL REFERENCES merchants(id) ON DELETE CASCADE,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    agent TEXT NOT NULL,
    action TEXT NOT NULL,
    input_summary TEXT,
    output_summary TEXT,
    approver TEXT
);

CREATE INDEX IF NOT EXISTS idx_audit_logs_merchant ON audit_logs(merchant_id);

-- -----------------------------------------------------------------------------
-- 12. MERCHANT_SETTINGS TABLE (Guardrails & Preferences)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS merchant_settings (
    merchant_id TEXT PRIMARY KEY REFERENCES merchants(id) ON DELETE CASCADE,
    max_discount_percent NUMERIC DEFAULT 25.0,
    max_campaign_budget NUMERIC DEFAULT 50000.0,
    max_campaigns_per_day INT DEFAULT 10,
    require_approval_to_launch BOOLEAN DEFAULT TRUE,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- -----------------------------------------------------------------------------
-- 13. AI_MEMORY TABLE
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS ai_memory (
    key TEXT PRIMARY KEY,
    merchant_id TEXT NOT NULL REFERENCES merchants(id) ON DELETE CASCADE,
    category TEXT NOT NULL,
    title TEXT NOT NULL,
    fact_statement TEXT NOT NULL,
    supporting_data JSONB DEFAULT '{}'::jsonb,
    applied_count INT DEFAULT 1,
    last_updated TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_ai_memory_merchant ON ai_memory(merchant_id);

-- =============================================================================
-- ROW LEVEL SECURITY (RLS) POLICIES
-- Multi-Tenant Preparedness: Enable RLS and grant read/write access to public anon & authenticated
-- =============================================================================
ALTER TABLE merchants ENABLE ROW LEVEL SECURITY;
ALTER TABLE customers ENABLE ROW LEVEL SECURITY;
ALTER TABLE products ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE transactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE opportunities ENABLE ROW LEVEL SECURITY;
ALTER TABLE strategies ENABLE ROW LEVEL SECURITY;
ALTER TABLE campaigns ENABLE ROW LEVEL SECURITY;
ALTER TABLE campaign_results ENABLE ROW LEVEL SECURITY;
ALTER TABLE experiments ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE merchant_settings ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_memory ENABLE ROW LEVEL SECURITY;

-- Allow public access for single-merchant demo mode
CREATE POLICY "Allow public read access" ON merchants FOR SELECT USING (true);
CREATE POLICY "Allow public all access" ON customers FOR ALL USING (true);
CREATE POLICY "Allow public all access" ON products FOR ALL USING (true);
CREATE POLICY "Allow public all access" ON orders FOR ALL USING (true);
CREATE POLICY "Allow public all access" ON transactions FOR ALL USING (true);
CREATE POLICY "Allow public all access" ON opportunities FOR ALL USING (true);
CREATE POLICY "Allow public all access" ON strategies FOR ALL USING (true);
CREATE POLICY "Allow public all access" ON campaigns FOR ALL USING (true);
CREATE POLICY "Allow public all access" ON campaign_results FOR ALL USING (true);
CREATE POLICY "Allow public all access" ON experiments FOR ALL USING (true);
CREATE POLICY "Allow public all access" ON audit_logs FOR ALL USING (true);
CREATE POLICY "Allow public all access" ON merchant_settings FOR ALL USING (true);
CREATE POLICY "Allow public all access" ON ai_memory FOR ALL USING (true);
