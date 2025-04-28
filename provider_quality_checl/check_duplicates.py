
from typing import Dict, List
from models.db import db

def check_provider_duplicates(provider_id: int) -> Dict:
    """
    Check for duplicate providers based on various matching criteria
    Returns JSON with duplicate status and IDs of any duplicates found
    """
    # Get provider details
    provider = db.session.execute("""
        SELECT npi, first_name, last_name, phone, address_line, city, state, zip
        FROM individual_providers 
        WHERE provider_id = :id
    """, {'id': provider_id}).fetchone()
    
    if not provider:
        return {
            "status": "No Provider Found",
            "duplicate_ids": []
        }

    # Check for exact duplicates (same NPI)
    exact_duplicates = db.session.execute("""
        SELECT provider_id 
        FROM individual_providers
        WHERE npi = :npi 
        AND provider_id != :id
    """, {'npi': provider.npi, 'id': provider_id}).fetchall()

    if exact_duplicates:
        return {
            "status": "Exact Duplicate Found",
            "duplicate_ids": [d[0] for d in exact_duplicates]
        }

    # Check for partial duplicates (same name + location or phone)
    partial_duplicates = db.session.execute("""
        SELECT provider_id
        FROM individual_providers
        WHERE provider_id != :id
        AND LOWER(first_name) = LOWER(:first_name)
        AND LOWER(last_name) = LOWER(:last_name)
        AND (
            (phone = :phone AND phone IS NOT NULL)
            OR (
                address_line = :address_line 
                AND city = :city 
                AND state = :state 
                AND zip = :zip
                AND address_line IS NOT NULL
            )
        )
    """, {
        'id': provider_id,
        'first_name': provider.first_name,
        'last_name': provider.last_name,
        'phone': provider.phone,
        'address_line': provider.address_line,
        'city': provider.city,
        'state': provider.state,
        'zip': provider.zip
    }).fetchall()

    if partial_duplicates:
        return {
            "status": "Partial Duplicate Found",
            "duplicate_ids": [d[0] for d in partial_duplicates]
        }

    return {
        "status": "No Duplicate Found",
        "duplicate_ids": []
    }
