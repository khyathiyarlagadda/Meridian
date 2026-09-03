import os
import csv

DATA_DIR = r"C:\Dev\Meridian\data\nova"
files = ["products.csv", "customers.csv", "transactions.csv", "order_items.csv"]

for filename in files:
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        reader = list(csv.reader(f))
        header = reader[0]
        rows = reader[1:]
        print("=" * 60)
        print(f"FILE: {filename}")
        print(f"HEADER: {header}")
        print(f"ROW COUNT: {len(rows)}")
        print("SAMPLE (3 ROWS):")
        for r in rows[:3]:
            print(f"  {r}")
        print("=" * 60)
        print()
