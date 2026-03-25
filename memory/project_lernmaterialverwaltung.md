---
name: project_lernmaterialverwaltung
description: Details of the school Abschlussprojekt – Lernmaterialverwaltung (LF8)
type: project
---

Project to build a database-backed application for managing learning materials (PDFs, DOCX, JPEG, Python files) for teachers and apprentices.

**Why:** Klausurersatzleistung (1/3 of written grade). No further exam this school year.

**Timeline:** 06.04.2026 – 16.05.2026. Submission via IServ.

**Grading:**
- Dokumentation (Prozess + Funktion): 40%
- Präsentation (10–15 min, Live-Demo am Smartboard): 40%
- Endprodukt (Datenbank): 20%

**Tech Stack (decided):**
- Backend: FastAPI
- Templates: Jinja2
- Interactivity: HTMX
- Database: MySQL (required)
- ORM: SQLAlchemy
- File storage: local `uploads/` folder

**Database schema (`sql/schema.sql`) — current state (2026-03-25):**
- Tables: `themengebiet`, `benutzer`, `kategorie`, `tag`, `material`, `kommentar`, `material_tag`, `version`
- `material.themengebiet_id` is a FK to `themengebiet` table (was incorrectly an ENUM before, now fixed)
- No demo data in schema.sql (kept clean — schema only)
- Triggers exist for auto-updating `aenderungsdatum` on material and kommentar

**Still to be built:**
- 7 required SELECT queries (2x Aggregation, 2x Inner Join, 1x Join+Aggregation, 2x Multi-table Join) — goes in `routers/search.py`
- Full FastAPI app (routers: materials, comments, users, search)
- Jinja2 templates
- `docs/` folder: ERD/ERM, SQL-Code, Normalisierung documentation

**How to apply:** When helping with this project, refer to this stack and schema. The schema is the source of truth for table/column names.
