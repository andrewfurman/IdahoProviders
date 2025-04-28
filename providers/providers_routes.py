from flask import Blueprint, render_template, abort
from main import db
from models import IndividualProvider, MedicalGroup, Hospital, Network, ProviderGroup


providers_bp = Blueprint('providers', __name__, template_folder='templates')

@providers_bp.route('/individual_providers/<int:provider_id>')
def provider_detail(provider_id):
    provider = db.session.query(IndividualProvider).get(provider_id)
    if provider is None:
        abort(404)

    medical_groups = db.session.query(MedicalGroup)\
        .join(ProviderGroup, ProviderGroup.group_id == MedicalGroup.group_id)\
        .filter(ProviderGroup.provider_id == provider_id)\
        .all()

    return render_template('individual_provider_detail.html', provider=provider, medical_groups=medical_groups)

@providers_bp.route('/individual_providers/<int:provider_id>/update', methods=['POST'])
def update_provider(provider_id):
    provider = db.session.query(IndividualProvider).get(provider_id)
    if provider is None:
        abort(404)
        
    # Update provider fields from form data
    provider.npi = request.form.get('npi')
    provider.first_name = request.form.get('first_name')
    provider.last_name = request.form.get('last_name')
    provider.gender = request.form.get('gender')
    provider.phone = request.form.get('phone')
    provider.provider_type = request.form.get('provider_type')
    provider.accepting_new_patients = request.form.get('accepting_new_patients') == 'true'
    provider.specialties = request.form.get('specialties')
    provider.board_certifications = request.form.get('board_certifications')
    provider.languages = request.form.get('languages')
    provider.address_line = request.form.get('address_line')
    provider.city = request.form.get('city')
    provider.state = request.form.get('state')
    provider.zip = request.form.get('zip')

    try:
        db.session.commit()
        flash('Provider updated successfully')
    except:
        db.session.rollback()
        flash('Error updating provider')
        
    return redirect(url_for('providers.provider_detail', provider_id=provider_id))

@providers_bp.route('/medical_groups')
def medical_groups():
    groups = db.session.query(MedicalGroup).order_by(MedicalGroup.group_id).all()
    return render_template('medical_groups.html', medical_groups=groups)

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