import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

AUDIT_FILE = r"C:\Dev\Meridian\data\audit_log.json"

class AuditLogger:
    def __init__(self, filepath: str = AUDIT_FILE):
        self.filepath = filepath
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        self.logs: List[Dict[str, Any]] = self._load_logs()

    def _load_logs(self) -> List[Dict[str, Any]]:
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def _save_logs(self):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self.logs, f, indent=2)

    def log_action(
        self,
        agent: str,
        action: str,
        input_summary: str,
        output_summary: str,
        approver: Optional[str] = None
    ) -> Dict[str, Any]:
        entry = {
            "id": len(self.logs) + 1,
            "timestamp": datetime.now().isoformat(),
            "agent": agent,
            "action": action,
            "input_summary": input_summary,
            "output_summary": output_summary,
            "approver": approver
        }
        self.logs.append(entry)
        self._save_logs()
        return entry

    def get_logs(self) -> List[Dict[str, Any]]:
        return self.logs

audit_logger = AuditLogger()
