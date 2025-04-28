
from .db import db
from datetime import datetime
import logging
from models.auth import User

logger = logging.getLogger(__name__)

class ProviderAudit(db.Model):
    """Audit log for provider changes"""
    __tablename__ = 'individual_provider_audit'
    
    audit_id = db.Column(db.Integer, primary_key=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('individual_providers.provider_id', ondelete='CASCADE'))
    field_updated = db.Column(db.Text, nullable=False)
    old_value = db.Column(db.Text)
    new_value = db.Column(db.Text)
    change_description = db.Column(db.Text)
    edit_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))

    # Relationships
    provider = db.relationship('IndividualProvider', backref=db.backref('audits', lazy='dynamic'))
    try:
        logger.debug("Setting up User relationship")
        user = db.relationship('models.auth.User', foreign_keys=[user_id])
        logger.debug("User relationship setup complete")
    except Exception as e:
        logger.error(f"Failed to setup User relationship: {str(e)}")
        raise
