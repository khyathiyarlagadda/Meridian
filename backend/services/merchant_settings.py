import os
import json
from typing import Dict, Any
from services.supabase_db import get_merchant_settings as db_get_settings, save_merchant_settings as db_save_settings

DEFAULT_SETTINGS: Dict[str, Any] = {
    "max_discount_percent": 25.0,
    "max_campaign_budget": 50000.0,
    "max_campaigns_per_day": 10,
    "auto_approve_analysis": False,
    "auto_approve_draft_campaigns": False,
    "require_approval_to_launch": True
}

class MerchantSettingsManager:
    def get_settings(self) -> Dict[str, Any]:
        data = db_get_settings()
        data["require_approval_to_launch"] = True  # Always enforce human-in-the-loop requirement
        return data

    def save_settings(self, new_settings: Dict[str, Any]) -> Dict[str, Any]:
        updated = {
            "max_discount_percent": float(new_settings.get("max_discount_percent", 25.0)),
            "max_campaign_budget": float(new_settings.get("max_campaign_budget", 50000.0)),
            "max_campaigns_per_day": int(new_settings.get("max_campaigns_per_day", 10)),
            "auto_approve_analysis": False,
            "auto_approve_draft_campaigns": False,
            "require_approval_to_launch": True
        }
        return db_save_settings(updated)

merchant_settings_manager = MerchantSettingsManager()
