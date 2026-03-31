-- =====================================================
-- Lernmaterialverwaltung - MySQL Database Schema
-- =====================================================

DROP DATABASE IF EXISTS lernmaterialverwaltung;
CREATE DATABASE lernmaterialverwaltung
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE lernmaterialverwaltung;

-- =====================================================
-- Themengebiet (z.B. "Netzwerke", "Datenbanken")
-- =====================================================
CREATE TABLE themengebiet (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    name         VARCHAR(100) NOT NULL UNIQUE,
    beschreibung TEXT
);

-- =====================================================
-- Benutzer (Lehrer, Azubi oder Admin)
-- =====================================================
CREATE TABLE benutzer (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    username   VARCHAR(100) NOT NULL UNIQUE,
    email      VARCHAR(255) NOT NULL UNIQUE,
    rolle      ENUM('Lehrer', 'Azubi', 'Admin') NOT NULL DEFAULT 'Azubi',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- Kategorie (z.B. "Zusammenfassung", "Übungsaufgabe")
-- =====================================================
CREATE TABLE kategorie (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    name         VARCHAR(100) NOT NULL UNIQUE,
    beschreibung TEXT
);

-- =====================================================
-- Tag (Stichwörter für Materialien)
-- =====================================================
CREATE TABLE tag (
    id   INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

-- =====================================================
-- Material (das eigentliche Lernmaterial)
-- =====================================================
CREATE TABLE material (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    titel            VARCHAR(255) NOT NULL,
    beschreibung     TEXT,
    themengebiet_id  INT NOT NULL,
    benutzer_id      INT NOT NULL,
    kategorie_id     INT NOT NULL,
    erstellungsdatum TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    aenderungsdatum  TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    dateiname        VARCHAR(255),
    dateityp         VARCHAR(50),
    dateigroesse     BIGINT DEFAULT 0,
    speicherort      VARCHAR(500),
    inhalt           LONGBLOB,
    is_in_database   BOOLEAN DEFAULT FALSE,

    FOREIGN KEY (themengebiet_id) REFERENCES themengebiet(id) ON DELETE RESTRICT,
    FOREIGN KEY (benutzer_id)     REFERENCES benutzer(id)     ON DELETE RESTRICT,
    FOREIGN KEY (kategorie_id)    REFERENCES kategorie(id)    ON DELETE RESTRICT
);

-- =====================================================
-- Kommentar (Kommentare zu einem Material)
-- =====================================================
CREATE TABLE kommentar (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    material_id      INT NOT NULL,
    autor_id         INT NOT NULL,
    text             TEXT NOT NULL,
    erstellungsdatum TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    aenderungsdatum  TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (material_id) REFERENCES material(id)  ON DELETE CASCADE,
    FOREIGN KEY (autor_id)    REFERENCES benutzer(id)   ON DELETE RESTRICT
);

-- =====================================================
-- Material_Tag (N:M – ein Material kann viele Tags haben)
-- =====================================================
CREATE TABLE material_tag (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    material_id INT NOT NULL,
    tag_id      INT NOT NULL,

    FOREIGN KEY (material_id) REFERENCES material(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id)      REFERENCES tag(id)      ON DELETE CASCADE
);

-- =====================================================
-- Version (Versionshistorie eines Materials)
-- =====================================================
CREATE TABLE version (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    material_id     INT NOT NULL,
    autor_id        INT NOT NULL,
    version_nr      INT NOT NULL,
    aenderungsdatum TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    aenderungen     TEXT,

    FOREIGN KEY (material_id) REFERENCES material(id) ON DELETE CASCADE,
    FOREIGN KEY (autor_id)    REFERENCES benutzer(id) ON DELETE RESTRICT
);

-- =====================================================
-- Trigger: aenderungsdatum automatisch aktualisieren
-- =====================================================
DELIMITER //

CREATE TRIGGER before_material_update
BEFORE UPDATE ON material
FOR EACH ROW
BEGIN
    SET NEW.aenderungsdatum = CURRENT_TIMESTAMP;
END //

CREATE TRIGGER before_kommentar_update
BEFORE UPDATE ON kommentar
FOR EACH ROW
BEGIN
    SET NEW.aenderungsdatum = CURRENT_TIMESTAMP;
END //

DELIMITER ;