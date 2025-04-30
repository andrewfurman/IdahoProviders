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
def process_image():                             # POST /upload/process
    uploaded_file = request.files.get("image_file")
    if not uploaded_file:
        flash("Please choose a file first.", "error")
        return render_template("upload_provider.html")

    # Optional: keep a copy on disk if you need auditing
    # filename = secure_filename(uploaded_file.filename)
    # uploaded_file.save(os.path.join(current_app.instance_path, filename))

    try:
        markdown = image_to_markdown(uploaded_file)
    except Exception as err:
        flash(f"Extraction failed: {err}", "error")
        return render_template("upload_provider.html")

    return render_template("upload_provider.html", markdown=markdown)