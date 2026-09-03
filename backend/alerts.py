import os
import json
from datetime import datetime
from typing import List, Dict, Any

from analytics import load_data, generate_opportunities, run_product_velocity_trends
from agents.audit_logger import audit_logger

ALERTS_FILE = r"C:\Dev\Meridian\data\nova\opportunity_alerts.json"

def get_real_alerts() -> List[Dict[str, Any]]:
    """
    Returns saved opportunity alerts. If none exist, runs the detection pipeline.
    """
    if os.path.exists(ALERTS_FILE):
        try:
            with open(ALERTS_FILE, "r", encoding="utf-8") as f:
                alerts = json.load(f)
                if alerts and len(alerts) > 0:
                    return alerts
        except Exception:
            pass
    return refresh_alerts()

def refresh_alerts() -> List[Dict[str, Any]]:
    """
    Executes an on-demand re-run of the real opportunity detection pipeline:
    Analyzes products, customers, transactions, and order items.
    Extracts high-priority alerts for new opportunities, velocity drops, and demand surges.
    Logs execution to audit logger.
    """
    products, customers, transactions, order_items = load_data()
    opps = generate_opportunities(products, customers, transactions, order_items)
    trends_df = run_product_velocity_trends(products, transactions, order_items)
    trends = trends_df.to_dict(orient="records")
    
    now_str = datetime.now().strftime("%d %b %Y, %I:%M %p")
    ts_id = int(datetime.now().timestamp())

    alerts = []

    # 1. Top Opportunity Detection Alert
    if opps:
        top = opps[0]
        alerts.append({
            "id": f"ALERT_OPP_{top['id']}_{ts_id}",
            "timestamp": now_str,
            "type": "NEW_OPPORTUNITY",
            "severity": "HIGH",
            "title": f"New High-Yield Opportunity: {top['title']}",
            "description": f"Targeting {top['affected_customer_count']:,} customers with expected revenue potential of INR {top['estimated_revenue_potential']['expected']:,.2f}.",
            "target_url": "/campaigns",
            "opportunity_id": top["id"]
        })

    # 2. Product Velocity Drop Alert
    declining = [t for t in trends if t["status"] == "declining"]
    if declining:
        dec = declining[0]
        alerts.append({
            "id": f"ALERT_DROP_{dec['product_id']}_{ts_id}",
            "timestamp": now_str,
            "type": "VELOCITY_DECLINE",
            "severity": "MEDIUM",
            "title": f"Product Velocity Drop: {dec['product_name']}",
            "description": f"Weekly sales dropped from {dec['units_w3']} units (W-3) to {dec['units_w1']} units in W-1 ({dec['wow_change_w1']}% WoW change).",
            "target_url": "/products",
            "opportunity_id": "OPP_EARBUD_CROSSSELL"
        })

    # 3. Demand Surge Alert
    emerging = [t for t in trends if t["status"] == "emerging"]
    if emerging:
        em = emerging[0]
        alerts.append({
            "id": f"ALERT_SURGE_{em['product_id']}_{ts_id}",
            "timestamp": now_str,
            "type": "DEMAND_SURGE",
            "severity": "HIGH",
            "title": f"Emerging Product Demand Surge: {em['product_name']}",
            "description": f"Weekly velocity increased by +{em['wow_change_w1']}% WoW over recent transactions.",
            "target_url": "/products",
            "opportunity_id": "OPP_WATCH_SCALE_PROMO"
        })

    # 4. Secondary Opportunity Alert
    if len(opps) > 1:
        second = opps[1]
        alerts.append({
            "id": f"ALERT_OPP_SEC_{second['id']}_{ts_id}",
            "timestamp": now_str,
            "type": "SEGMENT_SIGNAL",
            "severity": "MEDIUM",
            "title": f"Commercial Signal: {second['title']}",
            "description": f"Affecting {second['affected_customer_count']:,} customers with priority score of {second['priority_score']:,.2f}.",
            "target_url": "/campaigns",
            "opportunity_id": second["id"]
        })

    # Save to file
    try:
        os.makedirs(os.path.dirname(ALERTS_FILE), exist_ok=True)
        with open(ALERTS_FILE, "w", encoding="utf-8") as f:
            json.dump(alerts, f, indent=2)
    except Exception as e:
        print(f"Warning: Could not save alerts to file: {e}")

    # Log to audit logger
    audit_logger.log_action(
        agent="OpportunityAgent",
        action="run_pipeline_refresh",
        input_summary="Opportunity detection pipeline triggered on-demand",
        output_summary=f"Discovered {len(opps)} opportunities & generated {len(alerts)} real-time alerts"
    )

    return alerts
