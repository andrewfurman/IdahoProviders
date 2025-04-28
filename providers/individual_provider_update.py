
from flask import current_app, request, redirect, url_for, flash
from flask_login import current_user
from main import db
from models import IndividualProvider
from models.provider_audit import ProviderAudit

def update_individual_provider(provider_id):
    provider = db.session.query(IndividualProvider).get(provider_id)
    if provider is None:
        return {"error": "Provider not found"}, 404
    
    # Fields to track for audit
    fields_to_track = {
        'npi': 'NPI',
        'first_name': 'First Name',
        'last_name': 'Last Name', 
        'gender': 'Gender',
        'phone': 'Phone',
        'provider_type': 'Provider Type',
        'accepting_new_patients': 'Accepting New Patients',
        'specialties': 'Specialties',
        'board_certifications': 'Board Certifications',
        'languages': 'Languages',
        'address_line': 'Address',
        'city': 'City',
        'state': 'State',
        'zip': 'ZIP'
    }
    
    try:
        audit_records = []
        field_updates = []
        
        # First pass - collect all changes
        for field, display_name in fields_to_track.items():
            old_value = str(getattr(provider, field))
            new_value = str(request.form.get(field))
            
            # For boolean fields
            if field == 'accepting_new_patients':
                new_value = str(request.form.get(field) == 'true')
            
            if old_value != new_value:
                # Store the change
                field_updates.append((field, request.form.get(field), field == 'accepting_new_patients'))
                
                # Create audit record
                audit = ProviderAudit(
                    provider_id=provider_id,
                    field_updated=display_name,
                    old_value=old_value,
                    new_value=new_value,
                    change_description=f"Updated {display_name}",
                    user_id=current_user.id if current_user.is_authenticated else None
                )
                audit_records.append(audit)
        
        # Second pass - apply all changes if audit records were created successfully
        for audit in audit_records:
            try:
                db.session.add(audit)
                db.session.flush()  # Test if audit record can be created
            except Exception as e:
                db.session.rollback()
                current_app.logger.error(f"Failed to create audit record: {str(e)}")
                flash(f'Error creating audit record: {str(e)}')
                return redirect(url_for('providers.provider_detail', provider_id=provider_id))
        
        # Apply the actual field updates
        for field, value, is_boolean in field_updates:
            if is_boolean:
                setattr(provider, field, value == 'true')
            else:
                setattr(provider, field, value)
        
        db.session.commit()
        flash('Provider updated successfully')
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Failed to update provider: {str(e)}")
        flash(f'Error updating provider: {str(e)}')
        
    return redirect(url_for('providers.provider_detail', provider_id=provider_id))
