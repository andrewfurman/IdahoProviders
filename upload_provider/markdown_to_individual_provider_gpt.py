
from flask import current_app
from openai import OpenAI
from models.provider import IndividualProvider
from models.db import db
from providers.individual_provider_update import update_individual_provider
import json

client = OpenAI()  # uses OPENAI_API_KEY from env

def markdown_to_individual_provider_gpt(provider_id: int) -> bool:
    """
    Updates provider record by analyzing markdown text with GPT.
    
    Args:
        provider_id: Database ID of the provider record
        
    Returns:
        bool: True if update successful, False otherwise
    """
    logger = current_app.logger
    
    # Get provider record
    provider = db.session.query(IndividualProvider).get(provider_id)
    if not provider:
        logger.error(f"Provider not found with ID: {provider_id}")
        return False
        
    if not provider.provider_enrollment_form_markdown_text:
        logger.error(f"No markdown text found for provider ID: {provider_id}")
        return False

    try:
        # Ask GPT to extract provider fields
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": """Extract provider information from the markdown text into a JSON object with these fields:
                        - npi (string): National Provider Identifier
                        - first_name (string): Provider's first name
                        - last_name (string): Provider's last name
                        - gender (string): Provider's gender (M/F)
                        - phone (string): Contact phone number
                        - provider_type (string): Type of provider
                        - accepting_new_patients (boolean): Whether accepting new patients
                        - specialties (string): Medical specialties
                        - board_certifications (string): Board certifications
                        - languages (string): Languages spoken
                        - address_line (string): Street address
                        - city (string): City
                        - state (string): State
                        - zip (string): ZIP code"""
                },
                {
                    "role": "user", 
                    "content": provider.provider_enrollment_form_markdown_text
                }
            ],
            response_format={"type": "json_object"}
        )

        # Parse GPT response
        provider_data = json.loads(response.choices[0].message.content)
        
        # Simulate form submission by creating a request context
        from flask import Request, request
        class DummyRequest:
            form = provider_data
        
        # Store current request
        old_request = request._get_current_object() if request else None
        
        # Use dummy request
        request._local.request = DummyRequest()
        
        # Update provider using existing function
        result = update_individual_provider(provider_id)
        
        # Restore original request
        if old_request:
            request._local.request = old_request
            
        return True

    except Exception as e:
        logger.error(f"Error updating provider from markdown: {str(e)}")
        return False
