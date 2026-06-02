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

// ── Additional helpers ─────────────────────────────────────────────────────

const pItalic = (text) => new Paragraph({
  spacing: { after: 120 },
  children: [new TextRun({ text, font: "Arial", size: 22, color: C_LGREY, italics: true })]
});

const anhangH1 = (label, title) => new Paragraph({
  heading: HeadingLevel.HEADING_1,
  children: [new TextRun(label + ": " + title)]
});

const tdb = (text, w) => new TableCell({
  borders: CELL_BORDERS, width: { size: w, type: WidthType.DXA },
  shading: { fill: "DDEEFF", type: ShadingType.CLEAR }, margins: PAD,
  children: [new Paragraph({ children: [new TextRun({ text, font: "Arial", size: 20, bold: true, color: C_H1 })] })]
});

// ── SQL content (read from file) ───────────────────────────────────────────

const SQL = fs.readFileSync('sql/schema.sql', 'utf8');

const ERD_IMG = fs.readFileSync('lernmaterialverwaltung.png');

// ── Zeitplanung table ──────────────────────────────────────────────────────

const Z1 = 3200, Z2 = 1800, Z3 = 1900, Z4 = 2171;

function buildZeitplanungTable() {
  const rows = [
    ["Analyse & Planung",            "4 h",  "5 h",  "+1 h"],
    ["DB-Design (ERD, ERM, Schema)", "6 h",  "8 h",  "+2 h"],
    ["Python-Implementierung",       "15 h", "18 h", "+3 h"],
    ["Testen & Debugging",           "4 h",  "5 h",  "+1 h"],
    ["Dokumentation",                "6 h",  "7 h",  "+1 h"],
  ];
  return new Table({
    width: { size: CW, type: WidthType.DXA },
    columnWidths: [Z1, Z2, Z3, Z4],
    rows: [
      new TableRow({ tableHeader: true, children: [th("Phase", Z1), th("Geplant", Z2), th("Tatsächlich", Z3), th("Abweichung", Z4)] }),
      ...rows.map(([phase, geplant, tats, abw], i) => new TableRow({
        children: [td(phase, Z1, i%2===0), td(geplant, Z2, i%2===0), td(tats, Z3, i%2===0), td(abw, Z4, i%2===0)]
      })),
      new TableRow({ children: [tdb("Gesamt", Z1), tdb("35 h", Z2), tdb("43 h", Z3), tdb("+8 h", Z4)] })
    ]
  });
}

// ── Anhangsverzeichnis table ───────────────────────────────────────────────

const AV1 = 2300, AV2 = 6771;

function buildAnhangsverzeichnis() {
  const entries = [
    ["Anhang I",   "SQL-Schema (vollständige Datenbankdefinition)"],
    ["Anhang II",  "ERD und ERM (Datenbankdiagramm und Entitätsbeschreibungen)"],
    ["Anhang III", "Normalisierte Tabellenstruktur (alle 8 Tabellen)"],
    ["Anhang IV",  "Implementierungsdetails (Architektur, Bibliotheken, SQL-Abfragen)"],
    ["Anhang V",   "Installationsanleitung"],
  ];
  return new Table({
    width: { size: CW, type: WidthType.DXA },
    columnWidths: [AV1, AV2],
    rows: [
      new TableRow({ tableHeader: true, children: [th("Bezeichnung", AV1), th("Inhalt", AV2)] }),
      ...entries.map(([bez, inh], i) => new TableRow({
        children: [td(bez, AV1, i%2===0), td(inh, AV2, i%2===0)]
      }))
    ]
  });
}

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
      ...rows.map(([col, dt, k, d], i) => new TableRow({
        children: [mc(col, S1, i%2===0), mc(dt, S2, i%2===0), td(k, S3, i%2===0), td(d, S4, i%2===0)]
      }))
    ]
  });
}

// ── Document ───────────────────────────────────────────────────────────────

const doc = new Document({
  creator: "Auric Ergeson",
  title: "LF8 Projektbericht – Lernmaterialverwaltung",
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
          children: [new TextRun({ text: "Prozessorientierter Projektbericht", font: "Arial", size: 52, bold: true, color: "111111" })]
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

        // ── 1. Projektauftrag ──────────────────────────────────────────────
        h1("1. Projektauftrag"),

        h2("1.1 Ausgangssituation"),
        p("An unserer Berufsschule wurden Lernmaterialien bisher hauptsächlich per E-Mail weitergegeben oder in verschiedenen Ordnern auf Schulrechnern abgelegt. Ein Lehrer hatte zum Beispiel Unterlagen für dasselbe Thema in drei verschiedenen Verzeichnissen gespeichert – ohne einheitliche Benennung und ohne dass die Azubis wussten, welche Version aktuell war."),
        p("Im Rahmen von Lernfeld 8 wurde mir die Aufgabe gestellt, eine datenbankgestützte Lösung zu entwickeln, die dieses Problem systematisch löst. Ich habe das Projekt vom 06.04.2026 bis zum 16.05.2026 als Einzelprojekt durchgeführt."),
        p("Ein Problem war von Anfang an klar: Die Lösung muss einfach zu bedienen sein, weil nicht alle Nutzer technisch erfahren sind. Deshalb habe ich mich für eine konsolenbasierte Anwendung entschieden, die ohne grafische Oberfläche auskommt."),

        h2("1.2 Aufgabenstellung"),
        p("Das System sollte es ermöglichen, Lernmaterialien zentral zu speichern, zu suchen und herunterzuladen. Zusätzlich waren folgende technische Anforderungen vorgegeben: MySQL als Datenbank, Python als Programmiersprache, mindestens sieben SQL-Abfragen mit unterschiedlichen JOIN- und Aggregationstypen sowie eine duale Speicherstrategie für Dateien."),
        p("Ich habe die Anforderungen in acht konkrete Funktionen übersetzt, die alle über ein Hauptmenü erreichbar sind. Die genaue Auflistung zeigt Kapitel 4 – Funktionsübersicht."),

        h2("1.3 Projektumfeld"),
        p("Das Projekt war ein Einzelprojekt. Ich habe es auf meinem privaten Laptop entwickelt, auf dem MySQL 8.0, Python 3.12 und Visual Studio Code installiert sind. Die Datenbankmodellierung habe ich mit DBeaver durchgeführt, das auch das ERD-Diagramm erzeugt hat."),
        p("Als Versionskontrolle habe ich Git verwendet. Schnittstellen zu anderen Systemen gibt es nicht – die Anwendung läuft vollständig lokal. Die einzige externe Abhängigkeit ist die MySQL-Datenbank, die auf demselben Rechner läuft."),
        pItalic("(ERD-Diagramm: siehe Anhang II)"),
        sp(),

        // ── 2. Projektplanung ──────────────────────────────────────────────
        h1("2. Projektplanung"),

        h2("2.1 Lösungsansatz und Alternativen"),
        p("Zunächst war unklar, ob ich eine webbasierte Anwendung oder eine Kommandozeilenanwendung entwickeln soll. Eine Webanwendung mit Flask wäre benutzerfreundlicher gewesen, hätte aber deutlich mehr Entwicklungszeit benötigt und war für den vorgegebenen Zeitraum nicht realistisch."),
        p("Ich habe mich deshalb bewusst für die Kommandozeilenlösung entschieden. Der Vorteil: Ich konnte mich auf die Datenbanklogik konzentrieren, die der eigentliche Kern der Aufgabe war. Python bietet mit SQLAlchemy eine mächtige ORM-Bibliothek, die mir das Arbeiten mit der Datenbank deutlich erleichtert hat."),
        p("Bei der Datenbankstruktur hatte ich zunächst überlegt, Tags als kommaseparierte Liste direkt in der material-Tabelle zu speichern. Das wäre einfacher gewesen, hätte aber gegen die erste Normalform verstoßen. Ich habe mich deshalb für eine separate tag-Tabelle mit Verbindungstabelle material_tag entschieden."),

        h2("2.2 Zeitplanung"),
        p("Das Projekt lief über sechs Wochen (06.04.2026 – 16.05.2026). Die folgende Tabelle zeigt die geplanten und tatsächlich benötigten Stunden pro Arbeitspaket."),
        pItalic("(Zeitvergleich mit Abweichungen: siehe Kapitel 5.2)"),
        sp(),
        buildZeitplanungTable(),
        sp(),

        // ── 3. Projektdurchführung ─────────────────────────────────────────
        h1("3. Projektdurchführung"),

        h2("3.1 Datenbankdesign"),
        p("Bevor ich mit dem Programmieren angefangen habe, habe ich zuerst das Datenbankschema entworfen. Das war eine bewusste Entscheidung: Wenn die Datenbankstruktur nicht stimmt, zieht sich das durch den gesamten Code."),
        p("Ein Problem beim Design war die Frage der Dateispeicherung. Ich habe mich für eine duale Strategie entschieden: Dateien unter 1 MB werden direkt als LONGBLOB in der Datenbank gespeichert, größere Dateien werden im Ordner uploads/ abgelegt. Das vollständige Schema ist in Anhang I dokumentiert, das ERD-Diagramm in Anhang II."),
        p("Die Normalisierung habe ich nach den drei Normalformen durchgeführt. Besonders die Entscheidung, Tags in eine eigene Tabelle auszulagern, war wichtig für die 1NF. Die vollständige Tabellenstruktur mit allen Spalten und Datentypen ist in Anhang III dargestellt."),
        pItalic("(SQL-Schema: siehe Anhang I – ERD: siehe Anhang II – Tabellenstruktur: siehe Anhang III)"),

        h2("3.2 Implementierung"),
        p("Die Implementierung habe ich in drei Phasen aufgeteilt: zuerst database.py (Datenbankverbindung und Tabellen-Mapping), dann services.py (alle Datenbankfunktionen), zuletzt main.py (das Konsolenmenü). Diese Reihenfolge hat sich bewährt, weil ich immer auf fertigen Schichten aufgebaut habe."),
        p("Ein Problem war anfangs die SQLAlchemy automap-Funktion. Ich wusste nicht, dass die Tabellen zuerst in der Datenbank existieren müssen, bevor automap_base() sie einlesen kann. Das hat beim ersten Test zu einem Fehler geführt. Die Lösung war, das Schema zuerst zu importieren und erst danach die Python-Anwendung zu starten."),
        p("Die sieben SQL-Abfragen habe ich alle in services.py implementiert. Abfrage 7 ist die komplexeste: Sie verbindet vier Tabellen (material, benutzer, themengebiet, kategorie) mit drei JOINs und unterstützt optionale WHERE-Filter. Die Architektur und alle sieben Abfragen sind in Anhang IV ausführlich dokumentiert."),
        pItalic("(Architektur und SQL-Abfragen: siehe Anhang IV)"),

        h2("3.3 Ergebnisse"),
        p("Das Ergebnis ist eine vollständig funktionsfähige Kommandozeilenanwendung mit acht Menüpunkten. Alle sieben SQL-Abfragen laufen stabil, die duale Speicherstrategie funktioniert zuverlässig, und das Menü ist übersichtlich strukturiert."),
        p("Beim Testen habe ich festgestellt, dass die Ausgabe bei langen Titeln in der rich-Tabelle manchmal abgeschnitten wurde. Ich habe das gelöst, indem ich die Spaltenbreiten in der Tabellenformatierung angepasst habe. Insgesamt bin ich mit dem Ergebnis zufrieden – alle geforderten Funktionen sind umgesetzt."),
        sp(),

        // ── 4. Funktionsübersicht ──────────────────────────────────────────
        h1("4. Funktionsübersicht"),
        p("Die Anwendung bietet folgende acht Funktionen, die alle über das Hauptmenü erreichbar sind:"),
        sp(),
        buildFunktionsTable(),
        sp(),

        // ── 5. Projektabschluss ────────────────────────────────────────────
        h1("5. Projektabschluss"),

        h2("5.1 Soll-Ist-Vergleich"),
        p("Alle geforderten Funktionen wurden umgesetzt: die acht Menüpunkte, die sieben SQL-Abfragen, die duale Speicherstrategie und die vollständige Datenbankstruktur in 3NF. Die Anforderungen aus Kapitel 1.2 wurden damit vollständig erfüllt."),
        p("Nicht umgesetzt wurde eine grafische Oberfläche – das war aber auch keine Anforderung. Eine mögliche Erweiterung wäre eine einfache Web-GUI mit Flask, die ich bei mehr Zeit als Nächstes umsetzen würde."),

        h2("5.2 Zeitaufwand-Vergleich"),
        p("Insgesamt habe ich 43 Stunden benötigt, geplant waren 35 Stunden – eine Überschreitung von 8 Stunden bzw. etwa 23 %. Die größte Abweichung gab es bei der Python-Implementierung: statt 15 Stunden habe ich 18 Stunden gebraucht. Das lag hauptsächlich an dem bereits erwähnten Problem mit der SQLAlchemy automap-Funktion und an mehreren kleineren Bugs beim Datei-Upload."),
        p("Im Nachhinein hätte ich die Zeitplanung realistischer einschätzen können. Für zukünftige Projekte werde ich bei unbekannten Bibliotheken mehr Pufferzeit einplanen."),

        h2("5.3 Persönliche Reflexion"),
        p("Was gut funktioniert hat: Die Entscheidung, zuerst die Datenbank zu entwerfen und erst dann zu programmieren, war richtig. Das Konsolenmenü ist übersichtlich, und die Trennung in drei Python-Dateien (database.py, services.py, main.py) macht den Code gut wartbar."),
        p("Was ich beim nächsten Mal anders machen würde: früher mit dem Testen anfangen und nicht erst am Ende. Außerdem hätte ich die SQL-Abfragen früher direkt in der Datenbank testen sollen, bevor ich sie in Python übersetzt habe – das hätte einige Debugging-Runden gespart."),
        p("Eine persönliche Anmerkung: Da Deutsch nicht meine Muttersprache ist, hat mein Ausbilder bei einzelnen Formulierungen in der Dokumentation geholfen und ich habe stellenweise Google Übersetzer genutzt. Der gesamte Quellcode sowie der überwiegende Teil der Dokumentation wurden eigenständig verfasst."),
        sp(),

        // ── 6. Quellenverzeichnis ──────────────────────────────────────────
        h1("6. Quellenverzeichnis"),
        p("Die folgenden Quellen wurden bei der Entwicklung und Dokumentation dieses Projekts verwendet:"),
        sp(),
        p("[1]  Python Software Foundation: Python 3.12 Dokumentation. Online verfügbar unter: https://docs.python.org/3/ (Zugriff: 16.05.2026)."),
        p("[2]  SQLAlchemy Authors: SQLAlchemy 2.0 Dokumentation. Online verfügbar unter: https://docs.sqlalchemy.org/en/20/ (Zugriff: 16.05.2026)."),
        p("[3]  Oracle Corporation: MySQL 8.0 Reference Manual. Online verfügbar unter: https://dev.mysql.com/doc/refman/8.0/en/ (Zugriff: 16.05.2026)."),
        sp(),

        // ── Page break before Anhangsverzeichnis ──────────────────────────
        new Paragraph({ children: [new PageBreak()] }),

        // ── Anhangsverzeichnis ─────────────────────────────────────────────
        h1("Anhangsverzeichnis"),
        p("Die folgenden Anhänge enthalten die technischen Details des Projekts, die den Lesefluss des Berichts unterbrochen hätten, wenn sie direkt in den Haupttext integriert worden wären. Alle Anhänge werden im Bericht mit \"(siehe Anhang X)\" referenziert."),
        sp(),
        buildAnhangsverzeichnis(),
        sp(),

        // ── Anhang I: SQL-Schema ───────────────────────────────────────────
        new Paragraph({ children: [new PageBreak()] }),
        anhangH1("Anhang I", "SQL-Schema"),
        p("Das folgende SQL-Skript erstellt die Datenbank lernmaterialverwaltung vollständig neu: Datenbank, alle acht Tabellen mit Spalten, Datentypen, Primär- und Fremdschlüsseln, sowie zwei Trigger für die automatische Aktualisierung von Zeitstempeln."),
        sp(),
        ...SQL.split('\n').map(line => code(line)),
        sp(),

        // ── Anhang II: ERD und ERM ─────────────────────────────────────────
        new Paragraph({ children: [new PageBreak()] }),
        anhangH1("Anhang II", "ERD und ERM"),
        p("Das folgende Entity-Relationship-Diagramm wurde mit DBeaver aus der bestehenden MySQL-Datenbank generiert. Es zeigt alle acht Tabellen mit Spalten, Datentypen, Primärschlüsseln (fett markiert) und Fremdschlüsselbeziehungen (Linien mit Kardinalitätsangaben)."),
        p("Die Linien im Diagramm entsprechen den Fremdschlüsselbeziehungen aus dem Schema: material referenziert benutzer, themengebiet und kategorie; material_tag verbindet material und tag in einer N:M-Beziehung; kommentar und version referenzieren jeweils material und benutzer."),
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

        // ── Anhang III: Normalisierte Tabellenstruktur ─────────────────────
        new Paragraph({ children: [new PageBreak()] }),
        anhangH1("Anhang III", "Normalisierte Tabellenstruktur"),
        p("Alle acht Tabellen liegen in der dritten Normalform (3NF) vor. Jede Spalte ist direkt vom Primärschlüssel abhängig – es gibt weder partielle noch transitive Abhängigkeiten."),
        p("Erste Normalform (1NF): Alle Spalten enthalten atomare Werte. Tags sind nicht als kommaseparierte Liste gespeichert, sondern über die Verbindungstabelle material_tag referenziert. Zweite Normalform (2NF): Alle Tabellen haben einspaltige Primärschlüssel (id), daher gibt es keine partiellen Abhängigkeiten. Dritte Normalform (3NF): Alle Fremdschlüssel (benutzer_id, themengebiet_id, kategorie_id) zeigen auf eigene Tabellen – keine transitiven Abhängigkeiten."),
        sp(),

        ...Object.entries(TABLES).flatMap(([name, rows]) => [
          bp("Tabelle: " + name),
          buildSchemaTable(rows),
          sp(),
        ]),

        // ── Anhang IV: Implementierungsdetails ────────────────────────────
        new Paragraph({ children: [new PageBreak()] }),
        anhangH1("Anhang IV", "Implementierungsdetails"),

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
        p("Alle drei Python-Dateien sind auf Deutsch kommentiert. Jede Funktion hat einen erklärenden Kommentar direkt über der Definition. Wichtige Konstanten und technische Entscheidungen sind ebenfalls dokumentiert. Einige Beispiele:"),
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

        // ── Anhang V: Installationsanleitung ──────────────────────────────
        new Paragraph({ children: [new PageBreak()] }),
        anhangH1("Anhang V", "Installationsanleitung"),
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
