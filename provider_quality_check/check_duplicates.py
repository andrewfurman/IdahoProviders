
from typing import Dict
from models.db import db
from models.provider import IndividualProvider
from sqlalchemy import func

def check_provider_duplicates(provider_id: int) -> Dict:
    """
    Check for duplicate providers based on various matching criteria
    Returns JSON with duplicate status and IDs of any duplicates found
    """
    # Get provider details
    provider = db.session.query(IndividualProvider).get(provider_id)

    if not provider:
        return {
            "status": "No Provider Found",
            "duplicate_ids": []
        }

    # Check for exact duplicates (same NPI)
    exact_duplicates = db.session.query(IndividualProvider.provider_id)\
        .filter(IndividualProvider.npi == provider.npi)\
        .filter(IndividualProvider.provider_id != provider_id)\
        .all()

    if exact_duplicates:
        return {
            "status": "Exact Duplicate Found",
            "duplicate_ids": [d[0] for d in exact_duplicates]
        }

    # Check for partial duplicates (same name + location or phone)
    partial_duplicates = db.session.query(IndividualProvider.provider_id)\
        .filter(IndividualProvider.provider_id != provider_id)\
        .filter(func.lower(IndividualProvider.first_name) == func.lower(provider.first_name))\
        .filter(func.lower(IndividualProvider.last_name) == func.lower(provider.last_name))\
        .filter(
            db.or_(
                db.and_(
                    IndividualProvider.phone == provider.phone,
                    IndividualProvider.phone != None
                ),
                db.and_(
                    IndividualProvider.address_line == provider.address_line,
                    IndividualProvider.city == provider.city,
                    IndividualProvider.state == provider.state,
                    IndividualProvider.zip == provider.zip,
                    IndividualProvider.address_line != None
                )
            )
        ).all()

    if partial_duplicates:
        return {
            "status": "Partial Duplicate Found",
            "duplicate_ids": [d[0] for d in partial_duplicates]
        }

    return {
        "status": "No Duplicate Found",
        "duplicate_ids": []
    }