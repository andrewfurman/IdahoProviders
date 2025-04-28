import os
from main import db, app
from models.network import Network

def insert_networks():
    try:
        # Get existing network codes to avoid duplicates
        existing_codes = {n.code for n in Network.query.all()}
        networks = [
            Network(code='KCN', name='Kootenai Care Network'),
            Network(code='HNPN', name='Hometown North Provider Network'),
            Network(code='CPN', name='Clearwater Provider Network'),
            Network(code='SLHP', name='St. Luke\'s Health Partners'),
            Network(code='HSWPN', name='Hometown South-West Provider Network'),
            Network(code='IDID', name='Independent Doctors of Idaho'),
            Network(code='MVN', name='Mountain View Network'),
            Network(code='HEPN', name='Hometown East Provider Network'),
            Network(code='PQA', name='Patient Quality Alliance'),
            Network(code='MAHMO', name='True Blue HMO'),
            Network(code='MAPPO', name='Secure Blue PPO'),
            Network(code='MMCPHMO', name='True Blue Special Needs Plan'),
            Network(code='MICRON', name='Micron CDHP/PPO')
        ]

        for network in networks:
            # Only add if code doesn't already exist
            if network.code not in existing_codes:
                existing_codes.add(network.code)  # Update our tracking set
                db.session.add(network)

        db.session.commit()
        print("Networks inserted successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")
        db.session.rollback()

if __name__ == "__main__":
    with app.app_context():
        insert_networks()