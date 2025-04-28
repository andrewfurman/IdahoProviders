
from .db import db
from datetime import datetime

class WorkQueueItem(db.Model):
    __tablename__ = "work_queue_items"

    queue_id = db.Column(db.Integer, primary_key=True)
    provider_id = db.Column(db.Integer,
                          db.ForeignKey("individual_providers.provider_id",
                                       ondelete="CASCADE"),
                          nullable=False)
    issue_type = db.Column(db.String(40), nullable=False)
    description = db.Column(db.Text, nullable=False)
    recommended_action = db.Column(db.Text)
    status = db.Column(db.String(20), default="open", nullable=False)
    assigned_user_id = db.Column(db.Integer,
                                db.ForeignKey("users.id",
                                             ondelete="SET NULL"))
    created_by_user_id = db.Column(db.Integer,
                                  db.ForeignKey("users.id",
                                              ondelete="SET NULL"))
    created_at = db.Column(db.DateTime,
                          nullable=False,
                          default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,
                          nullable=False,
                          default=datetime.utcnow,
                          onupdate=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)

    # relationships
    provider = db.relationship("IndividualProvider")
    assigned_user = db.relationship("User",
                                  foreign_keys=[assigned_user_id])
    created_by_user = db.relationship("User",
                                    foreign_keys=[created_by_user_id])
