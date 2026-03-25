# MEMORY: Lernmaterialverwaltung Projekt

## Was ich verstanden habe

### Projektgrundlagen

| Detail | Information |
|--------|-------------|
| **Fach** | LF8 - Daten systemübergreifend bereitstellen |
| **Projekttyp** | Abschlussprojekt / Prüfungsleistung (Klausurersatz) |
| **Zeitraum** | 06.04.2026 - 16.05.2026 |
| **Abgabe** | IServ-Aufgabentool |
| **Präsentation** | 10-15 Minuten am Smartboard |

### Szenario

Du arbeitest in einem mittelständischen Softwareunternehmen als Teil eines Projektteams. Ihr entwickelt eine datenbankgestützte Anwendung zur Verwaltung von Lernmaterialien für Lehrkräfte und Auszubildende.

**Problem:**
- Materialien werden unstrukturiert abgelegt
- Manuelle Weitergabe führt zu Chaos
- Schwierigkeiten bei Suche, Versionierung und Aktualisierung

**Lösung:**
- Systematische Speicherung
- Gezielte Suche
- Kommentare möglich
- Revisionssichere Ablage

---

## Kernanforderungen

### Materialien

1. **Upload (Hinzufügen)**
   - Dateitypen: PDF, DOCX, JPEG, Python-Dateien
   - Speicherstrategie:
     - ≤1MB: Inhalt direkt in Datenbank (BLOB)
     - >1MB: Pfad-Referenz zum Dateisystem

2. **Download (Suchen & Öffnen)**
   - Materialien finden und herunterladen

3. **Metadaten**
   - Erstelldatum
   - Änderungsdatum
   - Dateiname
   - Dateityp
   - Themengebiet
   - Autor

### Kommentare

- Mehrere Kommentare pro Material möglich
- Attribute:
  - Erstelldatum
  - Letzte Änderung
  - Kommentartext
  - Autor

### Themengebiete

- Jedes Material gehört zu genau einem Themengebiet
- Beispiele: Informatik, Mathematik, Pflege, Wirtschaft, Sonstiges

---

## Datenbankanforderungen

### Mindestanzahl Tabellen

| # | Tabelle | Beschreibung |
|---|---------|-------------|
| 1 | Material | Haupttabelle |
| 2 | Themengebiet | Subject area |
| 3 | Kommentar | Comments |
| 4 | Benutzer | User/Author (zusätzlich) |
| 5 | Kategorie | Category (zusätzlich) |
| 6 | Tag | Tags (zusätzlich) |
| 7 | Version | Version history (zusätzlich) |

**Pflicht:** Mindestens 3 zusätzliche Entitäten → Ich habe 4 vorgeschlagen.

### Suchanforderungen

**Mindestens 7 Suchbefehle:**

| # | Typ | Beispiel |
|---|-----|----------|
| 1 | Aggregation | COUNT Materialien pro Themengebiet |
| 2 | Aggregation | AVG Dateigröße pro Dateityp |
| 3 | Join (Inner) | Materialien JOIN Themengebiet |
| 4 | Join (Inner) | Materialien JOIN Kommentare |
| 5 | Join + Aggregation | Anzahl Kommentare pro Material |
| 6 | Multi-Table Join | Material + Benutzer + Themengebiet |
| 7 | Multi-Table Join | Vollständige Suche mit Filtern |

### Datenbank: MySQL (vorgegeben)

---

## Benutzervorgaben

- **Auszubildende** und **Lehrkräfte** sollen Zugriff haben
- Für Anwendungsentwickler: Dateien <1MB in DB, >1MB als Pfad
- Für Systemintegratoren: Dateien immer als Pfad referenzieren

---

## Deliverables

### 1. Technische Dokumentation (40%)
- SQL-Code
- ERD und ERM (vor und nach Normalisierung)
- Normalisierte Tabellenstruktur

### 2. Software-Dokumentation (40%)
- Projektbeschreibung
- Zielsetzung
- Funktionsübersicht
- Implementierungsdetails
- Kommentare im Python-Quellcode

### 3. Funktionsfähiges Produkt (20%)
- Python-Menü zur Datenbanksteuerung (textbasiert)
- Upload, Suche, Download funktionieren

### 4. Präsentation
- 10-15 Minuten
- Produktvorstellung
- Reflexion des Arbeitsprozesses
- Live-Demo

---

## Technologieentscheidungen (empfohlen)

| Komponente | Empfehlung |
|------------|------------|
| Backend | FastAPI |
| Templates | Jinja2 |
| Interaktivität | HTMX (einfachster Weg) |
| Datenbank | MySQL |
| ORM | SQLAlchemy |
| File Storage | Lokales Dateisystem (`uploads/`) |

**Begründung für HTMX:**
- Keine JavaScript-Entwicklung nötig
- Funktioniert perfekt mit Jinja2
- Dynamisches Verhalten ohne Komplexität
- Ideal für CRUD-Anwendungen
- Schnellste Umsetzung für 1-Monat-Deadline

---

## Notizen

- Falls gemischte Gruppen (Anwendungsentwickler + Systemintegratoren): Anwendungsentwickler-Auftrag verwenden
- Projekt gilt als Klausurersatzleistung = 1/3 der schriftlichen Note
- Keine weitere Klausur in diesem Schuljahr
