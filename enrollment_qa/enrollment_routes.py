
from flask import Blueprint, render_template

enrollment_bp = Blueprint('enrollment', __name__)

@enrollment_bp.route('/enrollment-files')
def enrollment_files():
    return render_template('enrollment_files.html')
