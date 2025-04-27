
from dataclasses import dataclass

@dataclass
class GroupHospital:
    id: int
    group_id: int
    hospital_id: int
    privilege_type: str
