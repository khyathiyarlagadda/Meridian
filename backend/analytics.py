import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any

DATA_DIR = r"C:\Dev\Meridian\data\nova"

def load_data(data_dir: str = DATA_DIR):
    products = pd.read_csv(os.path.join(data_dir, "products.csv"))
    customers = pd.read_csv(os.path.join(data_dir, "customers.csv"))
    transactions = pd.read_csv(os.path.join(data_dir, "transactions.csv"))
    order_items = pd.read_csv(os.path.join(data_dir, "order_items.csv"))

    transactions['order_timestamp'] = pd.to_datetime(transactions['order_timestamp'])
    customers['signup_date'] = pd.to_datetime(customers['signup_date'])
    products['launch_date'] = pd.to_datetime(products['launch_date'])
    return products, customers, transactions, order_items


def run_rfm_analysis(customers: pd.DataFrame, transactions: pd.DataFrame) -> pd.DataFrame:
    max_date = transactions['order_timestamp'].max()
    completed_tx = transactions[transactions['payment_status'] == 'completed']

    rfm = completed_tx.groupby('customer_id').agg(
        last_order=('order_timestamp', 'max'),
        first_order=('order_timestamp', 'min'),
        frequency=('order_id', 'nunique'),
        total_monetary=('total_amount_inr', 'sum')
    ).reset_index()

    rfm['recency_days'] = (max_date - rfm['last_order']).dt.total_seconds() / 86400.0
    rfm['aov'] = rfm['total_monetary'] / rfm['frequency']

    cust_rfm = pd.merge(customers, rfm, on='customer_id', how='left').fillna({
        'frequency': 0,
        'total_monetary': 0.0,
        'recency_days': 999.0,
        'aov': 0.0
    })

    def assign_segment(row):
        freq = row['frequency']
        rec = row['recency_days']
        aov = row['aov']
        
        if freq >= 4 and aov >= 2500 and rec > 60:
            return "high_value_lapsed"
        elif freq >= 3 and rec > 60:
            return "win_back_candidate"
        elif freq >= 4 and aov >= 2500 and rec <= 60:
            return "high_value_loyal"
        elif rec > 60 and freq > 0:
            return "recently_inactive"
        elif freq == 1 and rec <= 60:
            return "first_time_buyer"
        elif freq >= 2 and rec <= 60:
            return "active_repeat"
        else:
            return "prospect"

    cust_rfm['rfm_segment'] = cust_rfm.apply(assign_segment, axis=1)
    return cust_rfm


def run_market_basket_analysis(products: pd.DataFrame, transactions: pd.DataFrame, order_items: pd.DataFrame):
    prod_dict = products.set_index('product_id')['product_name'].to_dict()
    cat_dict = products.set_index('product_id')['category'].to_dict()

    items_per_order = order_items.groupby('order_id')['product_id'].apply(set).to_dict()
    multi_orders = [items for items in items_per_order.values() if len(items) >= 2]
    total_multi = len(multi_orders)

    pair_counts = {}
    item_counts = {}

    for items in multi_orders:
        item_list = list(items)
        for i in range(len(item_list)):
            it1 = item_list[i]
            item_counts[it1] = item_counts.get(it1, 0) + 1
            for j in range(i + 1, len(item_list)):
                it2 = item_list[j]
                pair = tuple(sorted([it1, it2]))
                pair_counts[pair] = pair_counts.get(pair, 0) + 1

    basket_results = []
    if total_multi > 0:
        for (p1, p2), count in pair_counts.items():
            supp = count / total_multi
            conf_p1 = count / item_counts[p1]
            conf_p2 = count / item_counts[p2]
            p1_rate = item_counts[p1] / total_multi
            p2_rate = item_counts[p2] / total_multi
            lift = supp / (p1_rate * p2_rate) if (p1_rate * p2_rate) > 0 else 0.0

            basket_results.append({
                "pair": (p1, p2),
                "prod1_name": str(prod_dict.get(p1, p1)),
                "prod2_name": str(prod_dict.get(p2, p2)),
                "cat1": str(cat_dict.get(p1, "")),
                "cat2": str(cat_dict.get(p2, "")),
                "co_purchase_count": int(count),
                "total_multi_orders": int(total_multi),
                "co_purchase_rate": float(supp),
                "lift": float(lift)
            })

    basket_df = pd.DataFrame(basket_results)
    if not basket_df.empty:
        basket_df = basket_df.sort_values(by="co_purchase_count", ascending=False)

    tx_merged = pd.merge(transactions, order_items, on='order_id')
    tx_merged['category'] = tx_merged['product_id'].map(cat_dict)

    cust_txs = tx_merged.groupby('customer_id')
    earbud_buyers = 0
    earbud_xsell_cases = 0
    non_earbud_buyers = 0
    non_earbud_xsell_cases = 0

    for cid, group in cust_txs:
        sorted_g = group.sort_values(by='order_timestamp')
        first_tx_id = sorted_g['order_id'].iloc[0]
        first_tx_dt = sorted_g['order_timestamp'].iloc[0]
        first_cats = set(sorted_g[sorted_g['order_id'] == first_tx_id]['category'])
        
        followups = sorted_g[(sorted_g['order_timestamp'] > first_tx_dt) & (sorted_g['order_timestamp'] <= first_tx_dt + pd.Timedelta(days=7))]
        has_followup_case = 'Phone Cases' in set(followups['category'])

        if 'Wireless Earbuds' in first_cats:
            earbud_buyers += 1
            if has_followup_case:
                earbud_xsell_cases += 1
        else:
            non_earbud_buyers += 1
            if has_followup_case:
                non_earbud_xsell_cases += 1

    earbud_xsell_rate = (earbud_xsell_cases / earbud_buyers) if earbud_buyers > 0 else 0.0
    baseline_xsell_rate = (non_earbud_xsell_cases / non_earbud_buyers) if non_earbud_buyers > 0 else 0.0

    cross_sell_results = {
        "earbud_buyers": int(earbud_buyers),
        "earbud_xsell_cases": int(earbud_xsell_cases),
        "earbud_xsell_rate": float(earbud_xsell_rate),
        "baseline_xsell_rate": float(baseline_xsell_rate),
        "relative_lift": float(earbud_xsell_rate / baseline_xsell_rate) if baseline_xsell_rate > 0 else 0.0
    }

    return basket_df, cross_sell_results


def run_product_velocity_trends(products: pd.DataFrame, transactions: pd.DataFrame, order_items: pd.DataFrame):
    max_date = transactions['order_timestamp'].max()
    w1_start = max_date - pd.Timedelta(days=7)
    w2_start = max_date - pd.Timedelta(days=14)
    w3_start = max_date - pd.Timedelta(days=21)

    merged = pd.merge(order_items, transactions[['order_id', 'order_timestamp', 'payment_status']], on='order_id')
    merged = merged[merged['payment_status'] == 'completed']

    def get_units_in_range(start_dt, end_dt):
        sub = merged[(merged['order_timestamp'] >= start_dt) & (merged['order_timestamp'] < end_dt)]
        return sub.groupby('product_id')['quantity'].sum().to_dict()

    w3_units = get_units_in_range(w3_start, w2_start)
    w2_units = get_units_in_range(w2_start, w1_start)
    w1_units = get_units_in_range(w1_start, max_date)

    trends = []
    for _, p in products.iterrows():
        pid = str(p['product_id'])
        u3 = int(w3_units.get(pid, 0))
        u2 = int(w2_units.get(pid, 0))
        u1 = int(w1_units.get(pid, 0))

        wow1 = float(((u2 - u3) / u3)) if u3 > 0 else 0.0
        wow2 = float(((u1 - u2) / u2)) if u2 > 0 else 0.0

        if wow1 > 0.25 and wow2 > 0.25:
            status = "emerging"
        elif wow1 < -0.15 and wow2 < -0.15:
            status = "declining"
        else:
            status = "stable"

        trends.append({
            "product_id": pid,
            "product_name": str(p['product_name']),
            "category": str(p['category']),
            "price_inr": float(p['price_inr']),
            "units_w3": u3,
            "units_w2": u2,
            "units_w1": u1,
            "wow_change_w2": round(wow1, 4),
            "wow_change_w1": round(wow2, 4),
            "status": status
        })

    return pd.DataFrame(trends)


def calculate_opportunity_score(rev_expected: float, confidence: float, affected_count: int, historical_rev: float = 0.0) -> float:
    probability = confidence
    score = (rev_expected * 0.5) + (probability * 2000.0) + (confidence * 1000.0) + (historical_rev * 0.02) - (affected_count * 2.0)
    return round(float(max(0.0, score)), 2)


def generate_opportunities(products, customers, transactions, order_items) -> List[Dict[str, Any]]:
    rfm_df = run_rfm_analysis(customers, transactions)
    basket_df, xsell_res = run_market_basket_analysis(products, transactions, order_items)
    velocity_df = run_product_velocity_trends(products, transactions, order_items)

    opportunities = []

    # 1. Earbud -> Phone Case Cross-Sell Opportunity (Pattern 1)
    eb_count = int(xsell_res['earbud_buyers'])
    earbud_xsell_rate = float(xsell_res['earbud_xsell_rate'])
    baseline_rate = float(xsell_res['baseline_xsell_rate'])
    lift_ratio = float(xsell_res['relative_lift'])
    
    expected_additional_conversions = int(eb_count * 0.40)
    rev_low = float(expected_additional_conversions * 499)
    rev_exp = float(expected_additional_conversions * 699)
    rev_high = float(expected_additional_conversions * 899)
    conf = 0.92
    hist_rev = float(eb_count * 2499)

    opp_score1 = calculate_opportunity_score(rev_exp, conf, eb_count, hist_rev)

    opportunities.append({
        "id": "OPP_EARBUD_CROSSSELL",
        "title": "Automated Earbud to Phone Case Cross-Sell Campaign",
        "type": "earbud_case_cross_sell",
        "affected_customer_count": eb_count,
        "estimated_revenue_potential": {
            "low": round(rev_low, 2),
            "expected": round(rev_exp, 2),
            "high": round(rev_high, 2)
        },
        "confidence": conf,
        "supporting_evidence": {
            "earbud_buyers_count": eb_count,
            "earbud_7day_case_purchase_rate": round(earbud_xsell_rate * 100, 1),
            "baseline_case_purchase_rate": round(baseline_rate * 100, 1),
            "cross_sell_lift": round(lift_ratio, 2)
        },
        "priority_score": opp_score1
    })

    # 2. Phone Case + Screen Protector Bundle Opportunity (Pattern 2)
    top_bundle = basket_df.iloc[0] if not basket_df.empty else None
    if top_bundle is not None:
        multi_count = int(top_bundle['total_multi_orders'])
        co_count = int(top_bundle['co_purchase_count'])
        bundle_rate = float(top_bundle['co_purchase_rate'])
        
        rev_low = float(multi_count * 199)
        rev_exp = float(multi_count * 349)
        rev_high = float(multi_count * 499)
        conf = 0.95
        hist_rev = float(co_count * 998)

        opp_score2 = calculate_opportunity_score(rev_exp, conf, multi_count, hist_rev)

        opportunities.append({
            "id": "OPP_CASE_SCREEN_BUNDLE",
            "title": "Promote Phone Case & Screen Protector Add-On Bundle",
            "type": "bundle_cross_sell",
            "affected_customer_count": multi_count,
            "estimated_revenue_potential": {
                "low": round(rev_low, 2),
                "expected": round(rev_exp, 2),
                "high": round(rev_high, 2)
            },
            "confidence": conf,
            "supporting_evidence": {
                "multi_item_order_count": multi_count,
                "case_screen_copurchase_count": co_count,
                "co_purchase_rate_pct": round(bundle_rate * 100, 1),
                "lift": round(float(top_bundle['lift']), 2)
            },
            "priority_score": opp_score2
        })

    # 3. Win-Back Cohort Opportunity (Pattern 3)
    winback_df = rfm_df[rfm_df['rfm_segment'] == 'win_back_candidate']
    wb_count = int(len(winback_df))
    wb_hist_spend = float(winback_df['total_monetary'].sum())
    wb_avg_spend = float(winback_df['total_monetary'].mean()) if wb_count > 0 else 0.0

    target_winback_conversions = int(wb_count * 0.25)
    rev_low = float(target_winback_conversions * 1200)
    rev_exp = float(target_winback_conversions * 1800)
    rev_high = float(target_winback_conversions * 2500)
    conf = 0.88

    opp_score3 = calculate_opportunity_score(rev_exp, conf, wb_count, wb_hist_spend)

    opportunities.append({
        "id": "OPP_WINBACK_COHORT",
        "title": "Re-activate Lapsed Active Customers (Win-Back Cohort)",
        "type": "win_back_cohort",
        "affected_customer_count": wb_count,
        "estimated_revenue_potential": {
            "low": round(rev_low, 2),
            "expected": round(rev_exp, 2),
            "high": round(rev_high, 2)
        },
        "confidence": conf,
        "supporting_evidence": {
            "lapsed_customers_count": wb_count,
            "min_past_orders_threshold": 3,
            "days_inactive_threshold": 60,
            "historical_cohort_revenue_inr": round(wb_hist_spend, 2),
            "avg_customer_historical_spend_inr": round(wb_avg_spend, 2)
        },
        "priority_score": opp_score3
    })

    # 4. Declining Product Mitigation Opportunity (Pattern 4)
    declining_skus = velocity_df[velocity_df['status'] == 'declining']
    if not declining_skus.empty:
        dec_sku = declining_skus.iloc[0]
        p_name = str(dec_sku['product_name'])
        w3 = int(dec_sku['units_w3'])
        w2 = int(dec_sku['units_w2'])
        w1 = int(dec_sku['units_w1'])
        price = float(dec_sku['price_inr'])

        units_lost = int(w3 - w1)
        rev_loss_per_week = float(units_lost * price)
        rev_low = float(rev_loss_per_week * 2.0)
        rev_exp = float(rev_loss_per_week * 4.0)
        rev_high = float(rev_loss_per_week * 6.0)
        conf = 0.85

        opp_score4 = calculate_opportunity_score(rev_exp, conf, units_lost, float(w3 * price))

        opportunities.append({
            "id": "OPP_DECLINING_PRODUCT",
            "title": f"Intervene on Declining SKU: {p_name}",
            "type": "declining_product_mitigation",
            "affected_customer_count": units_lost,
            "estimated_revenue_potential": {
                "low": round(rev_low, 2),
                "expected": round(rev_exp, 2),
                "high": round(rev_high, 2)
            },
            "confidence": conf,
            "supporting_evidence": {
                "product_id": str(dec_sku['product_id']),
                "product_name": p_name,
                "weekly_units_history": [w3, w2, w1],
                "wow_change_week2_pct": round(float(dec_sku['wow_change_w2']) * 100, 1),
                "wow_change_week1_pct": round(float(dec_sku['wow_change_w1']) * 100, 1)
            },
            "priority_score": opp_score4
        })

    # 5. Emerging Product Promotion Opportunity (Pattern 5)
    emerging_skus = velocity_df[velocity_df['status'] == 'emerging']
    if not emerging_skus.empty:
        em_sku = emerging_skus.iloc[0]
        p_name = str(em_sku['product_name'])
        w3 = int(em_sku['units_w3'])
        w2 = int(em_sku['units_w2'])
        w1 = int(em_sku['units_w1'])
        price = float(em_sku['price_inr'])

        added_units = int(w1 - w3)
        gained_rev = float(added_units * price)
        rev_low = float(gained_rev * 1.5)
        rev_exp = float(gained_rev * 3.0)
        rev_high = float(gained_rev * 5.0)
        conf = 0.90

        opp_score5 = calculate_opportunity_score(rev_exp, conf, added_units, float(w1 * price))

        opportunities.append({
            "id": "OPP_EMERGING_PRODUCT",
            "title": f"Scale Inventory & Marketing for Emerging SKU: {p_name}",
            "type": "emerging_product_promotion",
            "affected_customer_count": w1,
            "estimated_revenue_potential": {
                "low": round(rev_low, 2),
                "expected": round(rev_exp, 2),
                "high": round(rev_high, 2)
            },
            "confidence": conf,
            "supporting_evidence": {
                "product_id": str(em_sku['product_id']),
                "product_name": p_name,
                "weekly_units_history": [w3, w2, w1],
                "wow_growth_week2_pct": round(float(em_sku['wow_change_w2']) * 100, 1),
                "wow_growth_week1_pct": round(float(em_sku['wow_change_w1']) * 100, 1)
            },
            "priority_score": opp_score5
        })

    # 6. High-Value-Lapsed VIP Win-Back Opportunity (Pattern 6)
    hvl_df = rfm_df[rfm_df['rfm_segment'] == 'high_value_lapsed']
    hvl_count = int(len(hvl_df))
    hvl_tot_spend = float(hvl_df['total_monetary'].sum())
    hvl_avg_aov = float(hvl_df['aov'].mean()) if hvl_count > 0 else 0.0

    target_hvl_conversions = int(hvl_count * 0.35)
    rev_low = float(target_hvl_conversions * 2500)
    rev_exp = float(target_hvl_conversions * 4500)
    rev_high = float(target_hvl_conversions * 7500)
    conf = 0.94

    opp_score6 = calculate_opportunity_score(rev_exp, conf, hvl_count, hvl_tot_spend)

    opportunities.append({
        "id": "OPP_HIGH_VALUE_LAPSED",
        "title": "VIP Concierge Outreach for High-Value Lapsed Customers",
        "type": "high_value_lapsed_winback",
        "affected_customer_count": hvl_count,
        "estimated_revenue_potential": {
            "low": round(rev_low, 2),
            "expected": round(rev_exp, 2),
            "high": round(rev_high, 2)
        },
        "confidence": conf,
        "supporting_evidence": {
            "high_value_lapsed_count": hvl_count,
            "min_order_frequency": 4,
            "aov_threshold_inr": 2500,
            "total_historical_spend_inr": round(hvl_tot_spend, 2),
            "average_customer_aov_inr": round(hvl_avg_aov, 2)
        },
        "priority_score": opp_score6
    })

    opportunities.sort(key=lambda x: x['priority_score'], reverse=True)
    return opportunities
