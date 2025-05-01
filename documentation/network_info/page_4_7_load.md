Based on all of the existing data in my database for Blue Cross Blue Shield of Idaho providers and the sample of the provider directory below, can you create a new updated insert sample data Python file that I can use to insert records into the database based on these exported data from the below tables?

~/workspace$ python export_network_hospitals_medgroups.py
## Networks

| ID | Code | Name |
|-----|------|------|
| 1 | MAHMO | True Blue HMO |
| 2 | MAPPO | Secure Blue PPO |
| 3 | MMCPHMO | True Blue Special Needs Plan |
| 4 | MICRON | Micron CDHP/PPO |
| 5 | SLHP | St. Luke's Health Partners |
| 6 | KCN | Kootenai Care Network |
| 7 | HNPN | Hometown North Provider Network |
| 8 | CPN | Clearwater Provider Network |
| 9 | HSWPN | Hometown South-West Provider Network |
| 10 | IDID | Independent Doctors of Idaho |
| 11 | MVN | Mountain View Network |
| 12 | HEPN | Hometown East Provider Network |
| 13 | PQA | Patient Quality Alliance |


## Hospitals

| ID | Name |
|-----|------|
| 1 | St Lukes Regional Medical Center |
| 2 | Saint Alphonsus Regional Medical Center |
| 3 | Benewah Community Hospital |
| 4 | Bonner General |
| 5 | Boundary Community Hospital |
| 6 | Clearwater Valley Hospital |
| 7 | Gritman Medical Center |
| 8 | Kootenai Health |
| 9 | Northern Idaho Advanced Care Hospital |
| 10 | Northwest Specialty Hospital |
| 11 | Shoshone Medical Center |
| 12 | St. Joseph Regional Medical Center |
| 13 | St. Mary's Hospital |
| 14 | Syringa Hospital & Clinics |
| 15 | Saint Alphonsus – Boise |
| 16 | Saint Alphonsus – Eagle |
| 17 | St. Luke’s Boise Medical Center |
| 18 | St. Luke’s Nampa Medical Center |
| 19 | St. Luke’s Wood River MC |
| 20 | St. Luke’s Magic Valley MC |
| 21 | St. Luke’s McCall |
| 22 | Valor Health |
| 23 | Bear Lake Memorial |
| 24 | Bingham Memorial |
| 25 | Caribou Medical Center |
| 26 | Cassia Regional Hospital |
| 27 | Eastern Idaho Regional MC |
| 28 | Franklin County MC |
| 29 | Idaho Falls Community Hospital |
| 30 | Lost Rivers District Hospital |
| 31 | Madison Memorial |
| 32 | Minidoka Memorial |
| 33 | Mountain View Hospital |
| 34 | Nell J Redfield Memorial |
| 35 | North Canyon Medical Center |
| 36 | Portneuf Medical Center |
| 37 | Power County Hospital |
| 38 | Steele Memorial Medical Center |
| 39 | Teton Valley Hospital |


## Medical Groups

| ID | Name | Address |
|-----|------|---------|
| 1 | Nexus Wound Consultants | 1555 W Shoreline Dr |
| 2 | St Lukes Clinic | 2619 W Fairview Ave |
| 3 | Medical Directors of Idaho | 3550 W Americana Ter |


## Hospital-Network Relationships

| Hospital ID | Network ID |
|------------|------------|
| 1 | 1 |
| 1 | 2 |
| 2 | 1 |
| 3 | 7 |
| 4 | 7 |
| 5 | 6 |
| 5 | 7 |
| 6 | 6 |
| 6 | 7 |
| 6 | 8 |
| 7 | 7 |
| 7 | 8 |
| 8 | 6 |
| 8 | 7 |
| 9 | 7 |
| 10 | 7 |
| 11 | 7 |
| 12 | 7 |
| 12 | 8 |
| 13 | 6 |
| 13 | 7 |
| 13 | 8 |
| 14 | 7 |
| 14 | 8 |
| 15 | 9 |
| 15 | 10 |
| 16 | 9 |
| 16 | 10 |
| 17 | 5 |
| 17 | 9 |
| 18 | 5 |
| 18 | 9 |
| 19 | 5 |
| 19 | 9 |
| 20 | 5 |
| 20 | 9 |
| 21 | 5 |
| 21 | 9 |
| 22 | 5 |
| 22 | 9 |
| 22 | 10 |
| 23 | 12 |
| 24 | 11 |
| 24 | 12 |
| 25 | 12 |
| 25 | 13 |
| 26 | 5 |
| 26 | 9 |
| 26 | 12 |
| 27 | 12 |
| 28 | 12 |
| 28 | 13 |
| 29 | 11 |
| 29 | 12 |
| 30 | 9 |
| 30 | 12 |
| 30 | 13 |
| 31 | 11 |
| 31 | 12 |
| 32 | 5 |
| 32 | 9 |
| 32 | 12 |
| 33 | 11 |
| 33 | 12 |
| 34 | 9 |
| 34 | 12 |
| 34 | 13 |
| 35 | 5 |
| 35 | 9 |
| 35 | 12 |
| 36 | 12 |
| 36 | 13 |
| 37 | 9 |
| 37 | 12 |
| 37 | 13 |
| 38 | 5 |
| 38 | 9 |
| 38 | 12 |
| 39 | 12 |


## Medical Group-Hospital Relationships

| Medical Group ID | Hospital ID |
|-----------------|-------------|
| 2 | 1 |
| 2 | 2 |