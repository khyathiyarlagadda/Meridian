import os
from typing import List, Dict, Any, Optional
from services.supabase_db import get_audit_logs, log_audit_entry

class AuditLogger:
    def log_action(
        self,
        agent: str,
        action: str,
        input_summary: str,
        output_summary: str,
        approver: Optional[str] = None
    ) -> Dict[str, Any]:
        return log_audit_entry(
            agent=agent,
            action=action,
            input_summary=input_summary,
            output_summary=output_summary,
            approver=approver
        )

    def get_logs(self) -> List[Dict[str, Any]]:
        return get_audit_logs()

audit_logger = AuditLogger()
