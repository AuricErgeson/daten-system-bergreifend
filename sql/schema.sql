-- =====================================================
-- Lernmaterialverwaltung - MySQL Database Schema
-- =====================================================

DROP DATABASE IF EXISTS lernmaterialverwaltung;
CREATE DATABASE lernmaterialverwaltung CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE lernmaterialverwaltung;

-- =====================================================
-- Tabelle: Themengebiet
-- =====================================================
CREATE TABLE themengebiet (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    beschreibung TEXT
);

-- =====================================================
-- Tabelle: Benutzer
-- =====================================================
CREATE TABLE benutzer (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    rolle ENUM('Lehrer', 'Azubi', 'Admin') NOT NULL DEFAULT 'Azubi',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- Tabelle: Kategorie
-- =====================================================
CREATE TABLE kategorie (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    beschreibung TEXT
);

-- =====================================================
-- Tabelle: Tag
-- =====================================================
CREATE TABLE tag (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

-- =====================================================
-- Tabelle: Material
-- =====================================================
CREATE TABLE material (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titel VARCHAR(255) NOT NULL,
    beschreibung TEXT,
    themengebiet_id INT NOT NULL,
    erstellungsdatum TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    aenderungsdatum TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    dateiname VARCHAR(255),
    dateityp VARCHAR(50),
    dateigroesse BIGINT DEFAULT 0,
    speicherort VARCHAR(500),
    inhalt LONGBLOB,
    is_in_database BOOLEAN DEFAULT FALSE,
    benutzer_id INT NOT NULL,
    kategorie_id INT NOT NULL,
    FOREIGN KEY (themengebiet_id) REFERENCES themengebiet(id) ON DELETE RESTRICT,
    FOREIGN KEY (benutzer_id) REFERENCES benutzer(id) ON DELETE RESTRICT,
    FOREIGN KEY (kategorie_id) REFERENCES kategorie(id) ON DELETE RESTRICT
);

-- =====================================================
-- Tabelle: Kommentar
-- =====================================================
CREATE TABLE kommentar (
    id INT AUTO_INCREMENT PRIMARY KEY,
    material_id INT NOT NULL,
    text TEXT NOT NULL,
    autor_id INT NOT NULL,
    erstellungsdatum TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    aenderungsdatum TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (material_id) REFERENCES material(id) ON DELETE CASCADE,
    FOREIGN KEY (autor_id) REFERENCES benutzer(id) ON DELETE RESTRICT
);

-- =====================================================
-- Tabelle: Material_Tag (N:M Beziehung)
-- =====================================================
CREATE TABLE material_tag (
    material_id INT NOT NULL,
    tag_id INT NOT NULL,
    PRIMARY KEY (material_id, tag_id),
    FOREIGN KEY (material_id) REFERENCES material(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tag(id) ON DELETE CASCADE
);

-- =====================================================
-- Tabelle: Version
-- =====================================================
CREATE TABLE version (
    id INT AUTO_INCREMENT PRIMARY KEY,
    material_id INT NOT NULL,
    version_nr INT NOT NULL,
    aenderungsdatum TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    aenderungen TEXT,
    autor_id INT NOT NULL,
    FOREIGN KEY (material_id) REFERENCES material(id) ON DELETE CASCADE,
    FOREIGN KEY (autor_id) REFERENCES benutzer(id) ON DELETE RESTRICT
);

-- =====================================================
-- Indizes für Performance-Optimierung
-- =====================================================
CREATE INDEX idx_material_themengebiet ON material(themengebiet_id);
CREATE INDEX idx_material_benutzer ON material(benutzer_id);
CREATE INDEX idx_material_kategorie ON material(kategorie_id);
CREATE INDEX idx_kommentar_material ON kommentar(material_id);
CREATE INDEX idx_version_material ON version(material_id);
CREATE INDEX idx_material_erstellungsdatum ON material(erstellungsdatum);

-- =====================================================
-- Trigger für automatisches Aenderungsdatum
-- =====================================================
DELIMITER //

CREATE TRIGGER before_material_update
BEFORE UPDATE ON material
FOR EACH ROW
BEGIN
    SET NEW.aenderungsdatum = CURRENT_TIMESTAMP;
END//

CREATE TRIGGER before_kommentar_update
BEFORE UPDATE ON kommentar
FOR EACH ROW
BEGIN
    SET NEW.aenderungsdatum = CURRENT_TIMESTAMP;
END//

DELIMITER ;

