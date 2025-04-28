import psycopg2
import os
from datetime import date
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from main import db
from models import WorkQueueItem
from datetime import datetime

def insert_work_queue_items():
    try:
        # Create work queue items
        queue_items = [
            WorkQueueItem(
                queue_id=1,
                provider_id=1,
                issue_type='duplicate',
                description='Provider has similar name and credentials to Dr. S. Raybuck in Arizona - potential duplicate record',
                recommended_action='Review and compare records to confirm if duplicate',
                status='open',
                assigned_user_id=1,
                created_by_user_id=1,
                created_at=datetime.utcnow()
            ),
            WorkQueueItem(
                queue_id=2,
                provider_id=2,
                issue_type='bad_npi',
                description='NPI registry shows different specialty than what is listed in our database',
                recommended_action='Verify NPI information and update specialty if needed',
                status='open',
                assigned_user_id=1,
                created_by_user_id=1,
                created_at=datetime.utcnow()
            ),
            WorkQueueItem(
                queue_id=3,
                provider_id=3,
                issue_type='sanction',
                description='Name appears similar to entry on HHS sanction list - requires verification',
                recommended_action='Cross reference with official HHS sanction database',
                status='open',
                assigned_user_id=1,
                created_by_user_id=1,
                created_at=datetime.utcnow()
            )
        ]

        for item in queue_items:
            # Add if not exists
            existing_item = WorkQueueItem.query.get(item.queue_id)
            if not existing_item:
                db.session.add(item)

        db.session.commit()
        print("Work queue items created successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")
        db.session.rollback()

if __name__ == "__main__":
    insert_work_queue_items()