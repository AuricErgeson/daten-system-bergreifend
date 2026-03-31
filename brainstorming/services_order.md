# Services – Reihenfolge der Implementierung

## Phase 1 — Basistabellen (keine Abhängigkeiten)
Diese Tabellen haben keine Foreign Keys, hier anfangen:

1. `benutzer` — create, get all
2. `themengebiet` — create, get all
3. `kategorie` — create, get all
4. `tag` — create, get all

---

## Phase 2 — Kern (abhängig von Phase 1)

5. `material` — **upload** (create), **download** (get by id)
   - Speicherstrategie: < 1 MB → BLOB in DB, sonst → Pfad speichern

---

## Phase 3 — Relationen (abhängig von Phase 2)

6. `material_tag` — Tag zu einem Material hinzufügen
7. `kommentar` — Kommentar zu Material hinzufügen, Kommentare abrufen
8. `version` — Versionseintrag erstellen wenn Material aktualisiert wird

---

## Phase 4 — Suchabfragen (mindestens 7 laut Aufgabe)

9. 2x Aggregation
   - z.B. Anzahl Materialien pro Themengebiet
   - z.B. Durchschnittliche Dateigröße
10. 2x INNER JOIN
    - z.B. Material + Benutzer
    - z.B. Material + Kategorie
11. 1x JOIN + Aggregation
    - z.B. Anzahl Materialien pro Benutzer
12. 2x INNER JOIN über mehrere Tabellen
    - z.B. Material + Themengebiet + Kategorie
    - z.B. Material + Tag + Benutzer