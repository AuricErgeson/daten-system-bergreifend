# Lernmaterialverwaltung

Textbasierte CLI-Anwendung zur Verwaltung von Lernmaterialien – entwickelt als LF8 Abschlussprojekt.

## Was macht die Anwendung?

Die Anwendung ermöglicht es, Lernmaterialien (Dateien wie PDFs, Word-Dokumente, Bilder) zu verwalten:

- **Upload** von Materialien mit automatischer Speicherstrategie (≤1MB → Datenbank, >1MB → Dateisystem)
- **Download** von Materialien auf den lokalen Rechner
- **Suche** nach Materialien mit verschiedenen Filtern
- **Kommentare** zu Materialien hinzufügen, anzeigen und löschen
- **7 Pflichtabfragen** (Aggregation, JOIN, Multi-JOIN)
- **CRUD-Operationen** für alle Entitäten

## Verwendete Technologien

| Technologie | Zweck |
|---|---|
| Python 3.12 | Programmiersprache |
| MySQL | Datenbank |
| SQLAlchemy | Datenbank-ORM (Object Relational Mapper) |
| Typer | CLI-Framework |
| Rich | Farbige Konsolenausgabe |

## Schnellstart

```bash
# Material hochladen
python main.py upload skript.pdf --titel "Python Grundlagen" --thema 1 --autor 1 --kategorie 1

# Materialien suchen
python main.py suche --titel "Python"

# Alle 7 Pflichtabfragen ausführen
python main.py all-queries
```

## Projektstruktur

```
app/
├── main.py        # Startpunkt der Anwendung
├── cli_simple.py  # CLI-Befehle (Typer)
├── services.py    # Datenbankoperationen & Geschäftslogik
├── database.py    # Datenbankverbindung (SQLAlchemy)
├── schemas.py     # Datenklassen
└── uploads/       # Ordner für große Dateien (>1MB)
sql/
└── schema.sql     # Datenbankschema mit Tabellen & Triggern
```
