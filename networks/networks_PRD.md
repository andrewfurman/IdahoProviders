# Product Requirements Document – **Networks Module** (BCBS Idaho Provider Directory)

**Author:** ChatGPT draft for Andrew Furman  
**Date:** 27 Apr 2025  
**Version:** 0.2 (revised per feedback)

---
## 1  Purpose
Provide a focused, front‑to‑back spec for the *networks* slice of the provider‑data web app, including UI, API, data model, and non‑functional standards so the feature can be built and reviewed independently.

---
## 2  Scope
| In scope | Out of scope |
|---|---|
| Identify, display, create, update, and **hard‑delete** networks (e.g., “SLHP”, “HNPN”) | Any provider search / filtering UI |
| Show which hospitals / counties participate in a network (read‑only) | Bulk CSV import tooling (tracked separately) |
| Tailwind‑only styling via **CDN build** for initial deployment | Global CSS frameworks or inline `<style>` blocks |

---
## 3  Success Criteria
* CRUD ops work end‑to‑end with Postgres & SQLAlchemy.  
* Deleting a Network *hard deletes* related rows in `hospital_network` & `county_network` without orphan leaks.  
* All pages render with **zero** custom CSS; inspection shows only Tailwind classes.  
* Universal header appears on every route, keeps 20 px side gutters, and remains usable at widths 320 px → 1920 px.

---
## 4  User Stories
1. **List Networks** – *As a compliance analyst*, I can see every network code & name so I can confirm inclusion.  
2. **View Network Detail** – *As a network manager*, I can click a network to see its hospitals & counties.  
3. **Add Network** – *As an admin*, I can create a new network by entering its **name and code** (both required).  
4. **Edit Network** – *As an admin*, I can change a network’s name or code.  
5. **Delete Network** – *As an admin*, I can delete a network; the system automatically removes any hospital / county mappings (hard delete).

---
## 5  Data Model (SQLAlchemy / Postgres)
> **Rules:** The `name` **and** `code` columns are **NOT NULL**; all other columns default to `NULL` unless stated.

```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, Date
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class TimestampMixin:
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

class Network(TimestampMixin, Base):
    __tablename__ = "network"
    id   = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    code = Column(String(8),  nullable=False, unique=True)  # now required

    county_links   = relationship("CountyNetwork", cascade="all, delete-orphan", passive_deletes=True)
    hospital_links = relationship("HospitalNetwork", cascade="all, delete-orphan", passive_deletes=True)

class County(TimestampMixin, Base):
    __tablename__ = "county"
    id   = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)

class Hospital(TimestampMixin, Base):
    __tablename__ = "hospital"
    id   = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)

class CountyNetwork(Base):
    __tablename__ = "county_network"
    id         = Column(Integer, primary_key=True)
    county_id  = Column(Integer, ForeignKey("county.id",  ondelete="CASCADE"), nullable=False)
    network_id = Column(Integer, ForeignKey("network.id", ondelete="CASCADE"), nullable=False)

class HospitalNetwork(Base):
    __tablename__ = "hospital_network"
    id          = Column(Integer, primary_key=True)
    hospital_id = Column(Integer, ForeignKey("hospital.id", ondelete="CASCADE"), nullable=False)
    network_id  = Column(Integer, ForeignKey("network.id",  ondelete="CASCADE"), nullable=False)
    effective_date = Column(Date)
    status         = Column(String(40))
```

---
## 6  API & Routing
| Route | HTTP | Auth? | Handler | Purpose |
|-------|------|-------|---------|---------|
| `/networks` | GET | public | `networks.list()` | List page |
| `/networks/<int:id>` | GET | public | `networks.detail(id)` | Detail page |
| `/networks/new` | GET/POST | admin | `networks.create()` | Create form + submit |
| `/networks/<int:id>/edit` | GET/POST | admin | `networks.edit(id)` | Edit form + submit |
| `/networks/<int:id>/delete` | POST | admin | `networks.delete(id)` | Hard delete action |

Blueprint: `blueprints/networks/routes.py`

---
## 7  Front‑End Pages, Assets & Universal Header
### 7.1  Header spec (applies to **all** templates)
```html
<header class="bg-white shadow w-full">
  <div class="max-w-screen-xl mx-auto px-5 py-3 flex items-center justify-between">
    <h1 class="text-xl font-semibold text-blue-800 whitespace-nowrap">
      BCBS Idaho Provider Directory
    </h1>
    <nav class="flex gap-6 text-sm font-medium">
      <a class="hover:text-blue-600" href="/networks">Networks</a>
      <a class="hover:text-blue-600" href="/providers">Providers</a>
      <!-- add more as needed -->
    </nav>
  </div>
</header>
```
* 20 px gutter achieved via `px-5` (Tailwind = 1.25 rem ≈ 20 px).  
* Header sits above every page; main content wrapper also uses `px-5` for matching side padding.

### 7.2  Page inventory
| Page | Template | Tailwind Components | Page‑specific JS |
|------|----------|---------------------|-----------------|
| List | `networks_index.html` | responsive table (`flex flex-col divide‑y`) | `networks_index.js` |
| Detail | `network_detail.html` | card section, accordions | `network_detail.js` |
| Create/Edit | `network_form.html` | form controls (`flex flex-col gap-4`) | `network_form.js` |

Tailwind CDN snippet to include at top of `base.html`:
```html
<script src="https://cdn.tailwindcss.com"></script>
```

---
## 8  State Management & JS Standards
* Vanilla ES modules only (one file per page).
* Include scripts at *bottom* of each template:  
  `<script type="module" src="/static/networks/<page>.js"></script>`
* Use `fetch()` for all API calls; errors surface via Tailwind alert banners injected dynamically.

---
## 9  Non‑Functional Requirements
* **Styling:** Tailwind **CDN build** for phase 1; future ticket will migrate to self‑hosted `@tailwindcss` build pipeline.  
* **Performance:** FCP ≤ 2 s on local broadband.  
* **Security:** CSRF tokens on all POST forms; server validation that both `name` and `code` are supplied.  
* **DB Integrity:** Unit tests prove cascades by creating & deleting a network → junction counts = 0.  
* **Logging:** CRUD actions logged to stdout; to be piped to Azure App Insights later.

---
## 10  Acceptance Criteria (excerpt)
| # | Scenario | Given | When | Then |
|---|----------|-------|------|------|
| 1 | Create Network | admin on `/networks/new` | submits form with *name* and *code* | record saved; redirected to detail; toast “Created” |
| 2 | Hard Delete Cascade | network exists with 3 hospital links | admin deletes | rows vanish from `hospital_network`; hospitals remain |
| 3 | Header Rendering | any route | viewport 320 px → 1920 px | header sticks to top, left/right gutters = 20 px, nav links stay visible |
| 4 | Styling Check | any page | dev tools open | no `<style>` tags; Tailwind classes only |

---
## 11  Open Questions
* None at this time – decisions on delete mode, code requirement, and Tailwind delivery chosen above.

