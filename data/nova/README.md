# NOVA Synthetic Dataset Documentation

This directory contains the synthetic dataset for **NOVA**, a fictional Indian electronics/lifestyle D2C merchant.

## File Manifest & Row Counts

- `products.csv`: 35 SKUs across 7 categories (Wireless Earbuds, Power Banks, Phone Cases, Smart Watches, Chargers, Screen Protectors, Bluetooth Speakers)
- `customers.csv`: 2,000 customers with signup dates spread over the last 12 months.
- `transactions.csv`: 10,000 transactions over the last 6 months (2026-03-01 to 2026-08-31).
- `order_items.csv`: 12,500 line items across all transactions.

---

## Engineered Signals & Injected Pattern Magnitudes

| # | Pattern Description | Injected Target / Rule | Intended Magnitude |
|---|---|---|---|
| 1 | **Earbud -> Phone Case Cross-Sell** | Earbud buyers purchase a Phone Case within 7 days at a rate far higher than baseline. | ~45% cross-sell rate for Earbud buyers vs ~5% baseline. |
| 2 | **Phone Case + Screen Protector Bundle** | Multi-item orders (2+ line items) contain both Phone Case + Screen Protector. | ~66% of multi-item orders (>60% requirement). |
| 3 | **Win-Back Cohort** | Customers with 3+ past orders between 6 months and 60 days ago, but 0 orders in the last 60 days. | Exactly 180 customers. |
| 4 | **Declining Product** | `PROD_EAR_01` ("Nova Pods Lite") weekly sales drop continuously over the last 3 weeks. | Week -3: 100 units<br>Week -2: 78 units (-22%)<br>Week -1: 60 units (-23%) |
| 5 | **Emerging Product** | `PROD_WATCH_01` ("Nova Fit Pulse 2") weekly sales grow >30% per week over the last 3 weeks. | Week -3: 40 units<br>Week -2: 55 units (+37.5%)<br>Week -1: 75 units (+36.4%) |
| 6 | **High-Value-Lapsed Segment** | High-frequency/high-AOV customers (4+ orders, AOV > ₹2,500) with 0 orders in the last 60 days. | Exactly 85 customers. |
