from flask import Blueprint, render_template, request, flash, current_app
from werkzeug.utils import secure_filename

from .image_to_markdown_gpt import image_to_markdown  # local import
from .provider_to_facets import convert_and_save_provider_facets

upload_provider_bp = Blueprint(
    "upload_provider",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="/upload"
)

@upload_provider_bp.get("/")
def upload():                                    # GET /upload/
    return render_template("upload_provider.html")

@upload_provider_bp.post("/process")
def process_image():
    uploaded_file = request.files.get("image_file")
    if not uploaded_file:
        return {"error": "No file provided"}, 400

    try:
        markdown = image_to_markdown(uploaded_file)
        return {"markdown": markdown}
    except Exception as err:
        return {"error": str(err)}, 500

@upload_provider_bp.post("/extract_provider_info/<int:provider_id>")
def extract_provider_info(provider_id):
    try:
        from .markdown_to_individual_provider_gpt import markdown_to_individual_provider_gpt
        success = markdown_to_individual_provider_gpt(provider_id)
        return {"success": success}
    except Exception as err:
        current_app.logger.error(f"Error extracting provider info: {str(err)}")
        return {"error": str(err)}, 500

@upload_provider_bp.post("/convert_to_facets/<int:provider_id>")
def convert_to_facets(provider_id):
    try:
        current_app.logger.debug(f"Starting Facets conversion for provider {provider_id}")
        from flask_login import current_user
        
        # Import here to avoid circular imports
        from models.provider import IndividualProvider
        provider = IndividualProvider.query.get(provider_id)
        if not provider:
            current_app.logger.error(f"Provider {provider_id} not found")
            return {"error": f"Provider {provider_id} not found"}, 404
            
        result = convert_and_save_provider_facets(provider_id, current_user)
        current_app.logger.debug(f"Conversion result: {result}")
        
        if isinstance(result, dict):
            if result.get('status') == 'success':
                from .facets_json_to_markdown import convert_facets_json_to_markdown
                try:
                    md_result = convert_facets_json_to_markdown(provider_id, current_user)
                    current_app.logger.debug(f"Markdown conversion result: {md_result}")
                except Exception as md_err:
                    current_app.logger.error(f"Markdown conversion failed: {str(md_err)}")
                    # Continue even if markdown fails - facets data was saved
                return {"success": True, "result": result}
            else:
                return {"error": "Conversion failed", "details": str(result)}, 400
        else:
            return {"error": "Invalid conversion result", "details": str(result)}, 400
            
    except Exception as err:
        import traceback
        error_details = traceback.format_exc()
        current_app.logger.error(f"Error converting to Facets: {str(err)}")
        current_app.logger.error(f"Traceback: {error_details}")
        return {"error": "Server error", "details": str(err)}, 500
        current_app.logger.error(f"Traceback: {error_details}")
        return {"error": str(err), "details": error_details}, 500

@upload_provider_bp.post("/create_provider")
def create_provider():
    markdown_text = request.form.get("markdown_text")
    image_file = request.files.get("image_file")
    
    if not markdown_text:
        return {"error": "No markdown text provided"}, 400

    try:
        from .create_individual_provider_from_image import create_individual_provider_from_markdown
        
        provider = create_individual_provider_from_markdown(markdown_text, image_file)
        if not provider:
            current_app.logger.error("Provider creation returned None")
            return "Provider creation failed - no provider returned", 500
            
        current_app.logger.info(f"Provider created successfully with ID: {provider.provider_id}")
        return {"provider_id": provider.provider_id}
    except Exception as err:
        import traceback
        current_app.logger.error(f"Error creating provider: {str(err)}")
        current_app.logger.error(f"Traceback: {traceback.format_exc()}")
        return str(err), 500