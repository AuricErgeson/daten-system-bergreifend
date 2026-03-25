# PROJECT PLAN: Lernmaterialverwaltung

## Projektübersicht

**Fach:** LF8 - Daten systemübergreifend bereitstellen  
**Projektart:** Abschlussprojekt / Prüfungsleistung  
**Zeitraum:** 06.04.2026 - 16.05.2026 (ca. 6 Wochen)

---

## Ausgangsituation

Du bist Teil eines Projektteams in einem mittelständischen Softwareunternehmen. Dein Team wurde beauftragt, eine datenbankgestützte Anwendung zu entwickeln, mit der Lernmaterialien für Lehrkräfte und Auszubildende digital verwaltet werden können.

**Problem:** Materialien werden unstrukturiert in verschiedenen Verzeichnissen abgelegt oder manuell weitergegeben → Probleme bei Suche, Versionierung und Aktualisierung.

**Ziel:** Anwendung konzipieren, die Lernmaterialien systematisch speichert, durchsucht, kommentiert und revisionssicher ablegt.

---

## Datenbank-Design

### ERD (Entity-Relationship-Diagramm)

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   THEMENGEBIET  │     │     BENUTZER    │     │    KATEGORIE    │
├─────────────────┤     ├─────────────────┤     ├─────────────────┤
│ PK id           │     │ PK id           │     │ PK id           │
│   name          │     │   username      │     │   name          │
│   beschreibung  │     │   email         │     │   beschreibung  │
└────────┬────────┘     │   rolle         │     └────────┬────────┘
         │             │   created_at    │             │
         │             └─────────────────┘             │
         │                                            │
         │ 1:N                                        │ 1:N
         ▼                                            ▼
┌────────────────────────────────────────────────────────────────────┐
│                            MATERIAL                                 │
├────────────────────────────────────────────────────────────────────┤
│ PK id                                                                │
│   titel                          FK themengebiet_id (→Themengebiet) │
│   beschreibung                   FK benutzer_id (→Benutzer)         │
│   erstellungsdatum               FK kategorie_id (→Kategorie)      │
│   aenderungsdatum                                              │
│   dateiname                                                      │
│   dateityp                                                         │
│   dateigroesse (bytes)                                             │
│   speicherort (path, NULL wenn <1MB)                               │
│   inhalt (BLOB, NULL wenn >1MB)                                    │
│   is_in_database (boolean)                                        │
└──────────────────────────┬────────────────────────────────────────┘
                           │
              ┌────────────┼────────────┐
              │ 1:N        │ 1:N        │ 1:N
              ▼            ▼            ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│    KOMMENTAR    │ │   MATERIAL_TAG  │ │    VERSION      │
├─────────────────┤ ├─────────────────┤ ├─────────────────┤
│ PK id           │ │ PK (mat_id,    │ │ PK id           │
│ FK material_id  │ │       tag_id)  │ │ FK material_id  │
│   text          │ │ FK material_id │ │   version_nr    │
│   autor_id      │ │ FK tag_id      │ │   aenderungsdatum│
│   erstellungsdatum              │ │   aenderungen    │
│   aenderungsdatum               │ │   autor_id      │
└─────────────────┘ └─────────────────┘ └─────────────────┘
                                      │
                                      │ N:1
                                      ▼
                              ┌─────────────────┐
                              │       TAG       │
                              ├─────────────────┤
                              │ PK id           │
                              │   name          │
                              └─────────────────┘
```

### Relationships

| Beziehung | Typ | Beschreibung |
|-----------|-----|--------------|
| Material → Themengebiet | N:1 | Jedes Material gehört zu einem Themengebiet |
| Material → Benutzer | N:1 | Jedes Material hat einen Autor |
| Material → Kategorie | N:1 | Jedes Material hat eine Kategorie |
| Material → Kommentar | 1:N | Ein Material kann viele Kommentare haben |
| Material ↔ Tag | N:M | Materialien können mehrere Tags haben |
| Material → Version | 1:N | Materialien können Versionsgeschichte haben |
| Kommentar → Benutzer | N:1 | Kommentare haben Autoren |

### Speicherstrategie

| Dateigröße | Speichermethode | Wo |
|------------|-----------------|-----|
| ≤ 1 MB | BLOB in DB | `inhalt` (Binary Large Object) |
| > 1 MB | Pfad-Referenz | Datei im Dateisystem, `speicherort` in DB |

---

## Funktionsanforderungen

### 1. Materialien verwalten
- [ ] Materialien hinzufügen (Upload)
- [ ] Materialien suchen und öffnen (Download)
- [ ] Materialien löschen
- [ ] Materialien bearbeiten

### 2. Metadaten
- [ ] Erstelldatum
- [ ] Änderungsdatum
- [ ] Dateiname
- [ ] Dateityp
- [ ] Themengebiet
- [ ] Autor

### 3. Kommentare
- [ ] Kommentar zu Material hinzufügen
- [ ] Kommentare anzeigen
- [ ] Kommentare bearbeiten/löschen

### 4. Suchfunktion
**Mindestens 7 Suchbefehle:**

| # | Typ | Beschreibung |
|---|-----|--------------|
| 1 | Aggregation | COUNT: Anzahl Materialien pro Themengebiet |
| 2 | Aggregation | AVG: Durchschnittliche Dateigröße pro Dateityp |
| 3 | Join | Materialien + Themengebiet |
| 4 | Join | Materialien + Kommentare |
| 5 | Join + Aggregation | Anzahl Kommentare pro Material |
| 6 | Multi-Table Join | Material + Benutzer + Themengebiet |
| 7 | Multi-Table Join | Vollständige Suche mit Filtern |

---

## Tech Stack

| Komponente | Wahl | Begründung |
|-----------|------|------------|
| Backend | FastAPI | Schnell, modern, automatische API-Dokumentation |
| Templates | Jinja2 | In FastAPI integriert |
| Interaktivität | HTMX | Kein eigenes JS nötig, funktioniert mit Jinja2 |
| Datenbank | MySQL | Pflicht laut Aufgabenstellung |
| ORM | SQLAlchemy | Saubere Python-Abfragen |
| Dateispeicher | Lokal `uploads/` | Einfachster Ansatz für Deadline |

---

## Projektstruktur

```
daten-system-bergreifend/        ← Repository Root
├── brainstorming/               ← Planungsdokumente & Notizen
│   ├── PROJECT_PLAN.md
│   ├── template-app.md
│   └── *.pdf                    # Schulunterlagen / Aufgabenstellung
├── docs/                        ← Technische Dokumentation (Abgabe)
│   ├── erd.md                   # ERD & ERM
│   ├── sql_code.md              # SQL-Code
│   └── normalisierung.md        # Normalisierung
├── lernmaterialverwaltung/      ← App-Code
│   ├── main.py                  # FastAPI Einstieg (uvicorn main:app)
│   ├── database.py              # MySQL Verbindung
│   ├── models.py                # SQLAlchemy Models
│   ├── schemas.py               # Pydantic Schemas
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── materials.py         # Material CRUD
│   │   ├── comments.py          # Kommentare
│   │   ├── users.py             # Benutzer
│   │   └── search.py            # Suchabfragen
│   ├── templates/               # Jinja2 Templates
│   │   ├── base.html
│   │   └── materials/
│   ├── static/
│   │   └── htmx.min.js
│   ├── uploads/                 # Dateispeicher (>1MB)
│   ├── .env                     # DB-Zugangsdaten (nicht in Git)
│   └── requirements.txt
└── README.md
```

**Imports** (alle relativ zu `lernmaterialverwaltung/`, von dort starten):
```python
# in main.py
from database import engine
from routers import materials, comments

# in routers/materials.py
from database import get_db
from models import Material
```

---

## 6-Wochen Zeitplan

### Woche 1: Datenbank-Design & Setup
| Tag | Aufgabe | Deliverable |
|-----|---------|-------------|
| 1-2 | ERD/ERM erstellen | Draw.io/SQLDBM Diagramm |
| 3-4 | MySQL Datenbank aufsetzen | Leere DB mit Tabellen |
| 5 | Normalisierung prüfen | Optimierte Tabellenstruktur |

### Woche 2: Backend (FastAPI)
| Tag | Aufgabe | Deliverable |
|-----|---------|-------------|
| 6-7 | SQLAlchemy Models & DB Verbindung | Verbundene App |
| 8-9 | CRUD API Endpoints | Upload/Download/Delete |
| 10 | Suchabfragen (7+ Queries) | Alle Abfragen funktionieren |

### Woche 3: Frontend (Jinja2 + HTMX)
| Tag | Aufgabe | Deliverable |
|-----|---------|-------------|
| 11-12 | Base Template + Navigation | Konsistentes UI |
| 13-14 | Material Upload/Download UI | Funktionierende Oberflächen |
| 15-16 | Such-UI mit Filtern | Dynamische Suche |
| 17 | Kommentar-Feature | Kommentare hinzufügen/anzeigen |

### Woche 4: Kommentare & Versionen
| Tag | Aufgabe | Deliverable |
|-----|---------|-------------|
| 18-19 | Versionierung implementieren | Änderungshistorie |
| 20-21 | Tags & Kategorien UI | Filterung funktioniert |

### Woche 5: Dokumentation
| Tag | Aufgabe | Deliverable |
|-----|---------|-------------|
| 22-23 | Technische Dokumentation | SQL, ERD, Normalisierung |
| 24-25 | Software-Dokumentation | Code-Kommentare |
| 26-27 | README und Setup-Guide | Installationsanleitung |

### Woche 6: Polieren & Abgabe
| Tag | Aufgabe | Deliverable |
|-----|---------|-------------|
| 28-29 | Testing & Bugfixes | Funktionierendes Produkt |
| 30-31 | Präsentationsvorbereitung | 10-15 Folien |
| 32 | **Abgabe** | IServ Upload |

---

## Abgabe-Anforderungen

### 1. Technische Dokumentation (40% der Note)
- [ ] SQL-Code
- [ ] ERD und ERM (vor und nach Normalisierung)
- [ ] Normalisierte Tabellenstruktur

### 2. Software-Dokumentation (40% der Note)
- [ ] Projektbeschreibung
- [ ] Zielsetzung
- [ ] Funktionsübersicht
- [ ] Implementierungsdetails
- [ ] Kommentare im Python-Quellcode (DE oder EN)

### 3. Funktionsfähiges Produkt (20% der Note)
- [ ] Python-Menü zur Datenbanksteuerung (textbasiert in Konsole)
- [ ] Upload, Suche und Download von Lernmaterialien

### 4. Präsentation (10-15 Minuten)
- [ ] Kurze Vorstellung des Produkts
- [ ] Reflexion des Arbeitsprozesses
- [ ] Live-Demo am Smartboard

---

## Bewertung

| Komponente | Gewichtung |
|------------|------------|
| Dokumentation (Prozess + Funktion) | 40% |
| Präsentation | 40% |
| Endprodukt (Datenbank) | 20% |

---

## Nützliche Ressourcen

- FastAPI Docs: https://fastapi.tiangolo.com/
- SQLAlchemy Docs: https://docs.sqlalchemy.org/
- HTMX Docs: https://htmx.org/docs/
- Jinja2 Docs: https://jinja.palletsprojects.com/
- MySQL Tutorial: https://www.mysqltutorial.org/
