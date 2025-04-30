
from datetime import datetime
from models.db import db
from models.provider import IndividualProvider

def create_individual_provider_from_markdown(markdown_text: str) -> IndividualProvider:
    """
    Creates a new individual provider record from markdown text with placeholder values.
    Only populates provider ID and markdown text, with placeholder values for required fields.
    
    Args:
        markdown_text: The markdown text generated from the image
        
    Returns:
        IndividualProvider: The newly created provider record
    """
    
    # Create timestamp for the placeholder last name
    current_time = datetime.now().strftime("%I:%M %p on %B %d, %Y")
    
    # Create new provider with required placeholder values
    new_provider = IndividualProvider(
        npi="To be assigned",
        first_name="New Provider from Image",
        last_name=f"Created at {current_time}",
        provider_enrollment_form_markdown_text=markdown_text
    )
    
    # Add and commit to database
    db.session.add(new_provider)
    db.session.commit()
    
    return new_provider
