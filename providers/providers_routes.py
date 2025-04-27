from flask import Blueprint, render_template
from flask_sqlalchemy import SQLAlchemy
from models import IndividualProvider, Network, Hospital

providers_bp = Blueprint('providers', __name__, template_folder='templates')
db = SQLAlchemy()

@providers_bp.route('/')
@providers_bp.route('/individual_providers')
def providers():
    providers = db.session.query(IndividualProvider).all()
    return render_template('individual_providers.html', providers=providers)

@providers_bp.route('/networks')
def networks():
    networks = db.session.query(Network).order_by(Network.network_id).all()
    return render_template('networks.html', networks=networks)

@providers_bp.route('/hospitals')
def hospitals():
    hospitals = db.session.query(Hospital).order_by(Hospital.hospital_id).all()
    return render_template('hospitals.html', hospitals=hospitals)