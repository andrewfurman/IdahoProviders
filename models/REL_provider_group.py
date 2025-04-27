
from dataclasses import dataclass
from datetime import date

@dataclass
class ProviderGroup:
    id: int
    provider_id: int
    group_id: int
    start_date: date
    end_date: date
    primary_flag: bool
