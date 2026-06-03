---
name: project_lernmaterialverwaltung
description: Completed LF8 Abschlussprojekt – Lernmaterialverwaltung, Python CLI + MySQL, submitted 2026-05-16
type: project
---

Database-backed CLI application for managing school learning materials. Fully completed and submitted.

**Why:** Klausurersatzleistung (1/3 of written grade). No further exam this school year.

**Timeline:** 06.04.2026 – 16.05.2026. Submitted via IServ.

**Grading weights:**
- Dokumentation: 40%
- Präsentation (10–15 min, Live-Demo am Smartboard): 40%
- Endprodukt (Datenbank + App): 20%

**Final tech stack (NOT FastAPI — switched to CLI):**
- Language: Python 3.12
- ORM: SQLAlchemy 2.0 (automap_base)
- DB Driver: PyMySQL 1.1.2
- Database: MySQL 8.0 (`lernmaterialverwaltung`)
- UI: `rich` 15.0 (terminal tables, colored output)
- Config: `python-dotenv`
- Entry point: `python app/main.py`

**Database schema (`sql/schema.sql`) — 8 tables:**
- `themengebiet`, `benutzer`, `kategorie`, `tag`, `material`, `kommentar`, `material_tag`, `version`
- Dual storage: files < 1 MB → LONGBLOB in DB; files ≥ 1 MB → `uploads/` folder + path in `speicherort`
- `is_in_database` flag on `material` tracks which strategy was used
- Triggers: `before_material_update`, `before_kommentar_update` (auto-update `aenderungsdatum`)
- Schema-only — no INSERT/seed data in schema.sql

**7 required SQL queries (in `services.py`):**
1. COUNT materials per Themengebiet (Aggregation)
2. AVG file size per file type (Aggregation)
3. INNER JOIN material + themengebiet
4. INNER JOIN material + kommentar
5. COUNT comments per material (JOIN + Aggregation)
6. material + benutzer + themengebiet (two JOINs)
7. Full search with three JOINs + optional WHERE filters (most complex)

**Documentation (`LF8_Dokumentation.docx`):**
- Generated via `node generate_doc.js` (requires `docx` npm package — install with `npm install docx`)
- After regeneration: open in Word → Ctrl+A → F9 to refresh TOC page numbers
- Structure: Cover → TOC → 6 chapters → Anhangsverzeichnis → Anhänge I–V
- Quellenverzeichnis: 4 sources ([1] Python, [2] SQLAlchemy, [3] MySQL, [4] rich)

**Doc changes made 2026-06-02:**
- Kap. 1.2: Fremdleistungsabgrenzung added (covers rubric item 2.1.2 = 3 pts)
- Kap. 3.2: Automap problem narration expanded (more personal/natural)
- Kap. 5.3: Language honesty note reordered — Eigenleistung first, Sprachhilfe second
- Quellenverzeichnis: [4] rich library added

**How to apply:** Project is complete. Focus is on documentation quality and presentation prep. The schema and code are not expected to change further.
