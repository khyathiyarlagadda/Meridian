import os
import json
import csv
from datetime import datetime
from services.supabase_db import supabase_client, DEMO_MERCHANT_ID

DATA_DIR = r"C:\Dev\Meridian\data"
NOVA_DIR = os.path.join(DATA_DIR, "nova")

def seed_all():
    if not supabase_client:
        print("[Seed Error] Supabase environment variables (SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY or SUPABASE_ANON_KEY) not configured.")
        print("Please add SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY to C:\\Dev\\Meridian\\backend\\.env")
        return

    print("================================================================================")
    print("SEEDING MERIDIAN CLOUD SUPABASE DATABASE")
    print(f"Merchant ID: {DEMO_MERCHANT_ID}")
    print("================================================================================")

    # 1. Seed Merchants Table
    print("\n1. Seeding Merchant...")
    merchant_data = {
        "id": DEMO_MERCHANT_ID,
        "name": "NOVA Electronics Direct",
        "domain": "nova-electronics.in",
        "currency": "INR"
    }
    supabase_client.table("merchants").upsert(merchant_data).execute()
    print("   [OK] Merchant seeded.")

    # 2. Seed Merchant Settings (Guardrails)
    print("\n2. Seeding Merchant Settings (Guardrails)...")
    settings_file = os.path.join(DATA_DIR, "merchant_settings.json")
    if os.path.exists(settings_file):
        with open(settings_file, "r", encoding="utf-8") as f:
            s_data = json.load(f)
    else:
        s_data = {"max_discount_percent": 25.0, "max_campaign_budget": 50000.0, "max_campaigns_per_day": 10, "require_approval_to_launch": True}

    s_record = {
        "merchant_id": DEMO_MERCHANT_ID,
        "max_discount_percent": float(s_data.get("max_discount_percent", 25.0)),
        "max_campaign_budget": float(s_data.get("max_campaign_budget", 50000.0)),
        "max_campaigns_per_day": int(s_data.get("max_campaigns_per_day", 10)),
        "require_approval_to_launch": bool(s_data.get("require_approval_to_launch", True))
    }
    supabase_client.table("merchant_settings").upsert(s_record).execute()
    print("   [OK] Merchant settings seeded.")

    # 3. Seed Products Table
    print("\n3. Seeding Products...")
    products_csv = os.path.join(NOVA_DIR, "products.csv")
    if os.path.exists(products_csv):
        prod_rows = []
        with open(products_csv, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                prod_rows.append({
                    "product_id": row["product_id"],
                    "merchant_id": DEMO_MERCHANT_ID,
                    "name": row["product_name"],
                    "category": row["category"],
                    "price_inr": float(row["price_inr"]),
                    "stock_quantity": int(row.get("stock_quantity", 100))
                })
        supabase_client.table("products").upsert(prod_rows).execute()
        print(f"   [OK] {len(prod_rows)} Products seeded.")

    # 4. Seed Customers Table
    print("\n4. Seeding Customers...")
    cust_csv = os.path.join(NOVA_DIR, "customers.csv")
    if os.path.exists(cust_csv):
        cust_rows = []
        with open(cust_csv, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cust_rows.append({
                    "customer_id": row["customer_id"],
                    "merchant_id": DEMO_MERCHANT_ID,
                    "name": row.get("name", f"Customer {row['customer_id']}"),
                    "email": row.get("email", f"{row['customer_id'].lower()}@example.com"),
                    "segment": row.get("segment", "active"),
                    "total_spent": float(row.get("total_spent", 0.0)),
                    "order_count": int(row.get("order_count", 1))
                })
        # Upsert in batches of 500
        batch_size = 500
        for i in range(0, len(cust_rows), batch_size):
            supabase_client.table("customers").upsert(cust_rows[i:i+batch_size]).execute()
        print(f"   [OK] {len(cust_rows)} Customers seeded.")

    # 5. Seed Opportunities Table
    print("\n5. Seeding Opportunities...")
    opps = [
        {
            "id": "OPP_EARBUD_CROSSSELL",
            "merchant_id": DEMO_MERCHANT_ID,
            "type": "earbud_case_cross_sell",
            "title": "Automated Earbud to Phone Case Cross-Sell Campaign",
            "affected_customer_count": 481,
            "priority_score": 84292.0,
            "estimated_revenue_potential": {"low": 35000, "expected": 84292, "high": 120000},
            "recommended_strategy": "cross-sell",
            "cross_sell_lift_pct": 36.4,
            "status": "ACTIVE"
        },
        {
            "id": "OPP_CASE_SCREEN_BUNDLE",
            "merchant_id": DEMO_MERCHANT_ID,
            "type": "bundle_cross_sell",
            "title": "Promote Phone Case & Screen Protector Add-On Bundle",
            "affected_customer_count": 2463,
            "priority_score": 105000.0,
            "estimated_revenue_potential": {"low": 45000, "expected": 105000, "high": 150000},
            "recommended_strategy": "bundle",
            "cross_sell_lift_pct": 28.5,
            "status": "ACTIVE"
        },
        {
            "id": "OPP_WINBACK_COHORT",
            "merchant_id": DEMO_MERCHANT_ID,
            "type": "winback_cohort",
            "title": "Re-engage At-Risk Lapsed Buyers (>60 Days Inactive)",
            "affected_customer_count": 180,
            "priority_score": 42000.0,
            "estimated_revenue_potential": {"low": 20000, "expected": 42000, "high": 60000},
            "recommended_strategy": "win-back campaign",
            "cross_sell_lift_pct": 18.0,
            "status": "ACTIVE"
        }
    ]
    supabase_client.table("opportunities").upsert(opps).execute()
    print(f"   [OK] {len(opps)} Opportunities seeded.")

    # 6. Seed Campaigns Table
    print("\n6. Seeding Campaigns...")
    camp_file = os.path.join(DATA_DIR, "campaigns.json")
    if os.path.exists(camp_file):
        with open(camp_file, "r", encoding="utf-8") as f:
            c_list = json.load(f)
            for c in c_list:
                c["merchant_id"] = DEMO_MERCHANT_ID
            supabase_client.table("campaigns").upsert(c_list).execute()
            print(f"   [OK] {len(c_list)} Campaigns seeded.")

    # 7. Seed Transactions Table
    print("\n7. Seeding Recorded Transactions...")
    tx_file = os.path.join(DATA_DIR, "recorded_transactions.json")
    if os.path.exists(tx_file):
        with open(tx_file, "r", encoding="utf-8") as f:
            tx_list = json.load(f)
            for t in tx_list:
                t["merchant_id"] = DEMO_MERCHANT_ID
            supabase_client.table("transactions").upsert(tx_list).execute()
            print(f"   [OK] {len(tx_list)} Recorded Transactions seeded.")

    # 8. Seed Audit Logs Table
    print("\n8. Seeding Audit Logs...")
    log_file = os.path.join(DATA_DIR, "audit_log.json")
    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            log_list = json.load(f)
            for log_entry in log_list:
                log_entry["merchant_id"] = DEMO_MERCHANT_ID
            supabase_client.table("audit_logs").upsert(log_list).execute()
            print(f"   [OK] {len(log_list)} Audit Logs seeded.")

    # 9. Seed AI Memory Table
    print("\n9. Seeding AI Memory...")
    mem_file = os.path.join(NOVA_DIR, "ai_memory.json")
    if os.path.exists(mem_file):
        with open(mem_file, "r", encoding="utf-8") as f:
            mem_list = json.load(f)
            for m in mem_list:
                m["merchant_id"] = DEMO_MERCHANT_ID
            supabase_client.table("ai_memory").upsert(mem_list).execute()
            print(f"   [OK] {len(mem_list)} AI Memory items seeded.")

    print("\n================================================================================")
    print("SUPABASE CLOUD DATABASE SEEDING COMPLETE!")
    print("================================================================================")

if __name__ == "__main__":
    seed_all()
