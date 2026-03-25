---
name: feedback_frontend_and_schema
description: Teacher approved web frontend; schema.sql should stay insert-free
type: feedback
---

**Rule 1: FastAPI web app is valid for this project.**
The assignment says "Eingabemaske in Textform" but the teacher explicitly confirmed that a web frontend is also acceptable. Do not suggest switching to a console/terminal app.

**Why:** User confirmed teacher's approval when this was flagged as a mismatch.

**How to apply:** Never recommend replacing FastAPI/Jinja2 with a console menu. Both are valid.

---

**Rule 2: Keep `schema.sql` free of INSERT/demo data.**
The user wants `schema.sql` to be schema-only (CREATE TABLE, indexes, triggers). No INSERT statements.

**Why:** User said "do not insert nothing" when fixing the schema bugs.

**How to apply:** If adding demo/test data is needed later, put it in a separate file (e.g., `sql/seed.sql`), not in `schema.sql`.
