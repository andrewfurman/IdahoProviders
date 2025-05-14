from . import db


class EnrollmentFile(db.Model):
    '''Represents a raw enrollment file that was ingested into the system.'''
    __tablename__ = 'enrollment_files'

    id = db.Column(db.Integer, primary_key=True)
    received_date = db.Column(db.Text)          # e.g. '2025‑05‑14T13:22:01Z'
    file_name = db.Column(db.Text)
    status = db.Column(db.Text)                 # e.g. 'RECEIVED', 'PROCESSED', 'ERROR'
    error_message = db.Column(db.Text)
    source_system = db.Column(db.Text)          # e.g. 'On‑Exchange', 'Employer Portal'
    file_type = db.Column(db.Text)              # e.g. '834‑EDI', 'CSV', 'JSON'
    update_date = db.Column(db.Text)            # last time any metadata was updated
    updated_by_user = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Back‑reference: one file may spawn many members
    members = db.relationship('Member', backref='source_enrollment_file', lazy=True)

    def __repr__(self):
        return f"<EnrollmentFile {self.id} – {self.file_name}>"


class Member(db.Model):
    '''Member or dependent enrolled in a health‑insurance plan.'''
    __tablename__ = 'members'

    member_id = db.Column(db.Integer, primary_key=True)

    # Self‑join: if this row is the policyholder the field is NULL;
    # otherwise it points to the policyholder's member_id
    policyholder_id = db.Column(db.Integer, db.ForeignKey('members.member_id'))
    relationship = db.Column(db.Text)           # 'self', 'spouse', 'child', 'other'

    ssn = db.Column(db.Text)                    # Social Security Number
    date_of_birth = db.Column(db.Text)          # ISO string or free‑form

    address_line1 = db.Column(db.Text)
    address_line2 = db.Column(db.Text)
    city = db.Column(db.Text)
    state = db.Column(db.Text)
    zip = db.Column(db.Text)

    # Primary‑care provider
    pcp_id = db.Column(db.Integer, db.ForeignKey('individual_providers.provider_id'))

    eligibility_status = db.Column(db.Text)     # 'active', 'pending', 'terminated'
    eligibility_start = db.Column(db.DateTime)
    eligibility_end = db.Column(db.DateTime)

    plan_id = db.Column(db.Text)

    # Traceability back to the file that originated this row
    source_enrollment_file_id = db.Column(db.Integer, db.ForeignKey('enrollment_files.id'))

    update_date = db.Column(db.Text)
    updated_by_user = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Relationships
    policyholder = db.relationship('Member', remote_side=[member_id], backref='dependents', lazy=True)
    pcp = db.relationship('IndividualProvider', lazy=True)
    updated_by = db.relationship('User', lazy=True)

    def __repr__(self):
        return f"<Member {self.member_id} – {self.relationship}>"

    def to_dict(self):
        '''Convenience method for JSON serialization.'''
        return {
            'member_id': self.member_id,
            'policyholder_id': self.policyholder_id,
            'relationship': self.relationship,
            'ssn': self.ssn,
            'date_of_birth': self.date_of_birth,
            'address_line1': self.address_line1,
            'address_line2': self.address_line2,
            'city': self.city,
            'state': self.state,
            'zip': self.zip,
            'pcp_id': self.pcp_id,
            'eligibility_status': self.eligibility_status,
            'eligibility_start': self.eligibility_start.isoformat() if self.eligibility_start else None,
            'eligibility_end': self.eligibility_end.isoformat() if self.eligibility_end else None,
            'plan_id': self.plan_id,
            'source_enrollment_file_id': self.source_enrollment_file_id,
            'update_date': self.update_date,
            'updated_by_user': self.updated_by_user,
        }