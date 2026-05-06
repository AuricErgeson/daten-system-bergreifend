# LF8 – Daten systemübergreifend bereitstellen

**Thema:** Abschlussprojekt (Prüfungsleistung)

---

## Handlungssituation

Du bist Teil eines Projektteams in einem mittelständischen Softwareunternehmen. Dein Team wurde beauftragt, eine datenbankgestützte Anwendung zu entwickeln, mit der Lernmaterialien für Lehrkräfte und Auszubildende digital verwaltet werden können. Derzeit werden die Materialien unstrukturiert in verschiedenen Verzeichnissen abgelegt oder manuell weitergegeben. Dies führt regelmäßig zu Problemen bei der Suche, Versionierung und Aktualisierung der Inhalte.

Das Ziel des Projekts ist es daher, eine Anwendung zu konzipieren, die es ermöglicht, Lernmaterialien systematisch zu speichern, gezielt zu durchsuchen, zu kommentieren und revisionssicher abzulegen. Die Materialien können in unterschiedlichen Dateiformaten vorliegen, wie z. B. PDF, DOCX, JPEG oder Python-Dateien. Sowohl Auszubildende als auch Lehrkräfte sollen auf die Inhalte zugreifen können. Für Dateien bis 1 MB Größe soll der Inhalt direkt in der Datenbank gespeichert werden. Größere Dateien hingegen sollen aus Performance-Gründen über Pfade zu einem definierten Speicherort referenziert werden. Darüber hinaus soll es möglich sein, Kommentare zu einzelnen Lernmaterialien zu hinterlegen, um Rückmeldungen, Fragen oder Hinweise zu geben. Jedes Lernmaterial gehört einem bestimmten Themengebiet an (z. B. Mathematik, Pflege, Informatik).

Die Anwendung zur Lernmaterialverwaltung soll folgende Funktionen ermöglichen:

1. Lehrkräfte und Auszubildende können Lernmaterialien (Materialien) der Datenbank
   - **hinzufügen** (hochladen)
   - **suchen und öffnen** (herunterladen).
   Die Materialien können z. B. PDFs, Office-Dokumente oder Quellcodedateien sein.
   **Suche:** Für die Suche sollen dem Benutzer mindestens sieben Standardsuchbefehle zur Verfügung stehen. Vorgabe für die Suchbefehle sind:
   - Zwei Aggregationen
   - Zwei Joins (Inner)
   - Ein Join, plus eine Aggregation
   - Zwei Joins (Inner) über mehrere Tabellen

2. Materialien besitzen Metadaten:
   - Erstelldatum
   - Änderungsdatum
   - Dateiname
   - Dateityp
   - Themengebiet
   - Autor sowie eine Speicherstrategie:
     - **Anwendungsentwickler:**
       - Bei Dateien mit weniger als 1 MB soll die Datei direkt in der Datenbank gespeichert werden.
       - Größere Dateien sollen nur über einen Pfad referenziert werden, wo sie im Dateisystem abgelegt sind.
     - **Systemintegratoren:**
       - Dateien sollen über einen Pfad referenziert werden.

3. Lernmaterialien können mehrere Kommentare enthalten. Jeder Kommentar mindestens folgende Attribute:
   - Erstelldatum
   - Letzte Änderung
   - Kommentartext
   - Autor

4. Jedes Lernmaterial gehört zu genau einem Themengebiet (z. B. Informatik, Mathematik, Pflege etc.).

5. Es sollen mindestens drei weitere sinnvolle Entitäten ergänzt werden.

6. Die zu nutzende Datenbank ist **MySQL**.

---

## Arbeitsauftrag

1. Führe eine vollständige Planung deiner Datenbank durch (Analyse, ERD, ERM).
2. Verbessere falls notwendig deine Datenbank (Normalisierung, Korrektur ERD, ERM).
3. Setze deine Datenbank als eine MySQL-Datenbank um.
4. Erstelle eine Bedienoberfläche in Python (Eingabemaske in Textform).
5. Dokumentiere deine Arbeitsschritte gemäß der beigefügten Excelinhalte (siehe Anhang I_Projekt_Bewertung_Vorlage).

---

## Organisatorisches: Projekt Lernfeld 8

### Prüfungsleistung
Die Projektarbeit gilt als Klausurersatzleistung und macht ein Drittel der schriftlichen Note im Fach aus. Dafür wird es keine weitere Klausurleistung in diesem Schuljahr mehr geben.

### Partnerarbeit
Die Partnerbildung erfolgt flexibel. Es gibt jedoch einen Unterschied zwischen Anwendungsentwicklern und Systemintegratoren: Falls gemischte Partnergruppen gebildet werden, ist der Arbeitsauftrag für die Anwendungsentwickler zu bearbeiten.

### Zeitraum
- **Projektstart:** Donnerstag, 06.04.2026
- **Abgabe & Präsentationen:** Donnerstag, 16.05.2026
- Die finale Präsentation findet im Klassenverband statt. Die genauen Zeitfenster werden rechtzeitig bekanntgegeben.
- Alle Materialien (Code, Dokumentation etc.) sind über das IServ-Aufgabentool abzugeben.

### Handlungsergebnis
Am Ende des Projekts gebt ihr folgende Ergebnisse in Form einer Dokumentation ab:

1. **Technische Dokumentation:**
   - SQL-Code
   - ERD und ERM vor und ggf. nach der Normalisierung
   - Normalisierte Tabellenstruktur

2. **Softwaredokumentation:**
   - Projektbeschreibung
   - Zielsetzung
   - Funktionsübersicht
   - Implementierungsdetails
   - Dokumentation durch Kommentare im Python-Quellcode (Deutsch oder Englisch)

3. **Funktionsfähiges Produkt (Python-Anwendung):**
   - Python-Menü zur Datenbanksteuerung (Textbasiert in Eingabeaufforderung/Konsole)
   - Upload, Suche und Download von Lernmaterialien

4. **Präsentation** (Insgesamt 10–15 Minuten pro Gruppe am Smartboard):
   - Kurze Vorstellung des Produkts
   - Reflexion des Arbeitsprozesses („Wie sind wir zum Produkt gekommen?")

---

## Bewertung

Die Beurteilung erfolgt nach:

| Kriterium | Anteil |
|---|---|
| Ausführliche Dokumentation des Arbeitsprozesses und Funktion des Softwareproduktes (Punkte 1–3) | **40 %** der Note |
| Präsentation des Ergebnisses (Punkt 4) | **40 %** der Note |
| Endprodukt (Datenbank) | **20 %** der Note |
