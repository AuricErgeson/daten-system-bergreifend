#!/usr/bin/env python3
"""
Lernmaterialverwaltung - Startpunkt der Anwendung.

Diese Datei ist der Einstiegspunkt des Programms.
Sie importiert die fertige CLI-Anwendung aus cli_simple.py und startet sie.

Das Projekt erfüllt alle Anforderungen des LF8 Abschlussprojekts:
  - Upload von Materialien (≤1MB in DB gespeichert, >1MB im Dateisystem)
  - Download von Materialien auf den lokalen Rechner
  - Suche nach Materialien mit verschiedenen Filtern (Titel, Thema, Autor, Kategorie, Tag)
  - Kommentarfunktion: Kommentare hinzufügen, anzeigen und löschen
  - 7+ erforderliche Suchabfragen (Aggregation mit COUNT/AVG, JOIN, Multi-JOIN)
  - CRUD-Operationen für alle Entitäten (Benutzer, Themen, Kategorien, Tags, Materialien)

Verwendung in der Kommandozeile:
    python main.py --help
    python main.py upload <datei> --titel "Titel" --thema 1 --autor 1 --kategorie 1
    python main.py download <material-id>
    python main.py suche --titel "Suchbegriff"
    python main.py kommentar add --material 1 --autor 1 --text "Kommentar"
    python main.py list users|themen|kategorien|tags|materialien
    python main.py queries count-thema|avg-size|mat-themen|mat-comments|comments-per|mat-author|search-full
    python main.py create user|thema|kategorie|tag --name "Name"
    python main.py delete <material-id>
    python main.py all-queries
"""

# Die fertige CLI-Anwendung aus cli_simple.py importieren
# 'app' ist das typer-Objekt mit allen registrierten Befehlen
from cli_simple import app

# Nur ausführen, wenn diese Datei direkt gestartet wird (nicht wenn importiert)
# __name__ == "__main__" ist True, wenn z.B. "python main.py" aufgerufen wird
if __name__ == "__main__":
    app()  # CLI-Anwendung starten – typer übernimmt das Parsen der Argumente
