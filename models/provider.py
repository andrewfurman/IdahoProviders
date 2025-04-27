from . import db

class IndividualProvider(db.Model):
    __tablename__ = 'individual_providers'

    provider_id = db.Column(db.Integer, primary_key=True)
    npi = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    gender = db.Column(db.String)
    phone = db.Column(db.String)
    provider_type = db.Column(db.String)
    accepting_new_patients = db.Column(db.Boolean)
    specialties = db.Column(db.String)
    board_certifications = db.Column(db.String)
    languages = db.Column(db.String)
    address_line = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    zip = db.Column(db.String)

    def to_dict(self):
        """
        Convert IndividualProvider object to dictionary
        Useful for JSON serialization
        """
        return {
            'provider_id': self.provider_id,
            'npi': self.npi,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'gender': self.gender,
            'phone': self.phone,
            'provider_type': self.provider_type,
            'accepting_new_patients': self.accepting_new_patients,
            'specialties': self.specialties,
            'board_certifications': self.board_certifications,
            'languages': self.languages,
            'address_line': self.address_line,
            'city': self.city,
            'state': self.state,
            'zip': self.zip
        }