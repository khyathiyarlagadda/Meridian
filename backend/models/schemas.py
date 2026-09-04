from pydantic import BaseModel
from typing import Optional, Dict, Any

class ApprovalRequest(BaseModel):
    approver: str = "Merchant Admin"
    notes: Optional[str] = None

class CampaignInput(BaseModel):
    id: Optional[str] = None
    opportunity_id: str
    title: str
    strategy: str
    target_audience: str
    offer: str
    discount_pct: float
    budget_inr: float
    message: str
    timing: str
    action_type: Optional[str] = "launch_campaign"

class AssistantQueryRequest(BaseModel):
    query: str

class GuardrailsInput(BaseModel):
    max_discount_percent: Optional[float] = 25.0
    max_campaign_budget: Optional[float] = 50000.0
    max_campaigns_per_day: Optional[int] = 10
    auto_approve_analysis: Optional[bool] = False
    auto_approve_draft_campaigns: Optional[bool] = False
    require_approval_to_launch: Optional[bool] = True

class CreateOrderRequest(BaseModel):
    customer_id: Optional[str] = "CUST_1001"
    product_id: Optional[str] = "PROD_CASE_01"
    quantity: Optional[int] = 1

class VerifyPaymentRequest(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str
    customer_id: Optional[str] = "CUST_1001"
    product: Optional[str] = "Nova Premium Phone Case"
    amount_inr: Optional[float] = 594.15
