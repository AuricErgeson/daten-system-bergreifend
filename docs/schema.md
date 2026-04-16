# Datenbankschema

Das Datenbankschema der Lernmaterialverwaltung besteht aus 7 Tabellen und 2 Triggern.

## Tabellenübersicht

```
themengebiet ──────────────────┐
                               │
benutzer ──────────────────┐   │
                           │   │
kategorie ──────────────┐  │   │
                        ↓  ↓   ↓
                      material
                        │  │
           ┌────────────┘  └────────────┐
           ↓                            ↓
        kommentar                  material_tag
                                        │
                                        ↓
                                       tag

material ──→ version (Versionshistorie)
```

## Tabellen

### `themengebiet`
Themengebiete für Materialien (z.B. "Python", "Netzwerktechnik").

| Spalte | Typ | Beschreibung |
|---|---|---|
| id | INT AUTO_INCREMENT | Eindeutige ID |
| name | VARCHAR(100) UNIQUE | Themenname (Pflicht) |
| beschreibung | TEXT | Optionale Beschreibung |

### `benutzer`
Nutzer mit drei Rollen: Lehrer, Azubi, Admin.

| Spalte | Typ | Beschreibung |
|---|---|---|
| id | INT AUTO_INCREMENT | Eindeutige ID |
| username | VARCHAR(100) UNIQUE | Benutzername (Pflicht) |
| email | VARCHAR(255) UNIQUE | E-Mail-Adresse (Pflicht) |
| rolle | ENUM | "Lehrer", "Azubi" oder "Admin" |
| created_at | TIMESTAMP | Erstellungszeitpunkt (automatisch) |

### `kategorie`
Kategorien für Materialien (z.B. "Präsentation", "Skript").

| Spalte | Typ | Beschreibung |
|---|---|---|
| id | INT AUTO_INCREMENT | Eindeutige ID |
| name | VARCHAR(100) UNIQUE | Kategoriename (Pflicht) |
| beschreibung | TEXT | Optionale Beschreibung |

### `tag`
Schlagwörter für flexible Zusatzkategorisierung.

| Spalte | Typ | Beschreibung |
|---|---|---|
| id | INT AUTO_INCREMENT | Eindeutige ID |
| name | VARCHAR(50) UNIQUE | Schlagwort (Pflicht) |

### `material`
Kernstück: speichert alle Lernmaterialien.

| Spalte | Typ | Beschreibung |
|---|---|---|
| id | INT AUTO_INCREMENT | Eindeutige ID |
| titel | VARCHAR(255) | Titel (Pflicht) |
| beschreibung | TEXT | Optionale Beschreibung |
| themengebiet_id | INT | FK → themengebiet |
| benutzer_id | INT | FK → benutzer (Autor) |
| kategorie_id | INT | FK → kategorie |
| dateiname | VARCHAR(255) | Originaler Dateiname |
| dateityp | VARCHAR(50) | MIME-Type |
| dateigroesse | BIGINT | Größe in Bytes |
| speicherort | VARCHAR(500) | Pfad (nur bei >1MB) |
| inhalt | LONGBLOB | Dateiinhalt (nur bei ≤1MB) |
| is_in_database | BOOLEAN | Speicherstrategie-Markierung |

### `kommentar`
Kommentare zu Materialien.

| Spalte | Typ | Beschreibung |
|---|---|---|
| id | INT AUTO_INCREMENT | Eindeutige ID |
| material_id | INT | FK → material (CASCADE) |
| autor_id | INT | FK → benutzer |
| text | TEXT | Kommentartext (Pflicht) |
| erstellungsdatum | TIMESTAMP | Automatisch gesetzt |

### `material_tag`
Verknüpfungstabelle für die n:m-Beziehung Material ↔ Tag.

### `version`
Versionshistorie von Materialien.

## Trigger

| Trigger | Tabelle | Zeitpunkt | Aktion |
|---|---|---|---|
| `before_material_update` | material | BEFORE UPDATE | Setzt `aenderungsdatum` automatisch |
| `before_kommentar_update` | kommentar | BEFORE UPDATE | Setzt `aenderungsdatum` automatisch |
