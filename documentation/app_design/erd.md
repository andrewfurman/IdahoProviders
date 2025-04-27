erDiagram
individual_providers {
    int    provider_id PK
    text   npi
    text   first_name
    text   last_name
    text   gender
    text   phone
    text   provider_type
    boolean accepting_new_patients
    text   specialties
    text   board_certifications
    text   languages
    text   address_line
    text   city
    text   state
    text   zip
}

medical_groups {
    int    group_id PK
    text   name
    text   tax_id
    text   address_line
    text   city
    text   state
    text   zip
}

hospitals {
    int    hospital_id PK
    text   name
    text   ccn
    text   address_line
    text   city
    text   state
    text   zip
}

networks {
    int    network_id PK
    text   code
    text   name
}

%% ────── junctions to handle M:N links ──────
individual_provider_medical_group {
    int    id PK
    int    provider_id FK
    int    group_id    FK
    date   start_date
    date   end_date
    boolean primary_flag
}

medical_group_hospital {
    int    id PK
    int    group_id    FK
    int    hospital_id FK
    text   privilege_type
}

hospital_network {
    int    id PK
    int    hospital_id FK
    int    network_id  FK
    date   effective_date
    text   status
}

medical_group_network {
    int    id PK
    int    group_id   FK
    int    network_id FK
    date   effective_date
    text   status
}

%% ────── cardinalities ──────
individual_providers ||--o{ individual_provider_medical_group : ""
medical_groups       ||--o{ individual_provider_medical_group : ""

medical_groups ||--o{ medical_group_hospital : ""
hospitals      ||--o{ medical_group_hospital : ""

hospitals ||--o{ hospital_network : ""
networks  ||--o{ hospital_network : ""

medical_groups ||--o{ medical_group_network : ""
networks       ||--o{ medical_group_network : ""
