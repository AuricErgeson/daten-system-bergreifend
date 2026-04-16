# Lernmaterialverwaltung - Simplified CLI App

## Projektübersicht

Dies ist eine vereinfachte Kommandozeilen-App für das Lernmaterialverwaltung-Projekt (LF8 - Daten systemübergreifend bereitstellen). Die ursprüngliche FastAPI-Webanwendung wurde in eine einfache CLI-App umgewandelt, die weiterhin mit der MySQL-Datenbank verbunden ist.

## Projektidee

Das Projekt ist eine datenbankgestützte Anwendung zur Verwaltung von Lernmaterialien für Lehrkräfte und Auszubildende. Es löst das Problem unstrukturierter Materialablage durch systematische Speicherung, gezielte Suche und revisionssichere Ablage.

**Kernfunktionen:**
- Verwaltung von Lernmaterialien (PDF, DOCX, JPEG, Python-Dateien)
- Materialien werden in der Datenbank oder im Dateisystem gespeichert (je nach Größe)
- Metadatenverwaltung (Titel, Beschreibung, Themengebiet, Autor, etc.)
- Kommentarfunktion für Materialien
- Suchfunktionen mit verschiedenen Filteroptionen

## Technische Details

### Datenbank
- **MySQL** (vorgegeben)
- **Schema:** 8 Tabellen (themengebiet, benutzer, kategorie, tag, material, kommentar, material_tag, version)
- **Speicherstrategie:** 
  - Dateien ≤ 1 MB: Inhalt direkt in Datenbank (BLOB)
  - Dateien > 1 MB: Pfad-Referenz zum Dateisystem

### Aktuelle App-Struktur
```
daten-system-bergreifend/
├── app/                    # Hauptanwendung
│   ├── main.py           # Typer CLI-Einstiegspunkt
│   ├── cli_simple.py     # Typer CLI mit voller Funktionalität
│   ├── database.py       # MySQL-Datenbankverbindung (SQLAlchemy)
│   ├── services.py       # Datenbankoperationen & 7+ Suchabfragen
│   ├── schemas.py        # Einfache Datenklassen
│   ├── uploads/          # Dateispeicher (>1MB)
│   └── cli.py            # Alte CLI (nicht mehr verwendet)
├── sql/
│   └── schema.sql        # MySQL-Datenbankschema (8 Tabellen)
├── brainstorming/        # Projektplanung & Notizen
├── memory/              # Projektkontext & Feedback
├── requirements.txt     # Python-Abhängigkeiten (Typer + Rich + SQLAlchemy)
└── .env                # Datenbankzugangsdaten
```

## Verwendung

### Installation
1. Python 3.8+ installieren
2. Abhängigkeiten installieren:
   ```bash
   pip install -r requirements.txt
   ```
3. Datenbank einrichten:
   ```bash
   mysql -u root -p < sql/schema.sql
   ```
4. `.env`-Datei mit Datenbankzugangsdaten erstellen (siehe `.env.example`)

### Vollständige Funktionalität - Textbasierte CLI

Die App implementiert **alle Projektanforderungen** mit einer textbasierten Typer CLI:

#### 1. Materialien hochladen (Upload)
```bash
# Kleine Dateien (≤1MB) werden in der Datenbank gespeichert
python main.py upload pfad/zur/datei.pdf --titel "Titel" --thema 1 --autor 1 --kategorie 1

# Große Dateien (>1MB) werden im Dateisystem gespeichert
python main.py upload pfad/zur/großen-datei.pdf --titel "Große Datei" --thema 2 --autor 1 --kategorie 1
```

#### 2. Materialien herunterladen (Download)
```bash
python main.py download <material-id>
python main.py download 1 --output downloads/
```

#### 3. Materialien suchen (Suche)
```bash
# Nach Titel suchen
python main.py suche --titel "Suchbegriff"

# Nach Themengebiet filtern
python main.py suche --thema 1

# Nach Autor filtern  
python main.py suche --autor 1

# Kombinierte Suche
python main.py suche --titel "Test" --thema 1 --autor 1
```

#### 4. Kommentare verwalten
```bash
# Kommentar hinzufügen
python main.py kommentar add --material 1 --autor 1 --text "Dies ist ein Kommentar"

# Kommentare anzeigen
python main.py kommentar list --material 1

# Kommentar löschen
python main.py kommentar delete --id 1
```

#### 5. Entitäten auflisten (CRUD)
```bash
python main.py list users
python main.py list themen
python main.py list kategorien
python main.py list tags
python main.py list materialien
```

#### 6. Neue Entitäten erstellen
```bash
# Benutzer erstellen
python main.py create user --name "lehrer1" --email "lehrer@schule.de" --rolle "Lehrer"

# Themengebiet erstellen
python main.py create thema --name "Physik" --beschreibung "Mechanik, Optik, Thermodynamik"

# Kategorie erstellen
python main.py create kategorie --name "Klausur" --beschreibung "Prüfungsmaterialien"

# Tag erstellen
python main.py create tag --name "wichtig"
```

#### 7. 7+ erforderliche Suchabfragen
```bash
# 1. Aggregation: Material pro Themengebiet (COUNT)
python main.py queries count-thema

# 2. Aggregation: Durchschnittliche Größe pro Dateityp (AVG)
python main.py queries avg-size

# 3. Inner Join: Materialien mit Themengebieten
python main.py queries mat-themen

# 4. Inner Join: Materialien mit Kommentaren
python main.py queries mat-comments

# 5. Join + Aggregation: Kommentare pro Material
python main.py queries comments-per

# 6. Multi-Table Join: Material mit Autor und Thema
python main.py queries mat-author

# 7. Multi-Table Join: Vollständige Suche mit Filtern
python main.py queries search-full --thema 1 --autor 1

# Alle 7 Abfragen auf einmal
python main.py all-queries
```

#### 8. Material löschen
```bash
python main.py delete <material-id>
```

### Unterstützte Dateitypen
- **PDF** (.pdf)
- **Word** (.doc, .docx)
- **Bilder** (.jpg, .jpeg, .png)
- **Python** (.py)
- **Text** (.txt, .csv)

### Speicherstrategie (Projektanforderung)
- **Dateien ≤ 1 MB**: Inhalt wird direkt in der Datenbank gespeichert (BLOB)
- **Dateien > 1 MB**: Pfad-Referenz zum Dateisystem (`uploads/` Verzeichnis)

## Projektkontext

Dies ist ein **Abschlussprojekt / Prüfungsleistung** für das Fach LF8. 
- **Zeitraum:** 06.04.2026 - 16.05.2026
- **Bewertung:** Dokumentation (40%), Präsentation (40%), Endprodukt (20%)
- **Abgabe:** IServ-Aufgabentool

### Erfüllte Projektanforderungen

Die App implementiert **alle Kernanforderungen** des LF8 Abschlussprojekts:

#### ✅ **Funktionsfähiges Produkt (20% der Note)**
- **Upload (Hinzufügen)**: Dateiupload mit Größen-basierter Speicherstrategie
- **Download (Suchen & Öffnen)**: Materialien finden und herunterladen
- **Python-Menü**: Textbasierte CLI mit Typer
- **7+ Suchabfragen**: Alle erforderlichen SQL-Abfragen implementiert

#### ✅ **Materialien-Verwaltung**
- **Dateitypen**: PDF, DOCX, JPEG, Python-Dateien, Textdateien
- **Speicherstrategie**: 
  - ≤1MB: Inhalt direkt in Datenbank (BLOB)
  - >1MB: Pfad-Referenz zum Dateisystem (`uploads/`)
- **Metadaten**: Titel, Beschreibung, Dateiname, Dateityp, Dateigröße, Themengebiet, Autor, Kategorie, Tags

#### ✅ **Kommentar-System**
- Mehrere Kommentare pro Material möglich
- Vollständige CRUD-Operationen für Kommentare
- Autoren- und Zeitstempel-Verwaltung

#### ✅ **7+ erforderliche Suchabfragen**
1. ✅ **COUNT Materialien pro Themengebiet** (Aggregation)
2. ✅ **AVG Dateigröße pro Dateityp** (Aggregation)
3. ✅ **Materialien JOIN Themengebiete** (Inner Join)
4. ✅ **Materialien JOIN Kommentare** (Inner Join)
5. ✅ **Anzahl Kommentare pro Material** (Join + Aggregation)
6. ✅ **Material + Benutzer + Themengebiet** (Multi-Table Join)
7. ✅ **Vollständige Suche mit Filtern** (Multi-Table Join)

#### ✅ **Datenbank-Design**
- **8 Tabellen**: Material, Themengebiet, Kommentar, Benutzer, Kategorie, Tag, Material_Tag, Version
- **MySQL** (vorgegeben)
- **Normalisierte Struktur** mit Fremdschlüsseln
- **Triggers** für automatische Änderungsdatum-Aktualisierung

#### ✅ **Technische Umsetzung**
- **Backend**: Python mit Typer CLI
- **Datenbank**: MySQL mit SQLAlchemy ORM
- **Dateispeicher**: Lokales `uploads/` Verzeichnis
- **Benutzeroberfläche**: Textbasierte CLI mit Rich für schöne Tabellen

## Nächste Schritte

Die App kann erweitert werden für:
1. Komplette Datei-Upload-Funktionalität im CLI
2. Alle 7 erforderlichen Suchabfragen implementieren
3. Vollständige CRUD-Operationen für alle Entitäten
4. Bessere Fehlerbehandlung und Validierung
5. Export-Funktionen für Berichte