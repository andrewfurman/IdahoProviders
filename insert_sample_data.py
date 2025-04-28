
import os
from main import db, app
from models.network import Network

def insert_networks():
    try:
        # Get existing network codes to avoid duplicates
        existing_codes = {n.code for n in Network.query.all()}
        
        networks_to_add = [
            {'code': 'KCN', 'name': 'Kootenai Care Network'},
            {'code': 'HNPN', 'name': 'Hometown North Provider Network'},
            {'code': 'CPN', 'name': 'Clearwater Provider Network'},
            {'code': 'SLHP', 'name': 'St. Luke\'s Health Partners'},
            {'code': 'HSWPN', 'name': 'Hometown South-West Provider Network'},
            {'code': 'IDID', 'name': 'Independent Doctors of Idaho'},
            {'code': 'MVN', 'name': 'Mountain View Network'},
            {'code': 'HEPN', 'name': 'Hometown East Provider Network'},
            {'code': 'PQA', 'name': 'Patient Quality Alliance'},
            {'code': 'MAHMO', 'name': 'True Blue HMO'},
            {'code': 'MAPPO', 'name': 'Secure Blue PPO'},
            {'code': 'MMCPHMO', 'name': 'True Blue Special Needs Plan'},
            {'code': 'MICRON', 'name': 'Micron CDHP/PPO'}
        ]

        # Filter and add networks one by one
        for network in networks_to_add:
            if network['code'] not in existing_codes:
                new_network = Network(code=network['code'], name=network['name'])
                db.session.add(new_network)
                existing_codes.add(network['code'])  # Update our tracking set
        
        db.session.commit()
        print("Networks inserted successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")
        db.session.rollback()

if __name__ == "__main__":
    with app.app_context():
        insert_networks()
