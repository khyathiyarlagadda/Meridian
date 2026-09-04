export interface RevenuePotential {
  low: number;
  expected: number;
  high: number;
}

export interface Opportunity {
  id: string;
  type: string;
  title: string;
  description: string;
  confidence: number;
  affected_customer_count: number;
  estimated_revenue_potential: RevenuePotential;
  priority_score: number;
  supporting_evidence: Record<string, any>;
  recommended_strategy: string;
  cross_sell_lift_pct?: number;
}

export interface Campaign {
  id: string;
  opportunity_id: string;
  title: string;
  strategy: string;
  target_audience: string;
  audience_size?: number;
  offer: string;
  discount_pct: number;
  budget_inr: number;
  message: string;
  timing: string;
  status: string;
  risk_tier: string;
  roi_pct?: number;
  roi_multiple?: string;
  incremental_revenue_inr?: number;
}

export interface GuardrailSettings {
  max_discount_percent: number;
  max_campaign_budget: number;
  max_campaigns_per_day: number;
  auto_approve_analysis: boolean;
  auto_approve_draft_campaigns: boolean;
  require_approval_to_launch: boolean;
}

export interface Transaction {
  order_id: string;
  customer_id: string;
  order_timestamp: string;
  total_amount_inr: number;
  payment_status: string;
  payment_method: string;
}

export interface AuditEntry {
  id: number;
  timestamp: string;
  agent: string;
  action: string;
  input_summary: string;
  output_summary: string;
  approver?: string | null;
}

export interface ProductTrend {
  product_id: string;
  product_name: string;
  category: string;
  price_inr: number;
  units_w3: number;
  units_w2: number;
  units_w1: number;
  wow_change_w2: number;
  wow_change_w1: number;
  status: 'emerging' | 'declining' | 'stable';
  cross_sell?: string[];
}

export interface SegmentSummary {
  segment: string;
  count: number;
  avg_recency_days: number;
  avg_frequency: number;
  avg_monetary_inr: number;
  avg_aov_inr: number;
}

export interface OpportunityAlert {
  id: string;
  timestamp: string;
  type: string;
  severity: 'HIGH' | 'MEDIUM' | 'LOW';
  title: string;
  description: string;
  target_url: string;
  opportunity_id?: string;
}
