'use strict';
const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, TabStopType, TabStopPosition, ImageRun,
  TableOfContents, HeadingLevel, BorderStyle, WidthType, ShadingType,
  PageNumber, PageBreak
} = require('docx');

// A4 dimensions in DXA (1440 DXA = 1 inch, 567 DXA = 1 cm)
const A4_W  = 11906;
const A4_H  = 16838;
const M_TOP = 1701;   // ~3 cm
const M_BOT = 1701;
const M_LFT = 1701;
const M_RGT = 1134;   // ~2 cm
const CW    = A4_W - M_LFT - M_RGT; // 9071

const PAGE_PROPS = {
  page: {
    size: { width: A4_W, height: A4_H },
    margin: { top: M_TOP, bottom: M_BOT, left: M_LFT, right: M_RGT }
  }
};

const C_H1    = "1F3864";
const C_H2    = "2E75B6";
const C_BODY  = "1A1A1A";
const C_GREY  = "555555";
const C_LGREY = "777777";
const C_STRIPE = "EEF3FA";
const C_CODE  = "F2F2F2";
const C_BORD  = "CCCCCC";

const BDR = { style: BorderStyle.SINGLE, size: 4, color: C_BORD };
const CELL_BORDERS = { top: BDR, bottom: BDR, left: BDR, right: BDR };
const PAD = { top: 80, bottom: 80, left: 120, right: 120 };

// ── Paragraph helpers ──────────────────────────────────────────────────────

const p = (text, opts = {}) => new Paragraph({
  spacing: { after: 120 }, ...opts,
  children: [new TextRun({ text, font: "Arial", size: 22, color: C_BODY })]
});

const bp = (text) => new Paragraph({
  spacing: { after: 100 },
  children: [new TextRun({ text, font: "Arial", size: 22, bold: true, color: C_BODY })]
});

const sp = () => new Paragraph({
  spacing: { after: 60 },
  children: [new TextRun({ text: "", font: "Arial", size: 22 })]
});

const h1 = (text) => new Paragraph({
  heading: HeadingLevel.HEADING_1,
  children: [new TextRun(text)]
});

const h2 = (text) => new Paragraph({
  heading: HeadingLevel.HEADING_2,
  children: [new TextRun(text)]
});

const code = (text) => new Paragraph({
  spacing: { before: 0, after: 0 },
  shading: { fill: C_CODE, type: ShadingType.CLEAR },
  children: [new TextRun({ text: text || " ", font: "Courier New", size: 18, color: "333333" })]
});

// ── Table cell helpers ─────────────────────────────────────────────────────

const th = (text, w) => new TableCell({
  borders: CELL_BORDERS, width: { size: w, type: WidthType.DXA },
  shading: { fill: C_H1, type: ShadingType.CLEAR }, margins: PAD,
  children: [new Paragraph({ children: [new TextRun({ text, font: "Arial", size: 20, bold: true, color: "FFFFFF" })] })]
});

const td = (text, w, s = false) => new TableCell({
  borders: CELL_BORDERS, width: { size: w, type: WidthType.DXA },
  shading: { fill: s ? C_STRIPE : "FFFFFF", type: ShadingType.CLEAR }, margins: PAD,
  children: [new Paragraph({ children: [new TextRun({ text, font: "Arial", size: 20, color: C_BODY })] })]
});

const mc = (text, w, s = false) => new TableCell({
  borders: CELL_BORDERS, width: { size: w, type: WidthType.DXA },
  shading: { fill: s ? C_STRIPE : "FFFFFF", type: ShadingType.CLEAR }, margins: PAD,
  children: [new Paragraph({ children: [new TextRun({ text, font: "Courier New", size: 18, color: "333333" })] })]
});

// ── SQL content ────────────────────────────────────────────────────────────

const SQL = `DROP DATABASE IF EXISTS lernmaterialverwaltung;

CREATE DATABASE lernmaterialverwaltung
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE lernmaterialverwaltung;

CREATE TABLE themengebiet (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    name         VARCHAR(100) NOT NULL UNIQUE,
    beschreibung TEXT
);

CREATE TABLE benutzer (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    username   VARCHAR(100) NOT NULL UNIQUE,
    email      VARCHAR(255) NOT NULL UNIQUE,
    rolle      ENUM('Lehrer', 'Azubi', 'Admin') NOT NULL DEFAULT 'Azubi',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE kategorie (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    name         VARCHAR(100) NOT NULL UNIQUE,
    beschreibung TEXT
);

CREATE TABLE tag (
    id   INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

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

CREATE TABLE kommentar (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    material_id      INT NOT NULL,
    autor_id         INT NOT NULL,
    text             TEXT NOT NULL,
    erstellungsdatum TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    aenderungsdatum  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (material_id) REFERENCES material(id)  ON DELETE CASCADE,
    FOREIGN KEY (autor_id)    REFERENCES benutzer(id)  ON DELETE RESTRICT
);

CREATE TABLE material_tag (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    material_id INT NOT NULL,
    tag_id      INT NOT NULL,

    FOREIGN KEY (material_id) REFERENCES material(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id)      REFERENCES tag(id)      ON DELETE CASCADE
);

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

DELIMITER ;`;

const ERD_IMG = fs.readFileSync('lernmaterialverwaltung.png');

// ── Funktionsübersicht ─────────────────────────────────────────────────────

const F1 = 2300, F2 = 5571, F3 = 1200;

const FUNKTIONEN = [
  ["Material hochladen",       "Eine Datei wird mit Titel, Thema und Autor versehen und gespeichert – unter 1 MB direkt in der Datenbank, größere Dateien im Ordner uploads/.", "[1]"],
  ["Material herunterladen",   "Ein Material wird anhand der ID ausgewählt und in einen lokalen Ordner exportiert.",                                                               "[2]"],
  ["Materialien suchen",       "Die Liste lässt sich nach Titel, Themengebiet oder Autor filtern. Ergebnisse erscheinen als formatierte Tabelle.",                                 "[3]"],
  ["Material löschen",         "Ein Material wird anhand der ID aus der Datenbank entfernt. Liegt die Datei im Dateisystem, wird sie dort ebenfalls gelöscht.",                    "[4]"],
  ["Kommentare verwalten",     "Kommentare zu einem Material können angezeigt, hinzugefügt oder gelöscht werden.",                                                                 "[5]"],
  ["Listen & Übersichten",     "Materialien, Benutzer, Themen, Kategorien und Tags lassen sich vollständig als Tabelle einsehen.",                                                 "[6]"],
  ["Datenbank-Abfragen",       "Sieben SQL-Abfragen mit Joins und Aggregationen können einzeln oder alle auf einmal ausgeführt werden.",                                            "[7]"],
  ["Neue Einträge erstellen",  "Benutzer, Themengebiete, Kategorien und Tags lassen sich direkt über das Menü anlegen.",                                                           "[8]"],
];

function buildFunktionsTable() {
  return new Table({
    width: { size: CW, type: WidthType.DXA },
    columnWidths: [F1, F2, F3],
    rows: [
      new TableRow({ tableHeader: true, children: [th("Funktion", F1), th("Beschreibung", F2), th("Menü", F3)] }),
      ...FUNKTIONEN.map(([f, b, m], i) => new TableRow({
        children: [td(f, F1, i%2===0), td(b, F2, i%2===0), td(m, F3, i%2===0)]
      }))
    ]
  });
}

// ── Normalisierte Tabellenstruktur ─────────────────────────────────────────

const S1 = 2000, S2 = 2071, S3 = 1500, S4 = 3500;

const TABLES = {
  benutzer: [
    ["id",         "INT",          "PK, AI",  "Eindeutige Benutzer-ID"],
    ["username",   "VARCHAR(100)", "UNIQUE",  "Benutzername"],
    ["email",      "VARCHAR(255)", "UNIQUE",  "E-Mail-Adresse"],
    ["rolle",      "ENUM",         "",        "Rolle: Lehrer, Azubi oder Admin"],
    ["created_at", "TIMESTAMP",    "",        "Erstellungsdatum (automatisch gesetzt)"],
  ],
  themengebiet: [
    ["id",           "INT",          "PK, AI",  "Eindeutige Thema-ID"],
    ["name",         "VARCHAR(100)", "UNIQUE",  "Name des Themengebiets"],
    ["beschreibung", "TEXT",         "",        "Optionale Beschreibung"],
  ],
  kategorie: [
    ["id",           "INT",          "PK, AI",  "Eindeutige Kategorie-ID"],
    ["name",         "VARCHAR(100)", "UNIQUE",  "Name der Kategorie"],
    ["beschreibung", "TEXT",         "",        "Optionale Beschreibung"],
  ],
  tag: [
    ["id",   "INT",         "PK, AI",  "Eindeutige Tag-ID"],
    ["name", "VARCHAR(50)", "UNIQUE",  "Tag-Bezeichnung"],
  ],
  material: [
    ["id",               "INT",          "PK, AI",  "Eindeutige Material-ID"],
    ["titel",            "VARCHAR(255)", "",        "Titel des Lernmaterials"],
    ["beschreibung",     "TEXT",         "",        "Optionale Beschreibung"],
    ["themengebiet_id",  "INT",          "FK",      "Verweis auf themengebiet(id)"],
    ["benutzer_id",      "INT",          "FK",      "Verweis auf benutzer(id) – Autor"],
    ["kategorie_id",     "INT",          "FK",      "Verweis auf kategorie(id)"],
    ["erstellungsdatum", "TIMESTAMP",    "",        "Zeitpunkt des Uploads (automatisch)"],
    ["aenderungsdatum",  "TIMESTAMP",    "",        "Letztes Änderungsdatum (automatisch)"],
    ["dateiname",        "VARCHAR(255)", "",        "Originaldateiname"],
    ["dateityp",         "VARCHAR(50)",  "",        "MIME-Typ (z. B. application/pdf)"],
    ["dateigroesse",     "BIGINT",       "",        "Dateigröße in Bytes"],
    ["speicherort",      "VARCHAR(500)", "",        "Dateipfad (bei Dateisystemspeicherung)"],
    ["inhalt",           "LONGBLOB",     "",        "Dateiinhalt (bei Dateien unter 1 MB)"],
    ["is_in_database",   "BOOLEAN",      "",        "TRUE = Inhalt in DB, FALSE = Dateisystem"],
  ],
  kommentar: [
    ["id",               "INT",       "PK, AI",  "Eindeutige Kommentar-ID"],
    ["material_id",      "INT",       "FK",      "Verweis auf material(id)"],
    ["autor_id",         "INT",       "FK",      "Verweis auf benutzer(id)"],
    ["text",             "TEXT",      "",        "Kommentartext"],
    ["erstellungsdatum", "TIMESTAMP", "",        "Erstellungszeitpunkt"],
    ["aenderungsdatum",  "TIMESTAMP", "",        "Letztes Änderungsdatum"],
  ],
  material_tag: [
    ["id",          "INT", "PK, AI",  "Eindeutige Verbindungs-ID"],
    ["material_id", "INT", "FK",      "Verweis auf material(id)"],
    ["tag_id",      "INT", "FK",      "Verweis auf tag(id)"],
  ],
  version: [
    ["id",              "INT",       "PK, AI",  "Eindeutige Versions-ID"],
    ["material_id",     "INT",       "FK",      "Verweis auf material(id)"],
    ["autor_id",        "INT",       "FK",      "Verweis auf benutzer(id)"],
    ["version_nr",      "INT",       "",        "Versionsnummer"],
    ["aenderungsdatum", "TIMESTAMP", "",        "Zeitpunkt der Änderung"],
    ["aenderungen",     "TEXT",      "",        "Beschreibung der vorgenommenen Änderungen"],
  ],
};

function buildSchemaTable(rows) {
  return new Table({
    width: { size: CW, type: WidthType.DXA },
    columnWidths: [S1, S2, S3, S4],
    rows: [
      new TableRow({ tableHeader: true, children: [th("Spalte", S1), th("Datentyp", S2), th("Schlüssel", S3), th("Beschreibung", S4)] }),
      ...rows.map(([sp, dt, k, d], i) => new TableRow({
        children: [mc(sp, S1, i%2===0), mc(dt, S2, i%2===0), td(k, S3, i%2===0), td(d, S4, i%2===0)]
      }))
    ]
  });
}

// ── Document ───────────────────────────────────────────────────────────────

const doc = new Document({
  creator: "Auric Ergeson",
  title: "LF8 Softwaredokumentation – Lernmaterialverwaltung",
  styles: {
    default: { document: { run: { font: "Arial", size: 22 } } },
    paragraphStyles: [
      {
        id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "Arial", color: C_H1 },
        paragraph: { spacing: { before: 360, after: 180 }, outlineLevel: 0 }
      },
      {
        id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 24, bold: true, font: "Arial", color: C_H2 },
        paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 1 }
      },
    ]
  },
  sections: [
    // ── Cover page (no header/footer) ──────────────────────────────────────
    {
      properties: { ...PAGE_PROPS },
      children: [
        sp(), sp(), sp(), sp(), sp(), sp(), sp(),
        new Paragraph({
          alignment: AlignmentType.CENTER, spacing: { after: 200 },
          children: [new TextRun({ text: "Softwaredokumentation", font: "Arial", size: 56, bold: true, color: "111111" })]
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER, spacing: { after: 500 },
          children: [new TextRun({ text: "LF8 – Daten systemübergreifend bereitstellen", font: "Arial", size: 28, color: C_GREY })]
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER, spacing: { after: 140 },
          children: [new TextRun({ text: "Projekt: Lernmaterialverwaltung", font: "Arial", size: 24 })]
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER, spacing: { after: 140 },
          children: [new TextRun({ text: "Autor: Auric Ergeson", font: "Arial", size: 24 })]
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER, spacing: { after: 140 },
          children: [new TextRun({ text: "Datum: Mai 2026", font: "Arial", size: 24 })]
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER, spacing: { after: 120 },
          children: [new TextRun({ text: "Berufsschule – Anwendungsentwickler", font: "Arial", size: 22, italics: true, color: C_LGREY })]
        }),
        new Paragraph({ children: [new PageBreak()] }),
      ]
    },
    // ── Table of contents ──────────────────────────────────────────────────
    {
      properties: { ...PAGE_PROPS },
      children: [
        new Paragraph({
          spacing: { before: 0, after: 360 },
          children: [new TextRun({ text: "Inhaltsverzeichnis", font: "Arial", size: 32, bold: true, color: C_H1 })]
        }),
        new TableOfContents("Inhaltsverzeichnis", { hyperlink: true, headingStyleRange: "1-2" }),
        new Paragraph({ children: [new PageBreak()] }),
      ]
    },
    // ── Body (header + footer) ─────────────────────────────────────────────
    {
      properties: { ...PAGE_PROPS },
      headers: {
        default: new Header({
          children: [new Paragraph({
            border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: C_H2, space: 1 } },
            tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
            children: [
              new TextRun({ text: "LF8 – Lernmaterialverwaltung", font: "Arial", size: 18, color: C_GREY }),
              new TextRun({ text: "\tAuric Ergeson", font: "Arial", size: 18, color: C_GREY }),
            ]
          })]
        })
      },
      footers: {
        default: new Footer({
          children: [new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [
              new TextRun({ text: "Seite ", font: "Arial", size: 18, color: C_LGREY }),
              new TextRun({ children: [PageNumber.CURRENT], font: "Arial", size: 18, color: C_LGREY }),
              new TextRun({ text: " von ", font: "Arial", size: 18, color: C_LGREY }),
              new TextRun({ children: [PageNumber.TOTAL_PAGES], font: "Arial", size: 18, color: C_LGREY }),
            ]
          })]
        })
      },
      children: [
        // 1. Projektbeschreibung
        h1("1. Projektbeschreibung"),
        p("Die Lernmaterialverwaltung ist eine konsolenbasierte Python-Anwendung, mit der Lehrkräfte und Auszubildende Lernmaterialien digital verwalten können. Über ein textbasiertes Menü lassen sich Dateien hochladen, suchen, herunterladen, kommentieren und löschen."),
        p("Alle Materialien werden in einer MySQL-Datenbank gespeichert und mit Metadaten versehen: Titel, Dateityp, Themengebiet, Autor und Zeitstempel. Dateien unter 1 MB speichert das System direkt als Binärdaten in der Datenbank. Größere Dateien werden im Ordner uploads/ abgelegt und nur über den Pfad referenziert."),
        p("Das Projekt entstand im Rahmen von Lernfeld 8. Es ersetzt die bisherige Praxis, Materialien unstrukturiert in verschiedenen Verzeichnissen abzulegen oder per E-Mail weiterzugeben."),
        sp(),

        // 2. Zielsetzung
        h1("2. Zielsetzung"),
        p("Ziel war es, eine einfache, datenbankgestützte Anwendung zu entwickeln, die Lernmaterialien zentral speicherbar und durchsuchbar macht. Statt Dateien in verschiedenen Ordnern zu verteilen, sollten alle Materialien an einem Ort liegen – einheitlich mit Metadaten versehen und über ein Menü zugänglich."),
        p("Technisch waren MySQL als Datenbank, Python als Sprache und eine textbasierte Bedienung vorgegeben. Die Speicherstrategie – kleine Dateien in der Datenbank, große Dateien im Dateisystem – war Teil der Aufgabenstellung. Zusätzlich mussten mindestens sieben SQL-Abfragen mit verschiedenen Join- und Aggregationstypen umgesetzt werden."),
        sp(),

        // 3. Arbeitsprozess
        h1("3. Arbeitsprozess"),
        p("Bevor eine einzige Zeile Python geschrieben wurde, haben wir die Datenbankstruktur geplant. Das war bewusst so entschieden: Wenn die Datenbank nicht stimmt, zieht sich das durch den ganzen Code."),
        p("Die größte Herausforderung war das Datenbankdesign selbst. Es war nicht sofort klar, wie viele Tabellen wir brauchen und wie sie zusammenhängen. Besonders die Frage, wie Tags gespeichert werden – ob als Freitext in der material-Tabelle oder in einer eigenen Tabelle – hat einige Überlegungen erfordert. Wir haben uns für eine separate tag-Tabelle mit Verbindungstabelle material_tag entschieden, weil das die sauberere Lösung im Sinne der Normalisierung ist."),
        p("Auch die Speicherstrategie musste vorab festgelegt werden: Dateien unter 1 MB kommen direkt in die Datenbank, größere Dateien ins Dateisystem. Diese Grenze ist im Code als Konstante (MAX_SIZE) definiert."),

        h2("Umsetzung"),
        p("Nach Fertigstellung des Datenbankschemas begann die Python-Implementierung in drei Schritten: zuerst database.py (Verbindung und automatisches Tabellen-Mapping), dann services.py (alle Datenbankfunktionen), zuletzt main.py (das Konsolenmenü)."),
        p("Das Menü wurde so aufgebaut, dass jede Funktion eine eigene Funktion im Code hat. Das hat es einfach gemacht, einzelne Teile zu testen und später zu erweitern."),

        h2("Reflexion"),
        p("Was gut funktioniert hat: Das Konsolenmenü ist übersichtlich, alle sieben SQL-Abfragen laufen stabil, und die Datenbankstruktur hat sich während der Entwicklung kaum verändert – ein Zeichen dafür, dass die Planung am Anfang gründlich war."),
        p("Was wir beim nächsten Projekt anders machen würden: Früher mit dem Testen anfangen und nicht erst am Ende prüfen, ob alles funktioniert. Außerdem wäre eine einfache Fehlerprotokollierung hilfreich gewesen, um Probleme bei der Datenbankverbindung schneller zu erkennen."),
        p("Eine persönliche Anmerkung: Da Deutsch nicht meine Muttersprache ist, hat mein Ausbilder bei einzelnen Formulierungen in der Dokumentation geholfen und ich habe stellenweise Google Übersetzer genutzt. Der gesamte Quellcode sowie der überwiegende Teil der Dokumentation wurden eigenständig verfasst."),
        sp(),

        // 4. Funktionsübersicht
        h1("4. Funktionsübersicht"),
        p("Die Anwendung bietet folgende Funktionen, erreichbar über das Hauptmenü:"),
        sp(),
        buildFunktionsTable(),
        sp(),

        // 4. Implementierungsdetails
        h1("5. Implementierungsdetails"),

        h2("Architektur"),
        p("Das Programm ist in drei Schichten aufgeteilt. database.py stellt die Verbindung zur MySQL-Datenbank her und lädt alle Tabellen über SQLAlchemys automap_base() automatisch. services.py enthält alle Datenbankfunktionen, von einfachen Abfragen bis zu den sieben Auswertungen. main.py ist die Benutzeroberfläche: ein Menü, das Eingaben entgegennimmt und die passenden Funktionen aus services.py aufruft."),

        h2("Verwendete Bibliotheken"),
        p("SQLAlchemy 2.0 wird als ORM eingesetzt. Statt SQL direkt zu schreiben, werden Python-Objekte genutzt. Die automap-Funktion liest bestehende Tabellen automatisch aus, ohne dass Modellklassen manuell definiert werden müssen. PyMySQL 1.1 ist der Treiber, der SQLAlchemy mit dem MySQL-Server verbindet."),
        p("rich 15.0 gibt formatierte Tabellen und farbigen Text in der Konsole aus, ohne grafische Oberfläche. python-dotenv 1.2 lädt Zugangsdaten aus einer .env-Datei, damit Passwörter nicht direkt im Code stehen."),

        h2("Speicherstrategie"),
        p("Beim Upload wird die Dateigröße geprüft. Ist sie kleiner als 1.048.576 Bytes (1 MB), wird der Inhalt als LONGBLOB in der Tabelle material gespeichert und is_in_database auf TRUE gesetzt. Größere Dateien werden in den Ordner uploads/ kopiert, und nur der Pfad wird in der Spalte speicherort hinterlegt (is_in_database = FALSE). Beim Download entscheidet das System anhand dieses Flags, ob der Inhalt aus der Datenbank gelesen oder die Datei vom Dateisystem kopiert wird."),

        h2("Die sieben Datenbankabfragen"),
        p("Abfrage 1 – Materialien pro Themengebiet: COUNT-Aggregation mit GROUP BY. Zeigt, wie viele Materialien je Thema gespeichert sind (JOIN auf themengebiet)."),
        p("Abfrage 2 – Durchschnittliche Dateigröße pro Dateityp: AVG-Aggregation mit GROUP BY auf material.dateityp."),
        p("Abfrage 3 – Materialien mit Themengebiet: INNER JOIN zwischen material und themengebiet."),
        p("Abfrage 4 – Materialien mit Kommentaren: INNER JOIN zwischen material und kommentar."),
        p("Abfrage 5 – Kommentaranzahl pro Material: INNER JOIN mit COUNT (JOIN + Aggregation kombiniert)."),
        p("Abfrage 6 – Material mit Autor und Thema: Zwei JOINs auf benutzer und themengebiet."),
        p("Abfrage 7 – Vollständige Suche: Drei JOINs auf benutzer, themengebiet und kategorie, mit optionalen WHERE-Filtern nach Thema oder Autor."),
        sp(),

        h2("Quellcode-Kommentare"),
        p("Alle drei Python-Dateien sind auf Deutsch kommentiert. Jede Funktion hat einen erklärenden Kommentar direkt über der Definition. Wichtige Konstanten und technische Entscheidungen sind ebenfalls dokumentiert. Einige Beispiele aus dem Quellcode:"),
        sp(),
        code("# database.py"),
        code("# Hier verbinden wir uns mit der MySQL-Datenbank."),
        code("# Die Zugangsdaten kommen aus der .env Datei."),
        code(""),
        code("# SessionLocal öffnet eine neue Verbindung wenn wir sie brauchen"),
        code("SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)"),
        code(""),
        code("# SQLAlchemy liest die Tabellen automatisch aus der Datenbank"),
        code("Base = automap_base()"),
        sp(),
        code("# services.py"),
        code("# Dateien kleiner als 1 MB kommen direkt in die Datenbank"),
        code("MAX_SIZE = 1 * 1024 * 1024"),
        code(""),
        code("# Eine Datei hochladen – kleine Dateien in die DB, große auf die Festplatte"),
        code("def upload_material(db, file_path, titel, beschreibung, ...):"),
        code(""),
        code("# Abfrage 1: Wie viele Materialien gibt es pro Themengebiet? (COUNT)"),
        code("def anzahl_material_pro_themen(db):"),
        sp(),
        code("# main.py"),
        code("# Menü zum Hochladen – Benutzer gibt Dateipfad und Infos ein"),
        code("def upload_menu():"),
        code(""),
        code("# Das Hauptmenü – hier startet alles"),
        code("def hauptmenu():"),
        sp(),

        // 5. SQL-Code
        h1("6. SQL-Code"),
        p("Der folgende SQL-Code erstellt die Datenbank lernmaterialverwaltung mit allen acht Tabellen und zwei Triggern:"),
        sp(),
        ...SQL.split('\n').map(line => code(line)),
        sp(),

        // 6. ERD und ERM
        h1("7. ERD und ERM"),
        p("Das folgende Entity-Relationship-Diagramm wurde mit DBeaver aus der bestehenden MySQL-Datenbank generiert. Es zeigt alle acht Tabellen mit Spalten, Datentypen, Primärschlüsseln (fett markiert) und Fremdschlüsselbeziehungen (Linien mit Kardinalitätsangaben)."),
        sp(),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { after: 60 },
          children: [new ImageRun({
            type: "png",
            data: ERD_IMG,
            transformation: { width: 600, height: 482 },
            altText: { title: "ERD", description: "Entity-Relationship-Diagramm der Lernmaterialverwaltung", name: "ERD" }
          })]
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { after: 180 },
          children: [new TextRun({ text: "Abbildung 1: ERD der Datenbank lernmaterialverwaltung (generiert mit DBeaver)", font: "Arial", size: 18, italics: true, color: C_LGREY })]
        }),
        sp(),

        h2("Normalisierung"),
        p("Die Datenbank wurde von Beginn an nach den Regeln der drei Normalformen entworfen. Ein erster Entwurf hätte Tags als Freitext-Spalte in der material-Tabelle speichern können – das wäre jedoch nicht normalisiert. Stattdessen wurden Tags in eine eigene Tabelle ausgelagert."),
        p("Erste Normalform (1NF): Alle Spalten enthalten atomare Werte ohne Wiederholungsgruppen. Tags sind nicht als kommaseparierte Liste in material gespeichert, sondern über die Verbindungstabelle material_tag referenziert."),
        p("Zweite Normalform (2NF): Da alle Tabellen einspaltige Primärschlüssel (id) verwenden, gibt es keine partiellen Abhängigkeiten. Jedes Nicht-Schlüssel-Attribut hängt vollständig vom Primärschlüssel ab."),
        p("Dritte Normalform (3NF): Es gibt keine transitiven Abhängigkeiten. Der Autor eines Materials wird als Fremdschlüssel (benutzer_id) referenziert, nicht als Freitext. Dasselbe gilt für themengebiet_id und kategorie_id – jede davon zeigt auf eine eigene Tabelle mit weiteren Attributen."),
        sp(),

        h2("Entitäten und Beziehungen"),
        bp("benutzer – Benutzerinformationen"),
        p("Attribute: id (PK, AI), username (UNIQUE), email (UNIQUE), rolle (Lehrer/Azubi/Admin), created_at"),
        p("Beziehungen: 1:N zu material, 1:N zu kommentar, 1:N zu version."),
        sp(),

        bp("themengebiet – Fachgebiete der Materialien"),
        p("Attribute: id (PK, AI), name (UNIQUE), beschreibung"),
        p("Beziehungen: 1:N zu material."),
        sp(),

        bp("kategorie – Feinkategorisierung"),
        p("Attribute: id (PK, AI), name (UNIQUE), beschreibung"),
        p("Beziehungen: 1:N zu material."),
        sp(),

        bp("tag – Freie Schlagwörter"),
        p("Attribute: id (PK, AI), name (UNIQUE)"),
        p("Beziehungen: N:M zu material über material_tag."),
        sp(),

        bp("material – Zentrales Objekt der Anwendung"),
        p("Attribute: id, titel, beschreibung, themengebiet_id (FK), benutzer_id (FK), kategorie_id (FK), erstellungsdatum, aenderungsdatum, dateiname, dateityp, dateigroesse, speicherort, inhalt (LONGBLOB), is_in_database"),
        p("Beziehungen: Gehört zu 1 themengebiet, 1 benutzer, 1 kategorie. Hat 1:N zu kommentar und version. N:M zu tag über material_tag."),
        sp(),

        bp("kommentar – Rückmeldungen zu Materialien"),
        p("Attribute: id (PK, AI), material_id (FK), autor_id (FK), text, erstellungsdatum, aenderungsdatum"),
        p("Beziehungen: Gehört zu 1 material und 1 benutzer."),
        sp(),

        bp("material_tag – Verbindungstabelle (N:M)"),
        p("Attribute: id (PK, AI), material_id (FK), tag_id (FK)"),
        p("Beziehungen: Verbindet material und tag in einer N:M-Beziehung."),
        sp(),

        bp("version – Versionshistorie"),
        p("Attribute: id (PK, AI), material_id (FK), autor_id (FK), version_nr, aenderungsdatum, aenderungen"),
        p("Beziehungen: Gehört zu 1 material und 1 benutzer."),
        sp(),

        // 7. Normalisierte Tabellenstruktur
        h1("8. Normalisierte Tabellenstruktur"),
        p("Alle Tabellen liegen in der dritten Normalform (3NF) vor. Jede Spalte ist direkt vom Primärschlüssel abhängig, ohne partielle oder transitive Abhängigkeiten."),
        sp(),

        ...Object.entries(TABLES).flatMap(([name, rows]) => [
          bp("Tabelle: " + name),
          buildSchemaTable(rows),
          sp(),
        ]),

        // 9. Installation und Inbetriebnahme
        h1("9. Installation und Inbetriebnahme"),
        p("Um die Anwendung lokal auszuführen, werden Python 3.10 (oder neuer), MySQL 8.0 und pip benötigt."),
        sp(),

        h2("Schritt 1 – Abhängigkeiten installieren"),
        p("Im Projektverzeichnis folgenden Befehl ausführen:"),
        code("pip install -r requirements.txt"),
        sp(),

        h2("Schritt 2 – .env Datei anlegen"),
        p("Im Projektverzeichnis eine Datei mit dem Namen .env erstellen und folgende Werte eintragen:"),
        code("DB_DRIVER=mysql+pymysql"),
        code("DB_USERNAME=root"),
        code("DB_PASSWORD=IhrPasswort"),
        code("DB_HOST=localhost"),
        code("DB_PORT=3306"),
        code("DB_NAME=lernmaterialverwaltung"),
        sp(),

        h2("Schritt 3 – Datenbank einrichten"),
        p("Das SQL-Schema in MySQL importieren (einmalig, erstellt die Datenbank und alle Tabellen):"),
        code("mysql -u root -p < sql/schema.sql"),
        sp(),

        h2("Schritt 4 – Anwendung starten"),
        p("In den app-Ordner wechseln und das Programm starten:"),
        code("cd app"),
        code("python main.py"),
        p("Das Hauptmenü erscheint direkt im Terminal. Die Anwendung läuft vollständig textbasiert und benötigt keine grafische Oberfläche."),
        sp(),
      ]
    }
  ]
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync("LF8_Dokumentation.docx", buf);
  console.log("OK LF8_Dokumentation.docx geschrieben (" + buf.length.toLocaleString() + " Bytes)");
}).catch(err => {
  console.error("Fehler:", err.message);
  process.exit(1);
});
