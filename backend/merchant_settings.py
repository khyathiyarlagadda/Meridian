import os
import json
from typing import Dict, Any

SETTINGS_FILE = r"C:\Dev\Meridian\data\merchant_settings.json"

DEFAULT_SETTINGS: Dict[str, Any] = {
    "max_discount_percent": 25.0,
    "max_campaign_budget": 50000.0,
    "max_campaigns_per_day": 10,
    "auto_approve_analysis": False,
    "auto_approve_draft_campaigns": False,
    "require_approval_to_launch": True
}

class MerchantSettingsManager:
    def __init__(self, filepath: str = SETTINGS_FILE):
        self.filepath = filepath
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.filepath):
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            self.save_settings(DEFAULT_SETTINGS)

    def get_settings(self) -> Dict[str, Any]:
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Enforce locked human-in-the-loop requirement
                    data["require_approval_to_launch"] = True
                    return data
            except Exception:
                pass
        return DEFAULT_SETTINGS.copy()

    def save_settings(self, new_settings: Dict[str, Any]) -> Dict[str, Any]:
        current = self.get_settings()
        current.update({
            "max_discount_percent": float(new_settings.get("max_discount_percent", current["max_discount_percent"])),
            "max_campaign_budget": float(new_settings.get("max_campaign_budget", current["max_campaign_budget"])),
            "max_campaigns_per_day": int(new_settings.get("max_campaigns_per_day", current["max_campaigns_per_day"])),
            "auto_approve_analysis": bool(new_settings.get("auto_approve_analysis", current["auto_approve_analysis"])),
            "auto_approve_draft_campaigns": bool(new_settings.get("auto_approve_draft_campaigns", current["auto_approve_draft_campaigns"])),
            "require_approval_to_launch": True  # Always locked to True
        })

        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(current, f, indent=2)

        return current

merchant_settings_manager = MerchantSettingsManager()
