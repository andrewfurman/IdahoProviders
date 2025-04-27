
from dataclasses import dataclass
from datetime import date

@dataclass
class HospitalNetwork:
    id: int
    hospital_id: int
    network_id: int
    effective_date: date
    status: str
