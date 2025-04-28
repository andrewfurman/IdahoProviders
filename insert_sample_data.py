"""Insert or update Idaho hospitals and their network relationships.

This script assumes that all required network records already exist in the
`networks` table (you ran that migration previously).  It will **add new**
hospitals, **update** any that already exist (matched by `name`), and create
`HospitalNetwork` rows for every hospital‑network combination listed below.

Run with:
    python insert_sample_data.py
"""

import sqlalchemy as sa
from datetime import date

from main import db, app
from models.hospital import Hospital
from models.network import Network
from models.REL_hospital_network import HospitalNetwork

# ---------------------------------------------------------------------------
#  Data — each hospital entry includes the networks (by code) it participates in
# ---------------------------------------------------------------------------
HOSPITALS_DATA = [
    {
        "name": "Benewah Community Hospital",
        "address_line": "229 S 7th St",
        "city": "St. Maries",
        "state": "ID",
        "zip": "83861",
        "networks": ["HNPN"],
    },
    {
        "name": "Bonner General",
        "address_line": "520 N Third Ave",
        "city": "Sandpoint",
        "state": "ID",
        "zip": "83864",
        "networks": ["HNPN"],
    },
    {
        "name": "Boundary Community Hospital",
        "address_line": "6640 Kaniksu St",
        "city": "Bonners Ferry",
        "state": "ID",
        "zip": "83805",
        "networks": ["KCN", "HNPN"],
    },
    {
        "name": "Clearwater Valley Hospital",
        "address_line": "301 Cedar St",
        "city": "Orofino",
        "state": "ID",
        "zip": "83544",
        "networks": ["KCN", "HNPN", "CPN"],
    },
    {
        "name": "Gritman Medical Center",
        "address_line": "700 S Main St",
        "city": "Moscow",
        "state": "ID",
        "zip": "83843",
        "networks": ["HNPN", "CPN"],
    },
    {
        "name": "Kootenai Health",
        "address_line": "2003 Kootenai Health Way",
        "city": "Coeur d'Alene",
        "state": "ID",
        "zip": "83814",
        "networks": ["KCN", "HNPN"],
    },
    {
        "name": "Northern Idaho Advanced Care Hospital",
        "address_line": "600 N Cecil Rd",
        "city": "Post Falls",
        "state": "ID",
        "zip": "83854",
        "networks": ["HNPN"],
    },
    {
        "name": "Northwest Specialty Hospital",
        "address_line": "1593 E Polston Ave",
        "city": "Post Falls",
        "state": "ID",
        "zip": "83854",
        "networks": ["HNPN"],
    },
    {
        "name": "Shoshone Medical Center",
        "address_line": "25 Jacobs Gulch Rd",
        "city": "Kellogg",
        "state": "ID",
        "zip": "83837",
        "networks": ["HNPN"],
    },
    {
        "name": "St. Joseph Regional Medical Center",
        "address_line": "415 6th St",
        "city": "Lewiston",
        "state": "ID",
        "zip": "83501",
        "networks": ["HNPN", "CPN"],
    },
    {
        "name": "St. Mary's Hospital",
        "address_line": "701 Lewiston St",
        "city": "Cottonwood",
        "state": "ID",
        "zip": "83522",
        "networks": ["KCN", "HNPN", "CPN"],
    },
    {
        "name": "Syringa Hospital & Clinics",
        "address_line": "607 W Main St",
        "city": "Grangeville",
        "state": "ID",
        "zip": "83530",
        "networks": ["HNPN", "CPN"],
    },
    {
        "name": "Saint Alphonsus – Boise",
        "address_line": "1055 N Curtis Rd",
        "city": "Boise",
        "state": "ID",
        "zip": "83706",
        "networks": ["HSWPN", "IDID"],
    },
    {
        "name": "Saint Alphonsus – Eagle",
        "address_line": "323 E Riverside Dr",
        "city": "Eagle",
        "state": "ID",
        "zip": "83616",
        "networks": ["HSWPN", "IDID"],
    },
    {
        "name": "St. Luke’s Boise Medical Center",
        "address_line": "190 E Bannock St",
        "city": "Boise",
        "state": "ID",
        "zip": "83712",
        "networks": ["SLHP", "HSWPN"],
    },
    {
        "name": "St. Luke’s Nampa Medical Center",
        "address_line": "9850 W St. Luke's Dr",
        "city": "Nampa",
        "state": "ID",
        "zip": "83687",
        "networks": ["SLHP", "HSWPN"],
    },
    {
        "name": "St. Luke’s Wood River MC",
        "address_line": "100 Hospital Dr",
        "city": "Ketchum",
        "state": "ID",
        "zip": "83340",
        "networks": ["SLHP", "HSWPN"],
    },
    {
        "name": "St. Luke’s Magic Valley MC",
        "address_line": "801 Pole Line Rd W",
        "city": "Twin Falls",
        "state": "ID",
        "zip": "83301",
        "networks": ["SLHP", "HSWPN"],
    },
    {
        "name": "St. Luke’s McCall",
        "address_line": "1000 State St",
        "city": "McCall",
        "state": "ID",
        "zip": "83638",
        "networks": ["SLHP", "HSWPN"],
    },
    {
        "name": "Valor Health",
        "address_line": "1202 E Locust St",
        "city": "Emmett",
        "state": "ID",
        "zip": "83617",
        "networks": ["SLHP", "HSWPN", "IDID"],
    },
    {
        "name": "Bear Lake Memorial",
        "address_line": "164 S 5th St",
        "city": "Montpelier",
        "state": "ID",
        "zip": "83254",
        "networks": ["HEPN"],
    },
    {
        "name": "Bingham Memorial",
        "address_line": "98 Poplar St",
        "city": "Blackfoot",
        "state": "ID",
        "zip": "83221",
        "networks": ["MVN", "HEPN"],
    },
    {
        "name": "Caribou Medical Center",
        "address_line": "300 S 3rd W",
        "city": "Soda Springs",
        "state": "ID",
        "zip": "83276",
        "networks": ["HEPN", "PQA"],
    },
    {
        "name": "Cassia Regional Hospital",
        "address_line": "1501 Hiland Ave",
        "city": "Burley",
        "state": "ID",
        "zip": "83318",
        "networks": ["SLHP", "HSWPN", "HEPN"],
    },
    {
        "name": "Eastern Idaho Regional MC",
        "address_line": "3100 Channing Way",
        "city": "Idaho Falls",
        "state": "ID",
        "zip": "83404",
        "networks": ["HEPN"],
    },
    {
        "name": "Franklin County MC",
        "address_line": "44 N 1st E",
        "city": "Preston",
        "state": "ID",
        "zip": "83263",
        "networks": ["HEPN", "PQA"],
    },
    {
        "name": "Idaho Falls Community Hospital",
        "address_line": "2327 Coronado St",
        "city": "Idaho Falls",
        "state": "ID",
        "zip": "83404",
        "networks": ["MVN", "HEPN"],
    },
    {
        "name": "Lost Rivers District Hospital",
        "address_line": "551 Highland Dr",
        "city": "Arco",
        "state": "ID",
        "zip": "83213",
        "networks": ["HSWPN", "HEPN", "PQA"],
    },
    {
        "name": "Madison Memorial",
        "address_line": "450 E Main St",
        "city": "Rexburg",
        "state": "ID",
        "zip": "83440",
        "networks": ["MVN", "HEPN"],
    },
    {
        "name": "Minidoka Memorial",
        "address_line": "1224 8th St",
        "city": "Rupert",
        "state": "ID",
        "zip": "83350",
        "networks": ["SLHP", "HSWPN", "HEPN"],
    },
    {
        "name": "Mountain View Hospital",
        "address_line": "2325 Coronado St",
        "city": "Idaho Falls",
        "state": "ID",
        "zip": "83404",
        "networks": ["MVN", "HEPN"],
    },
    {
        "name": "Nell J Redfield Memorial",
        "address_line": "150 N 200 W",
        "city": "Malad City",
        "state": "ID",
        "zip": "83252",
        "networks": ["HSWPN", "HEPN", "PQA"],
    },
    {
        "name": "North Canyon Medical Center",
        "address_line": "267 N Canyon Dr",
        "city": "Gooding",
        "state": "ID",
        "zip": "83330",
        "networks": ["SLHP", "HSWPN", "HEPN"],
    },
    {
        "name": "Portneuf Medical Center",
        "address_line": "777 Hospital Way",
        "city": "Pocatello",
        "state": "ID",
        "zip": "83201",
        "networks": ["HEPN", "PQA"],
    },
    {
        "name": "Power County Hospital",
        "address_line": "510 Roosevelt Ave",
        "city": "American Falls",
        "state": "ID",
        "zip": "83211",
        "networks": ["HSWPN", "HEPN", "PQA"],
    },
    {
        "name": "Steele Memorial Medical Center",
        "address_line": "203 S Daisy St",
        "city": "Salmon",
        "state": "ID",
        "zip": "83467",
        "networks": ["SLHP", "HSWPN", "HEPN"],
    },
    {
        "name": "Teton Valley Hospital",
        "address_line": "120 E Howard Ave",
        "city": "Driggs",
        "state": "ID",
        "zip": "83422",
        "networks": ["HEPN"],
    },
]

# ---------------------------------------------------------------------------
#  Helper functions
# ---------------------------------------------------------------------------

def sync_pk_sequence(table_name: str, pk_column: str) -> None:
    """Ensure the Postgres sequence for *table_name.pk_column* is >= MAX(pk)."""
    max_id = db.session.query(sa.func.max(getattr(db.Model.metadata.tables[table_name].c, pk_column))).scalar() or 0
    db.session.execute(
        sa.text(
            "SELECT setval(pg_get_serial_sequence(:tbl,:col), :next_val, false)"
        ),
        {"tbl": table_name, "col": pk_column, "next_val": max_id + 1},
    )


def insert_or_update_hospitals() -> None:
    """Insert or update hospitals and create HospitalNetwork relationships."""
    try:
        sync_pk_sequence("hospitals", "hospital_id")
        sync_pk_sequence("hospital_network", "id")

        added, updated, rel_added = 0, 0, 0

        for entry in HOSPITALS_DATA:
            networks_codes = entry["networks"]
            hospital_attrs = {k: v for k, v in entry.items() if k != "networks"}

            hospital = Hospital.query.filter_by(name=hospital_attrs["name"]).first()
            if hospital:
                # Update address fields if they changed
                for col, val in hospital_attrs.items():
                    if getattr(hospital, col) != val:
                        setattr(hospital, col, val)
                updated += 1
            else:
                hospital = Hospital(**hospital_attrs)
                db.session.add(hospital)
                added += 1

            # Flush so hospital_id is available for relationships
            db.session.flush()

            for code in networks_codes:
                network = Network.query.filter_by(code=code).first()
                if not network:
                    print(f"⚠️  Network '{code}' not found — skipped")
                    continue

                rel_exists = HospitalNetwork.query.filter_by(
                    hospital_id=hospital.hospital_id,
                    network_id=network.network_id,
                ).first()

                if not rel_exists:
                    db.session.add(
                        HospitalNetwork(
                            hospital_id=hospital.hospital_id,
                            network_id=network.network_id,
                            effective_date=date.today(),
                            status="Active",
                        )
                    )
                    rel_added += 1

        db.session.commit()
        print(
            f"✓ Hospitals — {added} added, {updated} updated • "
            f"Relationships — {rel_added} added"
        )

    except Exception as exc:
        db.session.rollback()
        print(f"⚠️  Error inserting hospitals: {exc}")


# ---------------------------------------------------------------------------
#  Entry‑point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    with app.app_context():
        insert_or_update_hospitals()
