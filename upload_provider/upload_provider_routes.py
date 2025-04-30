
from flask import Blueprint, render_template

upload_provider_bp = Blueprint('upload_provider', __name__, template_folder='templates')

@upload_provider_bp.route('/upload')
def upload():
    return render_template('upload_provider.html')
