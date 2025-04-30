from flask import Blueprint, render_template, request, flash
from werkzeug.utils import secure_filename

from .image_to_markdown_gpt import image_to_markdown  # local import

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

@upload_provider_bp.post("/create_provider")
def create_provider():
    markdown_text = request.json.get("markdown_text")
    if not markdown_text:
        return {"error": "No markdown text provided"}, 400

    try:
        from .create_individual_provider_from_image import create_individual_provider_from_markdown
        provider = create_individual_provider_from_markdown(markdown_text)
        return {"provider_id": provider.provider_id}
    except Exception as err:
        return {"error": str(err)}, 500