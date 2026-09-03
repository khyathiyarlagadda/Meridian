import os
import csv
import sys
from datetime import datetime, timedelta
from collections import defaultdict

# Force UTF-8 output formatting for Windows console compatibility
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

DATA_DIR = r"C:\Dev\Meridian\data\nova"
NOW = datetime(2026, 8, 31, 14, 0, 0)
SIXTY_DAYS_AGO = NOW - timedelta(days=60)
SIX_MONTHS_AGO = NOW - timedelta(days=180)

WEEK3_START = NOW - timedelta(days=21)
WEEK3_END = NOW - timedelta(days=14)
WEEK2_START = NOW - timedelta(days=14)
WEEK2_END = NOW - timedelta(days=7)
WEEK1_START = NOW - timedelta(days=7)
WEEK1_END = NOW

# Load Products
products = {}
with open(os.path.join(DATA_DIR, "products.csv"), "r", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        products[row["product_id"]] = row

# Load Transactions
transactions = {}
cust_orders = defaultdict(list)
with open(os.path.join(DATA_DIR, "transactions.csv"), "r", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        row["dt"] = datetime.strptime(row["order_timestamp"], "%Y-%m-%d %H:%M:%S")
        row["total_amount_inr"] = float(row["total_amount_inr"])
        transactions[row["order_id"]] = row
        cust_orders[row["customer_id"]].append(row)

# Load Order Items
order_items = defaultdict(list)
with open(os.path.join(DATA_DIR, "order_items.csv"), "r", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        order_items[row["order_id"]].append(row)

print("================================================================================")
print("SANITY CHECK REPORT: INDEPENDENT RE-DERIVATION OF ALL 6 INJECTED PATTERNS")
print("================================================================================")

# PATTERN 1: Earbud -> Phone Case Cross-Sell
earbud_pids = {pid for pid, p in products.items() if p["category"] == "Wireless Earbuds"}
phone_case_pids = {pid for pid, p in products.items() if p["category"] == "Phone Cases"}

earbud_buyers = 0
earbud_cross_sells = 0

non_earbud_buyers = 0
non_earbud_cross_sells = 0

for cid, txs in cust_orders.items():
    sorted_txs = sorted(txs, key=lambda x: x["dt"])
    first_tx = sorted_txs[0]
    first_items = order_items[first_tx["order_id"]]
    first_pids = {item["product_id"] for item in first_items}
    
    has_followup_case = False
    for followup in sorted_txs[1:]:
        diff_days = (followup["dt"] - first_tx["dt"]).total_seconds() / 86400.0
        if 0 < diff_days <= 7:
            f_pids = {item["product_id"] for item in order_items[followup["order_id"]]}
            if f_pids.intersection(phone_case_pids):
                has_followup_case = True
                break
                
    if first_pids.intersection(earbud_pids):
        earbud_buyers += 1
        if has_followup_case:
            earbud_cross_sells += 1
    else:
        non_earbud_buyers += 1
        if has_followup_case:
            non_earbud_cross_sells += 1

earbud_xsell_rate = (earbud_cross_sells / earbud_buyers * 100) if earbud_buyers else 0
baseline_xsell_rate = (non_earbud_cross_sells / non_earbud_buyers * 100) if non_earbud_buyers else 0

print(f"1. Earbud -> Phone Case Cross-Sell Rate:")
print(f"   - Earbud Buyers Cross-Sell Rate: {earbud_xsell_rate:.1f}% ({earbud_cross_sells}/{earbud_buyers}) [Target: ~45%]")
print(f"   - Baseline Non-Earbud Cross-Sell Rate: {baseline_xsell_rate:.1f}% ({non_earbud_cross_sells}/{non_earbud_buyers}) [Target: ~5%]")
print()

# PATTERN 2: Phone Case + Screen Protector Bundle Co-Purchase Rate in Multi-Item Orders
multi_item_orders = 0
case_screen_bundles = 0

for oid, items in order_items.items():
    if len(items) >= 2:
        multi_item_orders += 1
        pids = {item["product_id"] for item in items}
        has_case = bool(pids.intersection(phone_case_pids))
        has_screen = bool(pids.intersection({pid for pid, p in products.items() if p["category"] == "Screen Protectors"}))
        if has_case and has_screen:
            case_screen_bundles += 1

bundle_rate = (case_screen_bundles / multi_item_orders * 100) if multi_item_orders else 0
print(f"2. Phone Case + Screen Protector Bundle Rate in Multi-Item Orders:")
print(f"   - Measured Bundle Rate: {bundle_rate:.1f}% ({case_screen_bundles}/{multi_item_orders}) [Target: >60%]")
print()

# PATTERN 3: Win-Back Cohort Count
winback_count = 0
for cid, txs in cust_orders.items():
    orders_before_60 = [t for t in txs if t["dt"] < SIXTY_DAYS_AGO and t["dt"] >= SIX_MONTHS_AGO]
    orders_after_60 = [t for t in txs if t["dt"] >= SIXTY_DAYS_AGO]
    if len(orders_before_60) >= 3 and len(orders_after_60) == 0:
        winback_count += 1

print(f"3. Win-Back Cohort Count (3+ past orders, 0 in last 60 days):")
print(f"   - Measured Count: {winback_count} customers [Target: ~180]")
print()

# PATTERN 4: Declining Product (PROD_EAR_01)
p_declining_id = "PROD_EAR_01"
w3_dec = sum(int(item["quantity"]) for oid, items in order_items.items() for item in items if item["product_id"] == p_declining_id and WEEK3_START <= transactions[oid]["dt"] < WEEK3_END)
w2_dec = sum(int(item["quantity"]) for oid, items in order_items.items() for item in items if item["product_id"] == p_declining_id and WEEK2_START <= transactions[oid]["dt"] < WEEK2_END)
w1_dec = sum(int(item["quantity"]) for oid, items in order_items.items() for item in items if item["product_id"] == p_declining_id and WEEK1_START <= transactions[oid]["dt"] < WEEK1_END)

drop_w3_w2 = ((w2_dec - w3_dec) / w3_dec * 100) if w3_dec else 0
drop_w2_w1 = ((w1_dec - w2_dec) / w2_dec * 100) if w2_dec else 0

print(f"4. Declining Product Sales Trend ({products[p_declining_id]['product_name']}):")
print(f"   - Week -3 (Aug 10-Aug 16): {w3_dec} units")
print(f"   - Week -2 (Aug 17-Aug 23): {w2_dec} units ({drop_w3_w2:+.1f}%) [Target: ~-20% to -25%]")
print(f"   - Week -1 (Aug 24-Aug 30): {w1_dec} units ({drop_w2_w1:+.1f}%) [Target: ~-20% to -25%]")
print()

# PATTERN 5: Emerging Product (PROD_WATCH_01)
p_emerging_id = "PROD_WATCH_01"
w3_em = sum(int(item["quantity"]) for oid, items in order_items.items() for item in items if item["product_id"] == p_emerging_id and WEEK3_START <= transactions[oid]["dt"] < WEEK3_END)
w2_em = sum(int(item["quantity"]) for oid, items in order_items.items() for item in items if item["product_id"] == p_emerging_id and WEEK2_START <= transactions[oid]["dt"] < WEEK2_END)
w1_em = sum(int(item["quantity"]) for oid, items in order_items.items() for item in items if item["product_id"] == p_emerging_id and WEEK1_START <= transactions[oid]["dt"] < WEEK1_END)

growth_w3_w2 = ((w2_em - w3_em) / w3_em * 100) if w3_em else 0
growth_w2_w1 = ((w1_em - w2_em) / w2_em * 100) if w2_em else 0

print(f"5. Emerging Product Sales Trend ({products[p_emerging_id]['product_name']}):")
print(f"   - Week -3 (Aug 10-Aug 16): {w3_em} units")
print(f"   - Week -2 (Aug 17-Aug 23): {w2_em} units ({growth_w3_w2:+.1f}%) [Target: >+30%]")
print(f"   - Week -1 (Aug 24-Aug 30): {w1_em} units ({growth_w2_w1:+.1f}%) [Target: >+30%]")
print()

# PATTERN 6: High-Value-Lapsed Segment Count
hvl_count = 0
for cid, txs in cust_orders.items():
    orders_before_60 = [t for t in txs if t["dt"] < SIXTY_DAYS_AGO and t["dt"] >= SIX_MONTHS_AGO]
    orders_after_60 = [t for t in txs if t["dt"] >= SIXTY_DAYS_AGO]
    if len(orders_before_60) >= 4 and len(orders_after_60) == 0:
        aov = sum(t["total_amount_inr"] for t in orders_before_60) / len(orders_before_60)
        if aov > 2500:
            hvl_count += 1

print(f"6. High-Value-Lapsed Segment Count (4+ orders, AOV > INR 2500, 0 in last 60 days):")
print(f"   - Measured Count: {hvl_count} customers [Target: ~85]")
print("================================================================================")
