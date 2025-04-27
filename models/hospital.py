
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Hospital:
    hospital_id: int
    name: str
    ccn: str
    address_line: str
    city: str
    state: str
    zip: str
