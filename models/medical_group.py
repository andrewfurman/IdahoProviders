
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class MedicalGroup:
    group_id: int
    name: str
    tax_id: str
    address_line: str
    city: str
    state: str
    zip: str
