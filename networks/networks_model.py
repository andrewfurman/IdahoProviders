
from datetime import datetime
from typing import List
from dataclasses import dataclass

@dataclass
class Region:
    id: int
    name: str
    created_at: datetime
    updated_at: datetime

@dataclass
class Network:
    id: int
    code: str  # e.g., 'KCN', 'HNPN'
    name: str  # e.g., 'Kootenai Care Network'
    primary_regions: List[str]  # e.g., ['North & North-Central']
    created_at: datetime
    updated_at: datetime

@dataclass
class County:
    id: int
    name: str
    region_id: int
    created_at: datetime
    updated_at: datetime

@dataclass
class Hospital:
    id: int
    name: str
    region_id: int
    created_at: datetime
    updated_at: datetime

@dataclass
class CountyNetwork:
    id: int
    county_id: int
    network_id: int
    created_at: datetime

@dataclass
class HospitalNetwork:
    id: int
    hospital_id: int
    network_id: int
    created_at: datetime
