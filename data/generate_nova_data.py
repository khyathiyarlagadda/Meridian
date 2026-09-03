import os
import csv
import random
from datetime import datetime, timedelta

# Fixed seed for exact reproducibility
random.seed(42)

OUTPUT_DIR = r"C:\Dev\Meridian\data\nova"
os.makedirs(OUTPUT_DIR, exist_ok=True)

NOW = datetime(2026, 8, 31, 14, 0, 0)
SIX_MONTHS_AGO = NOW - timedelta(days=180)
TWELVE_MONTHS_AGO = NOW - timedelta(days=365)
SIXTY_DAYS_AGO = NOW - timedelta(days=60)

WEEK3_START = NOW - timedelta(days=21)
WEEK3_END = NOW - timedelta(days=14)
WEEK2_START = NOW - timedelta(days=14)
WEEK2_END = NOW - timedelta(days=7)
WEEK1_START = NOW - timedelta(days=7)
WEEK1_END = NOW

# 1. PRODUCTS (35 SKUs across 7 categories)
PRODUCTS = [
    # Wireless Earbuds
    {"product_id": "PROD_EAR_01", "product_name": "Nova Pods Lite", "category": "Wireless Earbuds", "price_inr": 1499, "launch_date": "2025-01-15"},
    {"product_id": "PROD_EAR_02", "product_name": "Nova BassPods Max", "category": "Wireless Earbuds", "price_inr": 2499, "launch_date": "2025-03-10"},
    {"product_id": "PROD_EAR_03", "product_name": "Nova Air Buds Pro", "category": "Wireless Earbuds", "price_inr": 3499, "launch_date": "2025-06-20"},
    {"product_id": "PROD_EAR_04", "product_name": "Nova SoundBuds ANC", "category": "Wireless Earbuds", "price_inr": 4299, "launch_date": "2025-11-05"},
    {"product_id": "PROD_EAR_05", "product_name": "Nova SportPods Wireless", "category": "Wireless Earbuds", "price_inr": 1999, "launch_date": "2026-02-12"},

    # Power Banks
    {"product_id": "PROD_PWR_01", "product_name": "Nova Boost 10K mAh", "category": "Power Banks", "price_inr": 1299, "launch_date": "2025-02-01"},
    {"product_id": "PROD_PWR_02", "product_name": "Nova PowerVault 20K mAh", "category": "Power Banks", "price_inr": 2199, "launch_date": "2025-04-18"},
    {"product_id": "PROD_PWR_03", "product_name": "Nova UltraCharge 30K mAh", "category": "Power Banks", "price_inr": 3299, "launch_date": "2025-08-22"},
    {"product_id": "PROD_PWR_04", "product_name": "Nova SlimPower 5000", "category": "Power Banks", "price_inr": 899, "launch_date": "2026-01-10"},
    {"product_id": "PROD_PWR_05", "product_name": "Nova MagPower Wireless 10K", "category": "Power Banks", "price_inr": 2799, "launch_date": "2026-03-15"},

    # Phone Cases
    {"product_id": "PROD_CASE_01", "product_name": "Nova Clear Flex Case", "category": "Phone Cases", "price_inr": 499, "launch_date": "2025-01-01"},
    {"product_id": "PROD_CASE_02", "product_name": "Nova Armor Shield Case", "category": "Phone Cases", "price_inr": 799, "launch_date": "2025-03-05"},
    {"product_id": "PROD_CASE_03", "product_name": "Nova MagLeather Cover", "category": "Phone Cases", "price_inr": 999, "launch_date": "2025-05-12"},
    {"product_id": "PROD_CASE_04", "product_name": "Nova Matte Silicone Case", "category": "Phone Cases", "price_inr": 599, "launch_date": "2025-07-20"},
    {"product_id": "PROD_CASE_05", "product_name": "Nova Kickstand Hybrid Case", "category": "Phone Cases", "price_inr": 899, "launch_date": "2025-10-15"},

    # Smart Watches
    {"product_id": "PROD_WATCH_01", "product_name": "Nova Fit Pulse 2", "category": "Smart Watches", "price_inr": 2999, "launch_date": "2026-05-01"},
    {"product_id": "PROD_WATCH_02", "product_name": "Nova Apex Watch Pro", "category": "Smart Watches", "price_inr": 5499, "launch_date": "2025-04-10"},
    {"product_id": "PROD_WATCH_03", "product_name": "Nova Active Band 5", "category": "Smart Watches", "price_inr": 1899, "launch_date": "2025-06-01"},
    {"product_id": "PROD_WATCH_04", "product_name": "Nova Horizon Calling Watch", "category": "Smart Watches", "price_inr": 3999, "launch_date": "2025-09-15"},
    {"product_id": "PROD_WATCH_05", "product_name": "Nova Rugged GPS Watch", "category": "Smart Watches", "price_inr": 6999, "launch_date": "2026-01-20"},

    # Chargers
    {"product_id": "PROD_CHG_01", "product_name": "Nova QuickCharge 20W", "category": "Chargers", "price_inr": 699, "launch_date": "2025-01-20"},
    {"product_id": "PROD_CHG_02", "product_name": "Nova GaN FastCharge 65W", "category": "Chargers", "price_inr": 1899, "launch_date": "2025-04-05"},
    {"product_id": "PROD_CHG_03", "product_name": "Nova Dual USB-C Wall Adapter", "category": "Chargers", "price_inr": 999, "launch_date": "2025-07-11"},
    {"product_id": "PROD_CHG_04", "product_name": "Nova Wireless Charging Pad 15W", "category": "Chargers", "price_inr": 1499, "launch_date": "2025-10-01"},
    {"product_id": "PROD_CHG_05", "product_name": "Nova Car Fast Charger 45W", "category": "Chargers", "price_inr": 799, "launch_date": "2026-02-28"},

    # Screen Protectors
    {"product_id": "PROD_SCR_01", "product_name": "Nova Guard Tempered Glass 9H", "category": "Screen Protectors", "price_inr": 299, "launch_date": "2025-01-05"},
    {"product_id": "PROD_SCR_02", "product_name": "Nova Privacy Shield Glass", "category": "Screen Protectors", "price_inr": 499, "launch_date": "2025-03-25"},
    {"product_id": "PROD_SCR_03", "product_name": "Nova Matte Anti-Glare Film", "category": "Screen Protectors", "price_inr": 349, "launch_date": "2025-06-15"},
    {"product_id": "PROD_SCR_04", "product_name": "Nova UV Curved Glass", "category": "Screen Protectors", "price_inr": 699, "launch_date": "2025-09-01"},
    {"product_id": "PROD_SCR_05", "product_name": "Nova Camera Lens Protector 2-Pack", "category": "Screen Protectors", "price_inr": 249, "launch_date": "2025-11-20"},

    # Bluetooth Speakers
    {"product_id": "PROD_SPK_01", "product_name": "Nova Boom 360 Speaker", "category": "Bluetooth Speakers", "price_inr": 2499, "launch_date": "2025-02-15"},
    {"product_id": "PROD_SPK_02", "product_name": "Nova SoundBar Mini", "category": "Bluetooth Speakers", "price_inr": 3999, "launch_date": "2025-05-10"},
    {"product_id": "PROD_SPK_03", "product_name": "Nova Pocket Party Speaker", "category": "Bluetooth Speakers", "price_inr": 1299, "launch_date": "2025-08-01"},
    {"product_id": "PROD_SPK_04", "product_name": "Nova Outdoor Waterproof Speaker", "category": "Bluetooth Speakers", "price_inr": 3299, "launch_date": "2025-11-15"},
    {"product_id": "PROD_SPK_05", "product_name": "Nova Studio Desk Speaker", "category": "Bluetooth Speakers", "price_inr": 4999, "launch_date": "2026-02-01"},
]

PROD_DICT = {p["product_id"]: p for p in PRODUCTS}

EARBUD_IDS = [p["product_id"] for p in PRODUCTS if p["category"] == "Wireless Earbuds"]
PHONE_CASE_IDS = [p["product_id"] for p in PRODUCTS if p["category"] == "Phone Cases"]
SCREEN_PROTECTOR_IDS = [p["product_id"] for p in PRODUCTS if p["category"] == "Screen Protectors"]
HIGH_AOV_PROD_IDS = [p["product_id"] for p in PRODUCTS if p["price_inr"] >= 2499]
OTHER_PROD_IDS = [p["product_id"] for p in PRODUCTS if p["product_id"] not in PHONE_CASE_IDS + SCREEN_PROTECTOR_IDS + EARBUD_IDS + ["PROD_WATCH_01"]]

FIRST_NAMES = ["Aarav", "Ananya", "Rohan", "Priya", "Vikram", "Neha", "Aditya", "Pooja", "Rahul", "Sneha", "Karan", "Ishita", "Siddharth", "Kavya", "Arjun", "Riya", "Dev", "Meera", "Amit", "Tanvi", "Varun", "Simran", "Nikhil", "Divya", "Gaurav", "Swati", "Manish", "Bhavna", "Sanjay", "Deepika"]
LAST_NAMES = ["Sharma", "Verma", "Patel", "Mehta", "Joshi", "Nair", "Rao", "Gupta", "Singh", "Kumar", "Shah", "Reddy", "Chopra", "Deshmukh", "Bhat", "Iyer", "Sen", "Das", "Agarwal", "Kapoor"]
CITIES = ["Mumbai", "Delhi", "Bengaluru", "Hyderabad", "Ahmedabad", "Chennai", "Kolkata", "Surat", "Pune", "Jaipur", "Lucknow", "Kanpur", "Nagpur", "Indore", "Thane", "Bhopal", "Visakhapatnam", "Vadodara", "Ghaziabad", "Ludhiana"]

CUSTOMERS = []
NUM_CUSTOMERS = 2000
NUM_WINBACK = 180
NUM_HIGH_VAL_LAPSED = 85

for i in range(1, NUM_CUSTOMERS + 1):
    c_id = f"CUST_{i:04d}"
    fn = random.choice(FIRST_NAMES)
    ln = random.choice(LAST_NAMES)
    name = f"{fn} {ln}"
    email = f"{fn.lower()}.{ln.lower()}{i}@example.in"
    city = random.choice(CITIES)
    
    if i <= NUM_WINBACK:
        segment = "winback"
        signup_dt = TWELVE_MONTHS_AGO + timedelta(days=random.randint(0, 180))
    elif i <= NUM_WINBACK + NUM_HIGH_VAL_LAPSED:
        segment = "high_value_lapsed"
        signup_dt = TWELVE_MONTHS_AGO + timedelta(days=random.randint(0, 180))
    else:
        segment = "regular"
        signup_dt = TWELVE_MONTHS_AGO + timedelta(days=random.randint(0, 350))
        
    CUSTOMERS.append({
        "customer_id": c_id,
        "name": name,
        "email": email,
        "city": city,
        "signup_date": signup_dt.strftime("%Y-%m-%d"),
        "segment": segment,
        "signup_datetime": signup_dt
    })

TRANSACTIONS = []
ORDER_ITEMS = []

order_counter = 10000
item_counter = 50000

def add_order(cust_id, order_dt, items_list, pay_status="completed", pay_method=None):
    global order_counter, item_counter
    order_id = f"ORD_{order_counter}"
    order_counter += 1
    
    if pay_method is None:
        pay_method = random.choice(["UPI", "UPI", "UPI", "Credit Card", "Debit Card", "COD"])
        
    total_val = 0
    order_line_items = []
    for (pid, qty) in items_list:
        item_counter += 1
        unit_price = PROD_DICT[pid]["price_inr"]
        total_price = unit_price * qty
        total_val += total_price
        order_line_items.append({
            "order_item_id": f"ITEM_{item_counter}",
            "order_id": order_id,
            "product_id": pid,
            "quantity": qty,
            "unit_price_inr": unit_price,
            "total_price_inr": total_price
        })
        
    TRANSACTIONS.append({
        "order_id": order_id,
        "customer_id": cust_id,
        "order_timestamp": order_dt.strftime("%Y-%m-%d %H:%M:%S"),
        "total_amount_inr": total_val,
        "payment_status": pay_status,
        "payment_method": pay_method,
        "order_datetime": order_dt
    })
    ORDER_ITEMS.extend(order_line_items)
    return order_id

# PATTERN 3: Win-back cohort (~180 customers, 3 past orders between 6m and 60d ago, ZERO in last 60d)
winback_custs = [cust for cust in CUSTOMERS if cust["segment"] == "winback"]
for c in winback_custs:
    for _ in range(3):
        days_offset = random.randint(0, 115)
        order_dt = SIX_MONTHS_AGO + timedelta(days=days_offset, hours=random.randint(8, 20), minutes=random.randint(0, 59))
        p = random.choice(PRODUCTS)
        add_order(c["customer_id"], order_dt, [(p["product_id"], 1)])

# PATTERN 6: High-value-lapsed segment (~85 customers, 4 past orders, AOV > 2500, ZERO in last 60d)
hvl_custs = [cust for cust in CUSTOMERS if cust["segment"] == "high_value_lapsed"]
for c in hvl_custs:
    for _ in range(4):
        days_offset = random.randint(0, 115)
        order_dt = SIX_MONTHS_AGO + timedelta(days=days_offset, hours=random.randint(8, 20), minutes=random.randint(0, 59))
        pid = random.choice(HIGH_AOV_PROD_IDS)
        add_order(c["customer_id"], order_dt, [(pid, random.randint(1, 2))])

# REGULAR CUSTOMERS
regular_custs = [c for c in CUSTOMERS if c["segment"] == "regular"]
regular_cust_ids = [c["customer_id"] for c in regular_custs]

# PATTERN 1: Earbud Buyers (400 customers) vs Non-Earbud Buyers (400 customers)
earbud_buyer_ids = regular_cust_ids[:400]
non_earbud_buyer_ids = regular_cust_ids[400:800]

# Guaranteed earliest order for Earbud buyers (175 days ago)
for idx, c_id in enumerate(earbud_buyer_ids):
    dt1 = SIX_MONTHS_AGO + timedelta(days=5, hours=random.randint(1, 10))
    add_order(c_id, dt1, [(random.choice(EARBUD_IDS), 1)])
    
    # 45% (180 buyers) purchase a phone case within 5 days (170 days ago)
    if idx < 180:
        dt2 = dt1 + timedelta(days=random.randint(1, 5), hours=random.randint(1, 5))
        add_order(c_id, dt2, [(random.choice(PHONE_CASE_IDS), 1)])

# Guaranteed earliest order for non-Earbud buyers (175 days ago)
for idx, c_id in enumerate(non_earbud_buyer_ids):
    dt1 = SIX_MONTHS_AGO + timedelta(days=5, hours=random.randint(1, 10))
    add_order(c_id, dt1, [(random.choice(OTHER_PROD_IDS), 1)])
    
    # 5% (20 buyers) purchase a phone case within 5 days (170 days ago)
    if idx < 20:
        dt2 = dt1 + timedelta(days=random.randint(1, 5), hours=random.randint(1, 5))
        add_order(c_id, dt2, [(random.choice(PHONE_CASE_IDS), 1)])

# Active regular customers get 1 order in the last 60 days to prevent overlapping into winback
for c_id in regular_cust_ids:
    recent_days_ago = random.randint(1, 55)
    dt_recent = NOW - timedelta(days=recent_days_ago, hours=random.randint(8, 20))
    add_order(c_id, dt_recent, [(random.choice(OTHER_PROD_IDS), 1)])

# PATTERN 4 & 5: Declining (PROD_EAR_01) & Emerging (PROD_WATCH_01) SKUs
declining_targets = [(WEEK3_START, WEEK3_END, 100), (WEEK2_START, WEEK2_END, 78), (WEEK1_START, WEEK1_END, 60)]
emerging_targets = [(WEEK3_START, WEEK3_END, 40), (WEEK2_START, WEEK2_END, 55), (WEEK1_START, WEEK1_END, 75)]

for w_start, w_end, count in declining_targets:
    for _ in range(count):
        c_id = random.choice(regular_cust_ids)
        seconds = random.randint(0, int((w_end - w_start).total_seconds()))
        dt = w_start + timedelta(seconds=seconds)
        add_order(c_id, dt, [("PROD_EAR_01", 1)])

for w_start, w_end, count in emerging_targets:
    for _ in range(count):
        c_id = random.choice(regular_cust_ids)
        seconds = random.randint(0, int((w_end - w_start).total_seconds()))
        dt = w_start + timedelta(seconds=seconds)
        add_order(c_id, dt, [("PROD_WATCH_01", 1)])

# PATTERN 2: Phone Case + Screen Protector Bundle (>60% of multi-item orders)
num_multi_bundle = 1650 # 66% of 2500
num_multi_other = 850   # 34% of 2500

for _ in range(num_multi_bundle):
    c_id = random.choice(regular_cust_ids)
    seconds = random.randint(0, int((NOW - SIX_MONTHS_AGO).total_seconds()))
    dt = SIX_MONTHS_AGO + timedelta(seconds=seconds)
    p_case = random.choice(PHONE_CASE_IDS)
    p_screen = random.choice(SCREEN_PROTECTOR_IDS)
    add_order(c_id, dt, [(p_case, 1), (p_screen, 1)])

for _ in range(num_multi_other):
    c_id = random.choice(regular_cust_ids)
    seconds = random.randint(0, int((NOW - SIX_MONTHS_AGO).total_seconds()))
    dt = SIX_MONTHS_AGO + timedelta(seconds=seconds)
    p1 = random.choice(OTHER_PROD_IDS)
    p2 = random.choice(OTHER_PROD_IDS)
    add_order(c_id, dt, [(p1, 1), (p2, 1)])

# FILLER TRANSACTIONS TO REACH EXACTLY 10,000 TRANSACTIONS
curr_tx_count = len(TRANSACTIONS)
target_tx_count = 10000
needed = target_tx_count - curr_tx_count

safe_filler_products = [p for p in PRODUCTS if p["product_id"] not in ["PROD_EAR_01", "PROD_WATCH_01"]]

for _ in range(needed):
    c_id = random.choice(regular_cust_ids)
    seconds = random.randint(0, int((NOW - SIX_MONTHS_AGO).total_seconds()))
    dt = SIX_MONTHS_AGO + timedelta(seconds=seconds)
    p = random.choice(safe_filler_products)
    
    status_roll = random.random()
    if status_roll < 0.95:
        p_status = "completed"
    elif status_roll < 0.98:
        p_status = "failed"
    else:
        p_status = "refunded"
        
    add_order(c_id, dt, [(p["product_id"], 1)], pay_status=p_status)

# Sort transactions chronologically
TRANSACTIONS.sort(key=lambda x: x["order_datetime"])

# Write CSV files
with open(os.path.join(OUTPUT_DIR, "products.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["product_id", "product_name", "category", "price_inr", "launch_date"])
    writer.writeheader()
    for p in PRODUCTS:
        writer.writerow({
            "product_id": p["product_id"],
            "product_name": p["product_name"],
            "category": p["category"],
            "price_inr": p["price_inr"],
            "launch_date": p["launch_date"]
        })

with open(os.path.join(OUTPUT_DIR, "customers.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["customer_id", "name", "email", "city", "signup_date"])
    writer.writeheader()
    for c in CUSTOMERS:
        writer.writerow({
            "customer_id": c["customer_id"],
            "name": c["name"],
            "email": c["email"],
            "city": c["city"],
            "signup_date": c["signup_date"]
        })

with open(os.path.join(OUTPUT_DIR, "transactions.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["order_id", "customer_id", "order_timestamp", "total_amount_inr", "payment_status", "payment_method"])
    writer.writeheader()
    for t in TRANSACTIONS:
        writer.writerow({
            "order_id": t["order_id"],
            "customer_id": t["customer_id"],
            "order_timestamp": t["order_timestamp"],
            "total_amount_inr": t["total_amount_inr"],
            "payment_status": t["payment_status"],
            "payment_method": t["payment_method"]
        })

with open(os.path.join(OUTPUT_DIR, "order_items.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["order_item_id", "order_id", "product_id", "quantity", "unit_price_inr", "total_price_inr"])
    writer.writeheader()
    for oi in ORDER_ITEMS:
        writer.writerow({
            "order_item_id": oi["order_item_id"],
            "order_id": oi["order_id"],
            "product_id": oi["product_id"],
            "quantity": oi["quantity"],
            "unit_price_inr": oi["unit_price_inr"],
            "total_price_inr": oi["total_price_inr"]
        })

print(f"Dataset generated successfully at {OUTPUT_DIR}")
print(f"Products: {len(PRODUCTS)}")
print(f"Customers: {len(CUSTOMERS)}")
print(f"Transactions: {len(TRANSACTIONS)}")
print(f"Order Items: {len(ORDER_ITEMS)}")
