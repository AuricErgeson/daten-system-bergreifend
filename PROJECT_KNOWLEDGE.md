# LF8 – Lernmaterialverwaltung: Project Knowledge Base

## What This Project Is

A command-line application for managing school learning materials (Lernmaterialien). Built as the LF8 Abschlussprojekt for an Anwendungsentwickler Azubi (Auric Ergeson) at Berufsschule. The system allows uploading, downloading, searching, commenting on, and categorizing learning materials stored in a MySQL database.

**Grade weight:** Documentation 40% | Presentation 40% | Product 20%

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3 |
| ORM | SQLAlchemy 2.0 |
| DB Driver | PyMySQL 1.1.2 |
| Database | MySQL (`lernmaterialverwaltung`) |
| UI | `rich` 15.0 (terminal tables, colored output) |
| Config | `python-dotenv` |

**Entry point:** `python app/main.py`

---

## Project Structure

```
daten-system-bergreifend/
├── app/
│   ├── main.py          # All menus and user interaction (CLI)
│   ├── services.py      # Business logic + all 7 SQL queries
│   ├── database.py      # SQLAlchemy engine + SessionLocal setup
│   └── uploads/         # Filesystem storage for large files
├── sql/
│   └── schema.sql       # Full DB schema (import this to set up DB)
├── generate_doc.js      # Node.js script that generates the Word doc
├── LF8_Dokumentation.docx  # Output documentation (regenerate with node generate_doc.js)
├── Auric_Dokumentation.pdf # PDF export of the documentation
├── lernmaterialverwaltung.png  # ERD image (exported from DBeaver)
├── requirements.txt
└── .env                 # DB credentials (not committed)
```

---

## Database Schema (8 Tables)

```
themengebiet    → subject areas (e.g., Netzwerk, Programmierung)
benutzer        → users with roles: Lehrer | Azubi | Admin
kategorie       → file categories
tag             → free-form tags
material        → core table: files with metadata + binary content
kommentar       → comments linked to a material + author
material_tag    → many-to-many join between material and tag
version         → version history for materials
```

**Key design decision — dual storage strategy:**
Files under a threshold go into MySQL as `LONGBLOB` (`inhalt` column). Larger files are saved to `app/uploads/` on disk. The `is_in_database` boolean flag on `material` tracks which path was used.

**Two MySQL triggers are defined:**
- `before_material_update` — auto-updates `aenderungsdatum` on material changes
- `before_kommentar_update` — same for comments

---

## Application Menu (8 Functions)

| Menu Option | Function |
|---|---|
| 1 | Upload material (file path → title → thema → autor → kategorie → tags) |
| 2 | Download material (choose by ID → save to output folder) |
| 3 | Search materials (filter by title, thema, autor) |
| 4 | Delete material (with confirmation prompt) |
| 5 | Manage comments (view / add / delete) |
| 6 | View lists (Materialien, Benutzer, Themengebiete, Kategorien, Tags) |
| 7 | Run database queries (all 7 required SQL queries) |
| 8 | Create new entries (users, themen, kategorien, tags) |

---

## The 7 Required SQL Queries (in `services.py`)

These were required by the teacher rubric:

| # | Type | What it does |
|---|---|---|
| 1 | COUNT (Aggregation) | Number of materials per Themengebiet |
| 2 | AVG (Aggregation) | Average file size per file type |
| 3 | JOIN | Materials with their Themengebiet |
| 4 | JOIN | Materials with their comments |
| 5 | JOIN + COUNT | Comment count per material |
| 6 | Multi-JOIN | Material + author (benutzer) + themengebiet |
| 7 | Multi-JOIN + filter | Full search with optional thema/autor filters |

Query 7 returns named result objects (`r.titel`, `r.autor`, `r.themengebiet`, `r.kategorie`) — it's the most complex, joining material, benutzer, themengebiet, and kategorie in one query with optional WHERE clauses.

---

## Documentation

The Word documentation is generated programmatically using Node.js + the `docx` npm package.

**To regenerate:** `node generate_doc.js` → then open in Word and press **Ctrl+A → F9** to refresh TOC page numbers.

**Document layout:**
- A4, Arial 11pt, dark navy H1 (#1F3864), blue H2 (#2E75B6)
- Cover page → TOC → body with running header + "Seite X von Y" footer
- Tables: dark navy header, alternating light blue/white rows
- Code blocks: Courier New 9pt, grey (#F2F2F2) background

**Current structure — prozessorientierter Projektbericht (updated 2026-06-01):**

Main body (6 chapters):
1. Projektauftrag (1.1 Ausgangssituation, 1.2 Aufgabenstellung, 1.3 Projektumfeld)
2. Projektplanung (2.1 Lösungsansatz + Alternativen, 2.2 Zeitplanung table)
3. Projektdurchführung (3.1 Datenbankdesign, 3.2 Implementierung, 3.3 Ergebnisse)
4. Funktionsübersicht (8-function table)
5. Projektabschluss (5.1 Soll-Ist, 5.2 Zeitaufwand-Vergleich, 5.3 Reflexion)
6. Quellenverzeichnis (3 sources)

Then: Anhangsverzeichnis → 5 numbered appendices:
- Anhang I: Full SQL schema (read from `sql/schema.sql`)
- Anhang II: ERD image (DBeaver PNG, 600×482px) + entity text descriptions
- Anhang III: Normalized table structure (all 8 tables)
- Anhang IV: Architecture, libraries, storage strategy, 7 SQL queries, code comment examples
- Anhang V: Installation guide

**New helpers in `generate_doc.js`:**
- `pItalic(text)` — italic grey cross-reference lines, e.g. `(siehe Anhang I)`
- `anhangH1(label, title)` — H1 heading for appendices (shows in TOC)
- `tdb(text, w)` — bold blue cell for the totals row
- `buildZeitplanungTable()` — 6-row planned vs actual hours table (35h → 43h)
- `buildAnhangsverzeichnis()` — static index table listing Anhang I–V

**Rubric coverage (grading rubric = `brainstorming/Anhang I_Projekt_Bewertung_Vorlage.pdf`):**

| Rubric item | Points | Status |
|---|---|---|
| 1.2 Anhangsverzeichnis + Quellenangaben | 5 | ✅ |
| 1.3 Cross-references to Anhänge | 5 | ✅ |
| 2.1 Projektauftrag | 9 | ✅ |
| 2.2 Projektplanung + Zeitplan | 10 | ✅ |
| 2.3 Projektdurchführung | 31 | ✅ |
| 2.4 Projektabschluss + Reflexion | 15 | ✅ |
| 3.1 Anhänge (technical docs) | 10 | ✅ |

---

## Setup Instructions

1. Copy `.env.example` to `.env` and fill in MySQL credentials
2. Import the schema: `mysql -u root -p < sql/schema.sql`
3. Install Python dependencies: `pip install -r requirements.txt`
4. Run: `python app/main.py`

---

## Project Context

- **Student:** Auric Ergeson, Azubi Anwendungsentwickler
- **School:** Berufsschule
- **Submission:** 2026-05-16 via IServ
- **All code written by Auric** — documentation ~91% Auric, rest assisted with German phrasing
- **ERD image** (`lernmaterialverwaltung.png`) was generated from the live MySQL database using DBeaver
