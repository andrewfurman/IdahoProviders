
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Provider:
    provider_id: int
    npi: str
    first_name: str
    last_name: str
    gender: str
    phone: str
    provider_type: str
    accepting_new_patients: bool
    specialties: str
    board_certifications: str
    languages: str
    address_line: str
    city: str
    state: str
    zip: str

    @staticmethod
    def get_all_providers() -> List['Provider']:
        """
        Get all providers from the database
        Returns a list of Provider objects
        """
        # Placeholder for database implementation
        return []

    @staticmethod
    def get_provider_by_id(provider_id: int) -> Optional['Provider']:
        """
        Get a specific provider by ID
        Returns a Provider object or None if not found
        """
        # Placeholder for database implementation
        return None

    def to_dict(self) -> dict:
        """
        Convert Provider object to dictionary
        Useful for JSON serialization
        """
        return {
            'provider_id': self.provider_id,
            'npi': self.npi,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'gender': self.gender,
            'phone': self.phone,
            'provider_type': self.provider_type,
            'accepting_new_patients': self.accepting_new_patients,
            'specialties': self.specialties,
            'board_certifications': self.board_certifications,
            'languages': self.languages,
            'address_line': self.address_line,
            'city': self.city,
            'state': self.state,
            'zip': self.zip
        }
