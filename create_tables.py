import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_tables():
    database_url = os.environ['DATABASE_URL']

    conn = psycopg2.connect(database_url)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    try:
        # Create users table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                first_name VARCHAR(120),
                last_name VARCHAR(120),
                role VARCHAR(50)
            )
        """)

        # Create core tables
        cur.execute("""
            CREATE TABLE IF NOT EXISTS individual_providers (
                provider_id SERIAL PRIMARY KEY,
                npi TEXT NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                gender TEXT,
                phone TEXT,
                provider_type TEXT,
                accepting_new_patients BOOLEAN,
                specialties TEXT,
                board_certifications TEXT,
                languages TEXT,
                address_line TEXT,
                city TEXT,
                state TEXT,
                zip TEXT
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS individual_provider_audit (
                audit_id SERIAL PRIMARY KEY,
                provider_id INTEGER,
                field_updated TEXT NOT NULL,
                old_value TEXT,
                new_value TEXT,
                change_description TEXT,
                edit_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                user_id INTEGER,
                FOREIGN KEY (provider_id) REFERENCES individual_providers(provider_id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS medical_groups (
                group_id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                tax_id TEXT,
                address_line TEXT,
                city TEXT,
                state TEXT,
                zip TEXT
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS hospitals (
                hospital_id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                ccn TEXT,
                address_line TEXT,
                city TEXT,
                state TEXT,
                zip TEXT
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS networks (
                network_id SERIAL PRIMARY KEY,
                code TEXT NOT NULL,
                name TEXT NOT NULL
            )
        """)

        # Create relationship tables
        cur.execute("""
            CREATE TABLE IF NOT EXISTS individual_provider_medical_group (
                id SERIAL PRIMARY KEY,
                provider_id INTEGER REFERENCES individual_providers(provider_id),
                group_id INTEGER REFERENCES medical_groups(group_id),
                start_date DATE,
                end_date DATE,
                primary_flag BOOLEAN,
                UNIQUE(provider_id, group_id)
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS medical_group_hospital (
                id SERIAL PRIMARY KEY,
                group_id INTEGER REFERENCES medical_groups(group_id),
                hospital_id INTEGER REFERENCES hospitals(hospital_id),
                privilege_type TEXT,
                UNIQUE(group_id, hospital_id)
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS hospital_network (
                id SERIAL PRIMARY KEY,
                hospital_id INTEGER REFERENCES hospitals(hospital_id),
                network_id INTEGER REFERENCES networks(network_id),
                effective_date DATE,
                status TEXT,
                UNIQUE(hospital_id, network_id)
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS medical_group_network (
                id SERIAL PRIMARY KEY,
                group_id INTEGER REFERENCES medical_groups(group_id),
                network_id INTEGER REFERENCES networks(network_id),
                effective_date DATE,
                status TEXT,
                UNIQUE(group_id, network_id)
            )
        """)

        # Create work queue table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS work_queue_items (
                queue_id SERIAL PRIMARY KEY,
                provider_id INTEGER NOT NULL
                    REFERENCES individual_providers(provider_id) ON DELETE CASCADE,
                issue_type TEXT NOT NULL,
                description TEXT NOT NULL,
                action_type VARCHAR(20) NOT NULL DEFAULT 'update_field',
                field_name TEXT,
                new_value TEXT,
                duplicate_ids INTEGER[],
                recommended_action TEXT,
                status TEXT NOT NULL DEFAULT 'open',
                assigned_user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
                created_by_user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                resolved_at TIMESTAMP
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS enrollment_files (
                id SERIAL PRIMARY KEY,
                received_date TEXT,
                file_name TEXT,
                status TEXT,
                error_message TEXT,
                source_system TEXT,
                file_type TEXT,
                update_date TEXT,
                updated_by_user INTEGER REFERENCES users(id)
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS members (
                member_id SERIAL PRIMARY KEY,
                policyholder_id INTEGER REFERENCES members(member_id),
                relationship TEXT,
                ssn TEXT,
                date_of_birth TEXT,
                address_line1 TEXT,
                address_line2 TEXT,
                city TEXT,
                state TEXT,
                zip TEXT,
                pcp_id INTEGER REFERENCES individual_providers(provider_id),
                eligibility_status TEXT,
                eligibility_start TIMESTAMP,
                eligibility_end TIMESTAMP,
                plan_id TEXT,
                source_enrollment_file_id INTEGER REFERENCES enrollment_files(id) ON DELETE CASCADE,
                update_date TEXT,
                updated_by_user INTEGER REFERENCES users(id)
            )
        """)

        print("All tables created successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    create_tables()