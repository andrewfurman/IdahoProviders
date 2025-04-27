
from dataclasses import dataclass
from datetime import date

@dataclass
class GroupNetwork:
    id: int
    group_id: int
    network_id: int
    effective_date: date
    status: str
