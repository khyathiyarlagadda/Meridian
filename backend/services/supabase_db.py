import os
import json
import time
from datetime import datetime
from typing import List, Dict, Any, Optional

try:
    from dotenv import load_dotenv
    load_dotenv(r"C:\Dev\Meridian\backend\.env")
    load_dotenv(r"C:\Dev\Meridian\.env")
except ImportError:
    pass

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY")

supabase_client = None
if SUPABASE_URL and SUPABASE_KEY and not "your-supabase" in SUPABASE_URL:
    try:
        from supabase import create_client, Client
        supabase_client: Optional[Client] = create_client(SUPABASE_URL, SUPABASE_KEY)
        print(f"[Supabase Cloud DB] Connected successfully to {SUPABASE_URL}")
    except Exception as e:
        print(f"[Supabase Init Warning] Could not initialize Supabase SDK: {e}")

# Fallback local data files
LOCAL_DATA_DIR = r"C:\Dev\Meridian\data"
CAMPAIGNS_FILE = os.path.join(LOCAL_DATA_DIR, "campaigns.json")
RECORDED_TX_FILE = os.path.join(LOCAL_DATA_DIR, "recorded_transactions.json")
AUDIT_LOG_FILE = os.path.join(LOCAL_DATA_DIR, "audit_log.json")
SETTINGS_FILE = os.path.join(LOCAL_DATA_DIR, "merchant_settings.json")
AI_MEMORY_FILE = os.path.join(LOCAL_DATA_DIR, "nova", "ai_memory.json")

DEMO_MERCHANT_ID = "MERCHANT_NOVA_001"

# -----------------------------------------------------------------------------
# MERCHANT SETTINGS
# -----------------------------------------------------------------------------
def get_merchant_settings(merchant_id: str = DEMO_MERCHANT_ID) -> Dict[str, Any]:
    if supabase_client:
        try:
            res = supabase_client.table("merchant_settings").select("*").eq("merchant_id", merchant_id).execute()
            if res.data and len(res.data) > 0:
                data = res.data[0]
                return {
                    "max_discount_percent": float(data.get("max_discount_percent", 25.0)),
                    "max_campaign_budget": float(data.get("max_campaign_budget", 50000.0)),
                    "max_campaigns_per_day": int(data.get("max_campaigns_per_day", 10)),
                    "require_approval_to_launch": bool(data.get("require_approval_to_launch", True))
                }
        except Exception as e:
            print(f"[Supabase DB Error] get_merchant_settings fallback: {e}")

    # Fallback to local file
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    return {
        "max_discount_percent": 25.0,
        "max_campaign_budget": 50000.0,
        "max_campaigns_per_day": 10,
        "require_approval_to_launch": True
    }

def save_merchant_settings(settings: Dict[str, Any], merchant_id: str = DEMO_MERCHANT_ID) -> Dict[str, Any]:
    record = {
        "merchant_id": merchant_id,
        "max_discount_percent": float(settings.get("max_discount_percent", 25.0)),
        "max_campaign_budget": float(settings.get("max_campaign_budget", 50000.0)),
        "max_campaigns_per_day": int(settings.get("max_campaigns_per_day", 10)),
        "require_approval_to_launch": bool(settings.get("require_approval_to_launch", True)),
        "updated_at": datetime.now().isoformat()
    }

    if supabase_client:
        try:
            supabase_client.table("merchant_settings").upsert(record).execute()
        except Exception as e:
            print(f"[Supabase DB Error] save_merchant_settings fallback: {e}")

    # Also sync local file
    os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)

    return settings

# -----------------------------------------------------------------------------
# CAMPAIGNS
# -----------------------------------------------------------------------------
def get_campaigns(merchant_id: str = DEMO_MERCHANT_ID) -> List[Dict[str, Any]]:
    if supabase_client:
        try:
            res = supabase_client.table("campaigns").select("*").eq("merchant_id", merchant_id).order("created_at", desc=False).execute()
            if res.data:
                return res.data
        except Exception as e:
            print(f"[Supabase DB Error] get_campaigns fallback: {e}")

    # Fallback to local file
    if os.path.exists(CAMPAIGNS_FILE):
        try:
            with open(CAMPAIGNS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    return []

def save_campaign(campaign: Dict[str, Any], merchant_id: str = DEMO_MERCHANT_ID) -> Dict[str, Any]:
    camp_id = campaign.get("id") or campaign.get("campaign_id") or f"CAMP_{uuid.uuid4().hex[:8]}"
    record = {
        "id": camp_id,
        "merchant_id": merchant_id,
        "opportunity_id": campaign.get("opportunity_id", "OPP_CASE_SCREEN_BUNDLE"),
        "title": campaign.get("title", "Campaign Offer"),
        "strategy": campaign.get("strategy", "bundle"),
        "target_audience": campaign.get("target_audience", "Qualified Buyers"),
        "audience_size": int(campaign.get("audience_size", 2463)),
        "offer": campaign.get("offer", "Discount Tactic"),
        "discount_pct": float(campaign.get("discount_pct", 15.0)),
        "budget_inr": float(campaign.get("budget_inr", 25000.0)),
        "message": campaign.get("message", "Promotional message"),
        "timing": campaign.get("timing", "Immediate"),
        "status": campaign.get("status", "PENDING_MERCHANT_APPROVAL"),
        "risk_tier": campaign.get("risk_tier", "medium"),
        "roi_pct": float(campaign.get("roi_pct", 0.0)),
        "incremental_revenue_inr": float(campaign.get("incremental_revenue_inr", 0.0)),
        "predicted_performance": campaign.get("predicted_performance", {}),
        "actual_performance": campaign.get("actual_performance", {}),
        "performance_delta": campaign.get("performance_delta", {}),
        "updated_at": datetime.now().isoformat()
    }

    if supabase_client:
        try:
            supabase_client.table("campaigns").upsert(record).execute()
        except Exception as e:
            print(f"[Supabase DB Error] save_campaign fallback: {e}")

    # Sync local file
    existing = get_campaigns(merchant_id)
    target_idx = next((i for i, c in enumerate(existing) if c["id"] == camp_id), None)
    if target_idx is not None:
        existing[target_idx] = record
    else:
        existing.append(record)

    os.makedirs(os.path.dirname(CAMPAIGNS_FILE), exist_ok=True)
    with open(CAMPAIGNS_FILE, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2)

    return record

# -----------------------------------------------------------------------------
# TRANSACTIONS
# -----------------------------------------------------------------------------
def get_transactions(merchant_id: str = DEMO_MERCHANT_ID) -> List[Dict[str, Any]]:
    if supabase_client:
        try:
            res = supabase_client.table("transactions").select("*").eq("merchant_id", merchant_id).order("timestamp", desc=True).execute()
            if res.data:
                return res.data
        except Exception as e:
            print(f"[Supabase DB Error] get_transactions fallback: {e}")

    if os.path.exists(RECORDED_TX_FILE):
        try:
            with open(RECORDED_TX_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    return []

def record_transaction(tx_entry: Dict[str, Any], merchant_id: str = DEMO_MERCHANT_ID) -> Dict[str, Any]:
    tx_id = tx_entry.get("transaction_id") or f"TX_RZP_{int(time.time())}"
    record = {
        "transaction_id": tx_id,
        "merchant_id": merchant_id,
        "campaign_id": tx_entry.get("campaign_id", "CAMP_OPP_EARBUD_CROSSSELL"),
        "customer_id": tx_entry.get("customer_id", "CUST_1001"),
        "razorpay_order_id": tx_entry.get("razorpay_order_id"),
        "razorpay_payment_id": tx_entry.get("razorpay_payment_id"),
        "razorpay_signature": tx_entry.get("razorpay_signature"),
        "product": tx_entry.get("product", "Nova Premium Companion Phone Case"),
        "amount": float(tx_entry.get("amount", 594.15)),
        "discount_applied": tx_entry.get("discount_applied", "15%"),
        "status": tx_entry.get("status", "COMPLETED"),
        "timestamp": tx_entry.get("timestamp") or datetime.now().isoformat()
    }

    if supabase_client:
        try:
            supabase_client.table("transactions").upsert(record).execute()
        except Exception as e:
            print(f"[Supabase DB Error] record_transaction fallback: {e}")

    existing = get_transactions(merchant_id)
    existing.insert(0, record)
    os.makedirs(os.path.dirname(RECORDED_TX_FILE), exist_ok=True)
    with open(RECORDED_TX_FILE, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2)

    return record

# -----------------------------------------------------------------------------
# AUDIT LOGS
# -----------------------------------------------------------------------------
def get_audit_logs(merchant_id: str = DEMO_MERCHANT_ID) -> List[Dict[str, Any]]:
    if supabase_client:
        try:
            res = supabase_client.table("audit_logs").select("*").eq("merchant_id", merchant_id).order("id", desc=False).execute()
            if res.data:
                return res.data
        except Exception as e:
            print(f"[Supabase DB Error] get_audit_logs fallback: {e}")

    if os.path.exists(AUDIT_LOG_FILE):
        try:
            with open(AUDIT_LOG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    return []

def log_audit_entry(agent: str, action: str, input_summary: str, output_summary: str, approver: Optional[str] = None, merchant_id: str = DEMO_MERCHANT_ID) -> Dict[str, Any]:
    now_iso = datetime.now().isoformat()
    existing_logs = get_audit_logs(merchant_id)
    next_id = (max([l.get("id", 0) for l in existing_logs]) + 1) if existing_logs else 1

    record = {
        "id": next_id,
        "merchant_id": merchant_id,
        "timestamp": now_iso,
        "agent": agent,
        "action": action,
        "input_summary": input_summary,
        "output_summary": output_summary,
        "approver": approver
    }

    if supabase_client:
        try:
            supabase_client.table("audit_logs").insert({
                "merchant_id": merchant_id,
                "timestamp": now_iso,
                "agent": agent,
                "action": action,
                "input_summary": input_summary,
                "output_summary": output_summary,
                "approver": approver
            }).execute()
        except Exception as e:
            print(f"[Supabase DB Error] log_audit_entry fallback: {e}")

    existing_logs.append(record)
    os.makedirs(os.path.dirname(AUDIT_LOG_FILE), exist_ok=True)
    with open(AUDIT_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(existing_logs, f, indent=2)

    return record

# -----------------------------------------------------------------------------
# AI MEMORY
# -----------------------------------------------------------------------------
def get_ai_memories(merchant_id: str = DEMO_MERCHANT_ID) -> List[Dict[str, Any]]:
    if supabase_client:
        try:
            res = supabase_client.table("ai_memory").select("*").eq("merchant_id", merchant_id).order("last_updated", desc=True).execute()
            if res.data:
                return res.data
        except Exception as e:
            print(f"[Supabase DB Error] get_ai_memories fallback: {e}")

    if os.path.exists(AI_MEMORY_FILE):
        try:
            with open(AI_MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    return []

def save_ai_memory(memory_obj: Dict[str, Any], merchant_id: str = DEMO_MERCHANT_ID) -> Dict[str, Any]:
    key = memory_obj.get("key") or f"mem_{int(time.time())}"
    record = {
        "key": key,
        "merchant_id": merchant_id,
        "category": memory_obj.get("category", "PERFORMANCE_PATTERN"),
        "title": memory_obj.get("title", "Learned Memory"),
        "fact_statement": memory_obj.get("fact_statement", ""),
        "supporting_data": memory_obj.get("supporting_data", {}),
        "applied_count": int(memory_obj.get("applied_count", 1)),
        "last_updated": datetime.now().isoformat()
    }

    if supabase_client:
        try:
            supabase_client.table("ai_memory").upsert(record).execute()
        except Exception as e:
            print(f"[Supabase DB Error] save_ai_memory fallback: {e}")

    existing = get_ai_memories(merchant_id)
    target_idx = next((i for i, m in enumerate(existing) if m["key"] == key), None)
    if target_idx is not None:
        existing[target_idx] = record
    else:
        existing.append(record)

    os.makedirs(os.path.dirname(AI_MEMORY_FILE), exist_ok=True)
    with open(AI_MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2)

    return record
