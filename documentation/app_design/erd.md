
FURMAN UPDATE

Need to get audit log working

  File "/home/runner/workspace/.pythonlibs/lib/python3.11/site-packages/sqlalchemy/orm/query.py", line 289, in <listcomp>
    coercions.expect(
  File "/home/runner/workspace/.pythonlibs/lib/python3.11/site-packages/sqlalchemy/sql/coercions.py", line 388, in expect
    insp._post_inspect
  File "/home/runner/workspace/.pythonlibs/lib/python3.11/site-packages/sqlalchemy/util/langhelpers.py", line 1257, in __get__
    obj.__dict__[self.__name__] = result = self.fget(obj)
                                           ^^^^^^^^^^^^^^
  File "/home/runner/workspace/.pythonlibs/lib/python3.11/site-packages/sqlalchemy/orm/mapper.py", line 2724, in _post_inspect
    self._check_configure()
  File "/home/runner/workspace/.pythonlibs/lib/python3.11/site-packages/sqlalchemy/orm/mapper.py", line 2401, in _check_configure
    _configure_registries({self.registry}, cascade=True)
  File "/home/runner/workspace/.pythonlibs/lib/python3.11/site-packages/sqlalchemy/orm/mapper.py", line 4214, in _configure_registries
    _do_configure_registries(registries, cascade)
  File "/home/runner/workspace/.pythonlibs/lib/python3.11/site-packages/sqlalchemy/orm/mapper.py", line 4251, in _do_configure_registries
    raise e
sqlalchemy.exc.InvalidRequestError: One or more mappers failed to initialize - can't proceed with initialization of other mappers. Triggering mapper: 'Mapper[ProviderAudit(individual_provider_audit)]'. Original exception was: When initializing mapper Mapper[ProviderAudit(individual_provider_audit)], expression 'auth.auth_models.User' failed to locate a name ('auth.auth_models.User'). If this is a class name, consider adding this relationship() to the <class 'models.provider_audit.ProviderAudit'> class after both dependent classes have been defined.

FURMAN UPDATE GOT MODELS WORKING

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
