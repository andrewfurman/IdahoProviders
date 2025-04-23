
from flask import Blueprint, render_template

networks_bp = Blueprint('networks', __name__, template_folder='templates')

@networks_bp.route('/networks')
def networks():
    return render_template('networks.html')
