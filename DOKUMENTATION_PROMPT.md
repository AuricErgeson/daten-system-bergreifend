# Anweisung: Softwaredokumentation generieren

Du bist ein Assistent. Lies die unten genannten Dateien und erstelle danach eine vollständige Softwaredokumentation auf **Deutsch** für ein Schulprojekt (Berufsschule, LF8).

---

## Dateien die du lesen sollst

| Datei | Inhalt |
|---|---|
| `app/main.py` | Python-Menü (Benutzeroberfläche) |
| `app/services.py` | Alle Datenbankfunktionen und Abfragen |
| `app/database.py` | Datenbankverbindung mit SQLAlchemy |
| `sql/schema.sql` | MySQL-Datenbankschema mit allen Tabellen |

---

## Was du generieren sollst

Erstelle ein Word-Dokument (oder formatierten Text) mit genau diesen Abschnitten in dieser Reihenfolge:

---

### 1. Projektbeschreibung
Erkläre in 3–5 Sätzen was die Anwendung macht.
- Es ist eine Lernmaterialverwaltung
- Lehrkräfte und Azubis können Dateien hochladen, suchen und herunterladen
- Die Daten werden in einer MySQL-Datenbank gespeichert
- Die Oberfläche ist textbasiert (Konsolenmenü in Python)
- Schreibe in einfachem, klarem Deutsch

---

### 2. Zielsetzung
Erkläre in 3–4 Sätzen das Ziel des Projekts.
- Lernmaterialien digital verwalten statt in Ordnern
- Suche, Upload und Download für Lehrkräfte und Azubis
- Revisionssichere Ablage mit Metadaten
- Schreibe in einfachem, klarem Deutsch

---

### 3. Funktionsübersicht
Erstelle eine Tabelle oder Liste mit allen Funktionen der Anwendung.
Basis: schaue in `app/main.py` alle Menüpunkte an.
Format-Vorschlag:

| Funktion | Beschreibung |
|---|---|
| Material hochladen | ... |
| Material herunterladen | ... |
| ... | ... |

Erkläre jede Funktion in einem kurzen Satz.

---

### 4. Implementierungsdetails
Erkläre wie das Programm technisch aufgebaut ist. Beantworte dabei:
- Welche Python-Bibliotheken werden verwendet und warum? (SQLAlchemy, rich, dotenv)
- Wie ist der Code aufgeteilt? (database.py / services.py / main.py — was macht jede Datei?)
- Wie funktioniert die Speicherstrategie? (Dateien unter 1 MB → Datenbank, größere Dateien → Dateisystem als Pfad)
- Wie werden die 7 Datenbankabfragen kategorisiert? (2x Aggregation, 2x Join, 1x Join+Aggregation, 2x Multi-Join)
- Schreibe in einfachem, klarem Deutsch — kein Fachjargon ohne Erklärung

---

### 5. SQL-Code
Füge den kompletten Inhalt von `sql/schema.sql` hier ein — unverändert, als Code-Block.

---

### 6. ERD und ERM
Erstelle eine **textuelle Beschreibung** der Entitäten und Beziehungen (da du kein Bild zeichnen kannst).

Entitäten aus `sql/schema.sql`:
- `benutzer`
- `themengebiet`
- `kategorie`
- `tag`
- `material`
- `kommentar`
- `material_tag` (Verbindungstabelle)
- `version`

Beschreibe für jede Entität:
- Ihre Attribute (Felder)
- Ihre Beziehungen zu anderen Entitäten (1:N, N:M)

Beispiel-Format:
> **material** – speichert Lernmaterialien  
> Attribute: id, titel, beschreibung, dateiname, dateityp, dateigroesse, ...  
> Beziehungen: gehört zu 1 `themengebiet`, gehört zu 1 `benutzer`, kann viele `kommentar` haben

Hinweis für den Schüler: Zeichne das ERD danach selbst in draw.io (draw.io ist kostenlos im Browser).

---

### 7. Normalisierte Tabellenstruktur
Liste alle Tabellen mit ihren Spalten, Datentypen und Schlüsseln auf.
Basis: `sql/schema.sql`

Format-Vorschlag:

**Tabelle: material**
| Spalte | Datentyp | Beschreibung |
|---|---|---|
| id | INT, PK | Eindeutige ID |
| titel | VARCHAR(255) | Titel des Materials |
| ... | ... | ... |

Mache das für alle 8 Tabellen.

---

## Stil-Anweisungen

- Sprache: **Deutsch**
- Niveau: Berufsschule (einfach und klar, kein Uni-Niveau)
- Keine langen Einleitungen oder Füllsätze
- Direkt zum Punkt kommen
- Fachbegriffe kurz erklären wenn sie vorkommen
- Gesamtlänge: ca. 3–5 Seiten Word

---

## Kontext

- Projekt: LF8 – Daten systemübergreifend bereitstellen
- Schüler: Anwendungsentwickler (Azubi)
- Abgabe: 16.05.2026
- Datenbank: MySQL
- Sprache: Python 3
- Textbasierte Oberfläche (kein Web, kein GUI)
