from pydantic import BaseModel
from typing import Dict, Any

class SystemStatsSchema(BaseModel):
    cpu_percent: float
    ram_used_mb: float
    ram_total_mb: float
    disk_used_gb: float
    disk_total_gb: float
    temps: Dict[str, Any] | None
