# WorkQueue · Design & Implementation Guide

## 1  Purpose
The **WorkQueue** module surfaces provider‑data issues (duplicates, missing attributes, validation flags) as actionable work items. Reviewers claim items, inspect the affected provider record, perform corrective actions, and then mark each item *resolved*.  This guide defines database schema, Flask routes, HTML templates, and UX patterns for the first release.

---
## 2  Core Concepts
| Term | Definition |
|------|------------|
| **Work Item** | A single task representing one provider record that needs manual review. |
| **Queue Type** | Category that determined why the item was created (`DUPLICATE_CHECK`, `MISSING_DATA`, etc.). |
| **Status** | Lifecycle state: `OPEN` → `IN_PROGRESS` → `RESOLVED` (or `REJECTED`). |
| **Action** | Concrete reviewer operation recorded against the item (e.g., *add NPI*, *mark duplicate*, *comment*). |

---
## 3  Database Schema (SQLAlchemy)
```python
class WorkItem(db.Model):
    __tablename__ = "work_items"

    id           = db.Column(db.Integer, primary_key=True)
    provider_id  = db.Column(db.Integer, db.ForeignKey("individual_providers.id"), nullable=False)
    queue_type   = db.Column(db.Enum("DUPLICATE_CHECK", "MISSING_DATA", name="queue_type"), nullable=False)
    status       = db.Column(db.Enum("OPEN", "IN_PROGRESS", "RESOLVED", "REJECTED", name="work_status"), default="OPEN")
    priority     = db.Column(db.Integer, default=3)  # 1‑High, 5‑Low
    created_at   = db.Column(db.DateTime, server_default=db.func.now())
    assigned_to  = db.Column(db.Integer, db.ForeignKey("user.id"))
    resolved_at  = db.Column(db.DateTime)
    notes        = db.Column(db.Text)

class WorkAction(db.Model):
    __tablename__ = "work_actions"

    id          = db.Column(db.Integer, primary_key=True)
    work_item_id= db.Column(db.Integer, db.ForeignKey("work_items.id"), nullable=False)
    user_id     = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    action_type = db.Column(db.String(40))  # COMMENT, FIELD_UPDATE, RESOLVE
    payload     = db.Column(db.JSON)
    created_at  = db.Column(db.DateTime, server_default=db.func.now())

# Relationship helpers
WorkItem.actions = db.relationship("WorkAction", backref="work_item", lazy="dynamic")
```

### 3.1  Migration stub
```bash
flask db revision -m "create work queue tables"
flask db upgrade
```

---
## 4  Blueprint & Routes (`queue/routes.py`)
```python
bp = Blueprint("queue", __name__)

# List with filters, pagination
@bp.get("/queue")
@login_required
def list_items():
    q = WorkItem.query
    if (status := request.args.get("status")):
        q = q.filter_by(status=status)
    items = q.order_by(WorkItem.priority, WorkItem.created_at).paginate()
    return render_template("queue/index.html", items=items)

# Detail + provider context
@bp.get("/queue/<int:item_id>")
@login_required
def view_item(item_id):
    item = WorkItem.query.get_or_404(item_id)
    provider = IndividualProvider.query.get(item.provider_id)
    return render_template("queue/detail.html", item=item, provider=provider)

# Perform action (AJAX or form)
@bp.post("/queue/<int:item_id>/action")
@login_required
def perform_action(item_id):
    item = WorkItem.query.get_or_404(item_id)
    act  = WorkAction(work_item_id=item.id,
                      user_id=current_user.id,
                      action_type=request.form["action_type"],
                      payload=request.form.to_dict())
    db.session.add(act)
    if act.action_type == "RESOLVE":
        item.status = "RESOLVED"
        item.resolved_at = datetime.utcnow()
    db.session.commit()
    flash("Action recorded", "success")
    return redirect(url_for("queue.view_item", item_id=item.id))
```

> **URL design rationale**: `/queue` for the inbox; child routes scoped by `item_id` follow REST semantics.

---
## 5  Template Layout
```
templates/
└─ queue/
   ├─ index.html   # list / filters / claim button
   └─ detail.html  # provider card + action form
```

### 5.1  `index.html` (excerpt)
```html
{% extends "base.html" %}
{% block content %}
<h1 class="text-2xl font-bold mb-4">Work Queue</h1>
<table class="table-auto w-full">
  <thead><tr><th>ID</th><th>Provider</th><th>Type</th><th>Status</th><th>Priority</th><th></th></tr></thead>
  <tbody>
    {% for item in items.items %}
    <tr class="border-b">
      <td>{{ item.id }}</td>
      <td><a class="text-blue-600" href="{{ url_for('provider.view', provider_id=item.provider_id) }}">{{ item.provider_id }}</a></td>
      <td>{{ item.queue_type }}</td>
      <td>{{ item.status }}</td>
      <td>{{ item.priority }}</td>
      <td><a href="{{ url_for('queue.view_item', item_id=item.id) }}" class="btn">Open</a></td>
    </tr>
    {% endfor %}
  </tbody>
</table>
{% endblock %}
```

### 5.2  `detail.html` (excerpt)
```html
{% extends "base.html" %}
{% block content %}
<div class="grid grid-cols-2 gap-6">
  <section>
    <h2 class="text-xl font-semibold">Provider</h2>
    <pre class="bg-gray-100 p-4 rounded">{{ provider|tojson(indent=2) }}</pre>
  </section>
  <section>
    <h2 class="text-xl font-semibold">Review Actions</h2>
    <form method="post" action="{{ url_for('queue.perform_action', item_id=item.id) }}" class="space-y-4">
      <textarea name="comment" class="w-full border p-2" placeholder="Comment"></textarea>
      <select name="action_type" class="border p-2">
        <option value="COMMENT">Comment</option>
        <option value="FIELD_UPDATE">Field Update</option>
        <option value="RESOLVE">Mark Resolved</option>
      </select>
      <button class="btn-primary">Submit</button>
    </form>
    <hr class="my-6"/>
    <h3 class="font-medium mb-2">History</h3>
    {% for a in item.actions.order_by(WorkAction.created_at.desc()) %}
      <p><strong>{{ a.created_at.strftime('%Y-%m-%d %H:%M') }}</strong> – {{ a.action_type }} by {{ a.user_id }}</p>
      <pre class="bg-gray-50 p-2 rounded text-sm">{{ a.payload }}</pre>
    {% endfor %}
  </section>
</div>
{% endblock %}
```

---
## 6  UX Flow
1. **Inbox**: Reviewer opens `/queue`; filters by *status = OPEN* and selects top‑priority tasks.
2. **Detail View**: Provider record and context appear alongside an action panel.
3. **Action**: Reviewer updates fields or leaves comment → submits form.
4. **Resolution**: Choosing *Mark Resolved* moves item to `RESOLVED` (hidden from default view).

---
## 7  Environment Variables (additions)
No new secrets are required for WorkQueue; reuse existing DB + Flask config. If you want to tune pagination size or timeouts, add:
```bash
QUEUE_PAGE_SIZE=25          # default rows per page
```
Load via `app.config["QUEUE_PAGE_SIZE"]`.

---
## 8  Future Enhancements
* **Auto‑assignment** logic (round‑robin reviewers).
* **Bulk actions** on list page.
* **WebSocket** updates for real‑time queue refresh.
* **Audit export** (CSV of resolved items).
* **Background job** to auto‑create WorkItems from validation scripts.

---
© 2025 Engineering · Provider Data Apps

