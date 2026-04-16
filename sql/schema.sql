-- ═══════════════════════════════════════════════════════════════════════════
-- Datenbankschema: Lernmaterialverwaltung
--
-- Dieses Skript erstellt die gesamte Datenbankstruktur für das LF8-Projekt.
-- Es legt alle Tabellen, Beziehungen (Fremdschlüssel) und Trigger an.
--
-- Ausführen mit: mysql -u root -p < schema.sql
-- ═══════════════════════════════════════════════════════════════════════════


-- ─────────────────────────────────────────────────────────────────────────────
-- Schritt 1: Datenbank erstellen
-- ─────────────────────────────────────────────────────────────────────────────

-- Falls die Datenbank schon existiert, wird sie komplett gelöscht (Vorsicht!)
-- Nützlich bei der Entwicklung, um von vorne anzufangen
DROP DATABASE IF EXISTS lernmaterialverwaltung;

-- Neue Datenbank erstellen
-- CHARACTER SET utf8mb4   → Unterstützt alle Unicode-Zeichen, auch Emojis
-- COLLATE utf8mb4_unicode_ci → Sortierung: Groß-/Kleinschreibung wird ignoriert (ci = case insensitive)
CREATE DATABASE lernmaterialverwaltung
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

-- Ab jetzt alle Befehle in dieser Datenbank ausführen
USE lernmaterialverwaltung;


-- ─────────────────────────────────────────────────────────────────────────────
-- Schritt 2: Tabellen erstellen (Reihenfolge wichtig: zuerst die Eltern-Tabellen!)
-- Tabellen mit Fremdschlüsseln müssen nach den referenzierten Tabellen erstellt werden.
-- ─────────────────────────────────────────────────────────────────────────────

-- Tabelle: themengebiet
-- Speichert Themengebiete, denen Materialien zugeordnet werden können.
-- Beispiele: "Python-Programmierung", "Netzwerktechnik", "Datenbanken"
CREATE TABLE themengebiet (
    id           INT AUTO_INCREMENT PRIMARY KEY,  -- Eindeutige, automatisch hochzählende ID
    name         VARCHAR(100) NOT NULL UNIQUE,    -- Themenname (Pflicht, muss eindeutig sein, max. 100 Zeichen)
    beschreibung TEXT                             -- Optionale Beschreibung (keine Längenbegrenzung)
);


-- Tabelle: benutzer
-- Speichert alle Nutzer des Systems mit ihrer Rolle.
-- Mögliche Rollen: "Lehrer" (erstellt Material), "Azubi" (lernt), "Admin" (verwaltet alles)
CREATE TABLE benutzer (
    id         INT AUTO_INCREMENT PRIMARY KEY,              -- Eindeutige, automatisch hochzählende ID
    username   VARCHAR(100) NOT NULL UNIQUE,                -- Benutzername (Pflicht, eindeutig, max. 100 Zeichen)
    email      VARCHAR(255) NOT NULL UNIQUE,                -- E-Mail (Pflicht, eindeutig, max. 255 Zeichen)
    rolle      ENUM('Lehrer', 'Azubi', 'Admin') NOT NULL    -- Rolle: nur diese drei Werte erlaubt
                   DEFAULT 'Azubi',                         -- Standard-Rolle für neue Benutzer: Azubi
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP          -- Erstellungszeitpunkt (wird automatisch gesetzt)
);


-- Tabelle: kategorie
-- Kategorisiert Materialien nach ihrer Art.
-- Beispiele: "Präsentation", "Skript", "Aufgabenblatt", "Video"
CREATE TABLE kategorie (
    id           INT AUTO_INCREMENT PRIMARY KEY,  -- Eindeutige, automatisch hochzählende ID
    name         VARCHAR(100) NOT NULL UNIQUE,    -- Kategoriename (Pflicht, eindeutig, max. 100 Zeichen)
    beschreibung TEXT                             -- Optionale Beschreibung
);


-- Tabelle: tag
-- Schlagwörter für eine flexible Zusatzkategorisierung von Materialien.
-- Ein Material kann mehrere Tags haben (n:m-Beziehung über material_tag).
-- Beispiele: "Python3", "Anfänger", "LF8", "Klausur"
CREATE TABLE tag (
    id   INT AUTO_INCREMENT PRIMARY KEY,  -- Eindeutige, automatisch hochzählende ID
    name VARCHAR(50) NOT NULL UNIQUE      -- Schlagwort (Pflicht, eindeutig, max. 50 Zeichen)
);


-- Tabelle: material
-- Kernstück der Datenbank: speichert alle Lernmaterialien.
-- Jedes Material gehört zu genau einem Themengebiet, einem Benutzer und einer Kategorie.
--
-- Besonderheit Speicherstrategie:
--   - Kleine Dateien (≤1MB): Inhalt direkt in der Spalte 'inhalt' (LONGBLOB)
--   - Große Dateien (>1MB): Datei liegt im Dateisystem, Pfad steht in 'speicherort'
--   - 'is_in_database' zeigt an, welche Strategie verwendet wurde
CREATE TABLE material (
    id               INT AUTO_INCREMENT PRIMARY KEY,  -- Eindeutige, automatisch hochzählende ID
    titel            VARCHAR(255) NOT NULL,           -- Titel des Materials (Pflicht, max. 255 Zeichen)
    beschreibung     TEXT,                            -- Optionale Inhaltsbeschreibung
    themengebiet_id  INT NOT NULL,                    -- Fremdschlüssel → themengebiet.id (Pflicht)
    benutzer_id      INT NOT NULL,                    -- Fremdschlüssel → benutzer.id (Pflicht, der Autor)
    kategorie_id     INT NOT NULL,                    -- Fremdschlüssel → kategorie.id (Pflicht)
    erstellungsdatum TIMESTAMP DEFAULT CURRENT_TIMESTAMP,              -- Wann wurde das Material erstellt?
    aenderungsdatum  TIMESTAMP DEFAULT CURRENT_TIMESTAMP               -- Wann wurde es zuletzt geändert?
                     ON UPDATE CURRENT_TIMESTAMP,                      -- Automatisch aktualisiert bei Änderung
    dateiname        VARCHAR(255),                    -- Originaler Dateiname (z.B. "skript.pdf")
    dateityp         VARCHAR(50),                     -- MIME-Type (z.B. "application/pdf")
    dateigroesse     BIGINT DEFAULT 0,                -- Dateigröße in Bytes (BIGINT für große Dateien)
    speicherort      VARCHAR(500),                    -- Pfad im Dateisystem (nur bei großen Dateien)
    inhalt           LONGBLOB,                        -- Binärer Dateiinhalt (nur bei kleinen Dateien ≤1MB)
    is_in_database   BOOLEAN DEFAULT FALSE,           -- TRUE = Datei in DB gespeichert, FALSE = im Dateisystem

    -- Fremdschlüssel-Beziehungen:
    -- ON DELETE RESTRICT = Thema/Benutzer/Kategorie kann NICHT gelöscht werden, solange Material existiert
    FOREIGN KEY (themengebiet_id) REFERENCES themengebiet(id) ON DELETE RESTRICT,
    FOREIGN KEY (benutzer_id)     REFERENCES benutzer(id)     ON DELETE RESTRICT,
    FOREIGN KEY (kategorie_id)    REFERENCES kategorie(id)    ON DELETE RESTRICT
);


-- Tabelle: kommentar
-- Benutzer können Kommentare zu Materialien hinterlassen.
-- Jeder Kommentar gehört zu genau einem Material und hat genau einen Autor.
CREATE TABLE kommentar (
    id               INT AUTO_INCREMENT PRIMARY KEY,  -- Eindeutige, automatisch hochzählende ID
    material_id      INT NOT NULL,                    -- Fremdschlüssel → material.id (Pflicht)
    autor_id         INT NOT NULL,                    -- Fremdschlüssel → benutzer.id (Pflicht, Kommentar-Autor)
    text             TEXT NOT NULL,                   -- Kommentartext (Pflicht, keine Längenbegrenzung)
    erstellungsdatum TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Wann wurde der Kommentar erstellt?
    aenderungsdatum  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Wann wurde er zuletzt geändert?

    -- ON DELETE CASCADE = Wird das Material gelöscht, werden auch alle Kommentare gelöscht
    FOREIGN KEY (material_id) REFERENCES material(id)  ON DELETE CASCADE,
    -- ON DELETE RESTRICT = Benutzer kann nicht gelöscht werden, solange er Kommentare hat
    FOREIGN KEY (autor_id)    REFERENCES benutzer(id)  ON DELETE RESTRICT
);


-- Tabelle: material_tag
-- Verknüpfungstabelle für die n:m-Beziehung zwischen Material und Tag.
-- n:m bedeutet: Ein Material kann viele Tags haben, ein Tag kann zu vielen Materialien gehören.
-- Diese "Brückentabelle" löst die n:m-Beziehung in zwei 1:n-Beziehungen auf.
CREATE TABLE material_tag (
    id          INT AUTO_INCREMENT PRIMARY KEY,  -- Eindeutige, automatisch hochzählende ID
    material_id INT NOT NULL,                    -- Fremdschlüssel → material.id
    tag_id      INT NOT NULL,                    -- Fremdschlüssel → tag.id

    -- ON DELETE CASCADE = Tag-Verknüpfung wird automatisch gelöscht, wenn Material oder Tag gelöscht wird
    FOREIGN KEY (material_id) REFERENCES material(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id)      REFERENCES tag(id)      ON DELETE CASCADE
);


-- Tabelle: version
-- Speichert die Versionshistorie von Materialien.
-- Wenn ein Material geändert wird, kann eine neue Version eingetragen werden.
CREATE TABLE version (
    id              INT AUTO_INCREMENT PRIMARY KEY,  -- Eindeutige, automatisch hochzählende ID
    material_id     INT NOT NULL,                    -- Fremdschlüssel → material.id (welches Material?)
    autor_id        INT NOT NULL,                    -- Fremdschlüssel → benutzer.id (wer hat geändert?)
    version_nr      INT NOT NULL,                    -- Versionsnummer (z.B. 1, 2, 3, ...)
    aenderungsdatum TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Wann wurde diese Version erstellt?
    aenderungen     TEXT,                            -- Beschreibung was sich geändert hat

    -- ON DELETE CASCADE = Versions-Einträge werden gelöscht, wenn das Material gelöscht wird
    FOREIGN KEY (material_id) REFERENCES material(id) ON DELETE CASCADE,
    -- ON DELETE RESTRICT = Benutzer kann nicht gelöscht werden, solange er Versionseinträge hat
    FOREIGN KEY (autor_id)    REFERENCES benutzer(id) ON DELETE RESTRICT
);


-- ─────────────────────────────────────────────────────────────────────────────
-- Schritt 3: Trigger erstellen
--
-- Ein Trigger ist Code, der automatisch von der Datenbank ausgeführt wird,
-- wenn bestimmte Ereignisse eintreten (z.B. UPDATE auf einer Tabelle).
-- Hier sorgen Trigger dafür, dass 'aenderungsdatum' immer korrekt gesetzt wird.
-- ─────────────────────────────────────────────────────────────────────────────

-- DELIMITER ändert das Trennzeichen für SQL-Befehle
-- Normalerweise ist es ";", aber da unser Trigger selbst ";" enthält,
-- verwenden wir "//" als temporäres Trennzeichen, damit MySQL nicht zu früh aufhört
DELIMITER //

-- Trigger: before_material_update
-- Wird automatisch ausgeführt BEVOR ein Material-Datensatz geändert wird (BEFORE UPDATE).
-- Setzt das 'aenderungsdatum' auf den aktuellen Zeitpunkt.
-- NEW bezieht sich auf den neuen (geänderten) Datensatz.
CREATE TRIGGER before_material_update
BEFORE UPDATE ON material          -- Ausgelöst bei jedem UPDATE auf der material-Tabelle
FOR EACH ROW                       -- Für jede geänderte Zeile einzeln ausgeführt
BEGIN
    SET NEW.aenderungsdatum = CURRENT_TIMESTAMP;  -- Änderungsdatum automatisch aktualisieren
END //

-- Trigger: before_kommentar_update
-- Wird automatisch ausgeführt BEVOR ein Kommentar-Datensatz geändert wird.
-- Setzt das 'aenderungsdatum' des Kommentars auf den aktuellen Zeitpunkt.
CREATE TRIGGER before_kommentar_update
BEFORE UPDATE ON kommentar         -- Ausgelöst bei jedem UPDATE auf der kommentar-Tabelle
FOR EACH ROW                       -- Für jede geänderte Zeile einzeln
BEGIN
    SET NEW.aenderungsdatum = CURRENT_TIMESTAMP;  -- Änderungsdatum automatisch aktualisieren
END //

-- DELIMITER zurücksetzen auf ";" (Standard wiederherstellen)
DELIMITER ;
