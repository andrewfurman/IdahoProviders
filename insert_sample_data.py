import psycopg2
import os
from datetime import date
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from main import db
from models import WorkQueueItem
from datetime import datetime

def insert_sample_data():
    database_url = os.environ['DATABASE_URL']
    conn = psycopg2.connect(database_url)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    
    try:
        # Insert Networks
        networks = [
            (1, 'MAHMO', 'True Blue HMO'),
            (2, 'MAPPO', 'Secure Blue PPO'),
            (3, 'MMCPHMO', 'True Blue Special Needs Plan'),
            (4, 'MICRON', 'Micron CDHP/PPO'),
            (5, 'SLHP', 'St. Luke\'s Health Partners')
        ]
        for network in networks:
            cur.execute("""
                INSERT INTO networks (network_id, code, name)
                VALUES (%s, %s, %s)
                ON CONFLICT (network_id) DO NOTHING
            """, network)

        # Insert Medical Groups
        groups = [
            (1, 'Nexus Wound Consultants', 'NWC123', '1555 W Shoreline Dr', 'Boise', 'ID', '83702'),
            (2, 'St Lukes Clinic', 'SLC456', '2619 W Fairview Ave', 'Boise', 'ID', '83702'),
            (3, 'Medical Directors of Idaho', 'MDI789', '3550 W Americana Ter', 'Boise', 'ID', '83706')
        ]
        for group in groups:
            cur.execute("""
                INSERT INTO medical_groups (group_id, name, tax_id, address_line, city, state, zip)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (group_id) DO NOTHING
            """, group)

        # Insert Hospitals
        hospitals = [
            (1, 'St Lukes Regional Medical Center', 'SLRMC001', '190 E Bannock St', 'Boise', 'ID', '83712'),
            (2, 'Saint Alphonsus Regional Medical Center', 'SARMC002', '1055 N Curtis Rd', 'Boise', 'ID', '83706')
        ]
        for hospital in hospitals:
            cur.execute("""
                INSERT INTO hospitals (hospital_id, name, ccn, address_line, city, state, zip)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (hospital_id) DO NOTHING
            """, hospital)

        # Insert Individual Providers
        providers = [
            (1, '1720020076', 'Stacey', 'Raybuck', 'F', '830-285-8882', 'Professional', True, 'Family Medicine', 'Family Medicine', '', '1555 W Shoreline Dr Ste 100', 'Boise', 'ID', '83702'),
            (2, '1124681085', 'Mark', 'Hopkins', 'M', '208-706-2663', 'Professional', True, 'Emergency Medicine,Sports Medicine', 'Emergency Medicine,Sports Medicine', 'Spanish', '703 S Americana Blvd Ste 120', 'Boise', 'ID', '83702'),
            (3, '1831539220', 'Adam', 'Schwind', 'M', '208-615-4940', 'Professional', True, 'Family Medicine,Internal Medicine', 'Family Medicine', 'Spanish', '3550 W Americana Ter', 'Boise', 'ID', '83706')
        ]
        for provider in providers:
            cur.execute("""
                INSERT INTO individual_providers (provider_id, npi, first_name, last_name, gender, phone, provider_type, accepting_new_patients, specialties, board_certifications, languages, address_line, city, state, zip)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (provider_id) DO NOTHING
            """, provider)

        # Insert Provider-Group Relationships
        provider_groups = [
            (1, 1, 1, date(2023, 1, 1), None, True),
            (2, 2, 2, date(2023, 1, 1), None, True),
            (3, 3, 3, date(2023, 1, 1), None, True)
        ]
        for pg in provider_groups:
            cur.execute("""
                INSERT INTO individual_provider_medical_group (id, provider_id, group_id, start_date, end_date, primary_flag)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (provider_id, group_id) DO NOTHING
            """, pg)

        # Insert Group-Hospital Relationships
        group_hospitals = [
            (1, 2, 1, 'Full'),
            (2, 2, 2, 'Full')
        ]
        for gh in group_hospitals:
            cur.execute("""
                INSERT INTO medical_group_hospital (id, group_id, hospital_id, privilege_type)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (group_id, hospital_id) DO NOTHING
            """, gh)

        # Insert Hospital-Network Relationships
        hospital_networks = [
            (1, 1, 1, date(2023, 1, 1), 'Active'),
            (1, 1, 2, date(2023, 1, 1), 'Active'),
            (2, 2, 1, date(2023, 1, 1), 'Active')
        ]
        for hn in hospital_networks:
            cur.execute("""
                INSERT INTO hospital_network (id, hospital_id, network_id, effective_date, status)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (hospital_id, network_id) DO NOTHING
            """, hn)

        print("Sample data inserted successfully!")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        
    finally:
        cur.close()
        conn.close()

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
    insert_sample_data()
    insert_work_queue_items()