erDiagram
provider {
    int    provider_id PK
    char   npi[10]
    varchar first_name
    varchar last_name
    -- other demo fields …
}

medical_group {
    int    group_id PK
    varchar name
    char   tax_id[9]
}

hospital {
    int    hospital_id PK
    varchar name
    varchar ccn[10]
}

network {
    int    network_id PK
    varchar code
    varchar name
}

%% ────── junctions to handle M:N links ──────
provider_medical_group {
    int provider_id FK
    int group_id    FK
    date start_date
    date end_date
    boolean primary_flag
}

medical_group_hospital {
    int group_id    FK
    int hospital_id FK
    varchar privilege_type
}

hospital_network {
    int hospital_id FK
    int network_id  FK
    date effective_date
    varchar status          -- Active, Tier 1, etc.
}

%% ────── cardinalities ──────
provider      ||--o{ provider_medical_group : ""
medical_group ||--o{ provider_medical_group : ""

medical_group ||--o{ medical_group_hospital : ""
hospital      ||--o{ medical_group_hospital : ""

hospital      ||--o{ hospital_network : ""
network       ||--o{ hospital_network : ""