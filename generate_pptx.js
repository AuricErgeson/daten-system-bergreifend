const pptxgen = require('pptxgenjs');
const path = require('path');

const pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';
pres.author = 'Auric Ergeson';
pres.title = 'Lernmaterialverwaltung — LF8 Präsentation';

const C = {
  red:       'C8201A',
  black:     '111111',
  white:     'FFFFFF',
  grayDark:  '2A2A2A',
  grayMid:   '7A7A7A',
  grayLight: 'E4E4E4',
  grayUltra: 'F7F7F7',
  redLight:  'FFF0EF',
};

const STRIPE_W  = 0.15;
const CX        = 0.38;   // content left
const CW        = 9.32;   // content width
const SLIDE_H   = 5.625;
const FOOTER_Y  = 5.18;
const ERD_PATH  = path.join(__dirname, 'lernmaterialverwaltung.png');

function stripe(slide, dark) {
  slide.background = { color: dark ? C.black : C.white };
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: STRIPE_W, h: SLIDE_H,
    fill: { color: C.red }, line: { color: C.red, width: 0 }
  });
}

function slideNum(slide, num, dark) {
  slide.addText(String(num).padStart(2, '0') + ' / 12', {
    x: 8.5, y: 0.1, w: 1.35, h: 0.28,
    fontSize: 10, fontFace: 'Calibri',
    color: dark ? '444444' : 'AAAAAA',
    align: 'right', margin: 0
  });
}

function titleBar(slide, title, dark) {
  slide.addText(title, {
    x: CX, y: 0.17, w: CW - 1.1, h: 0.55,
    fontSize: 28, fontFace: 'Calibri', bold: true,
    color: dark ? C.white : C.black, margin: 0
  });
  slide.addShape(pres.shapes.LINE, {
    x: CX, y: 0.8, w: CW, h: 0,
    line: { color: dark ? '333333' : C.grayLight, width: 1 }
  });
}

function chrome(slide, num, title, dark = false) {
  stripe(slide, dark);
  slideNum(slide, num, dark);
  if (title) titleBar(slide, title, dark);
}

function footer(slide, num, dark = false, rightText = null) {
  slide.addText('Auric Ergeson · Lernmaterialverwaltung · LF8', {
    x: CX, y: FOOTER_Y, w: 5.5, h: 0.28,
    fontSize: 10, fontFace: 'Calibri',
    color: dark ? '444444' : C.grayMid, margin: 0
  });
  slide.addText(rightText || (String(num).padStart(2, '0') + ' / 12'), {
    x: 7.5, y: FOOTER_Y, w: 2.2, h: 0.28,
    fontSize: 10, fontFace: 'Calibri',
    color: dark ? '444444' : C.grayMid,
    align: 'right', margin: 0
  });
}

// ─── SLIDE 01 — TITLE ────────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  stripe(s, true);
  slideNum(s, 1, true);

  s.addText('LF8-Abschlussprojekt  ·  Daten systemübergreifend bereitstellen', {
    x: CX, y: 0.1, w: CW, h: 0.28,
    fontSize: 11, fontFace: 'Calibri', color: '555555',
    charSpacing: 1, margin: 0
  });

  s.addText([
    { text: 'Lernmaterial', options: { breakLine: true } },
    { text: 'verwaltung',   options: { color: C.red } }
  ], {
    x: CX, y: 0.6, w: 5.8, h: 2.2,
    fontSize: 60, fontFace: 'Calibri', bold: true,
    color: C.white, margin: 0
  });

  s.addText('Zentrales Materialmanagementsystem\nauf Python & MySQL-Basis', {
    x: CX, y: 2.9, w: 5.2, h: 0.8,
    fontSize: 18, fontFace: 'Calibri', color: '888888', margin: 0
  });

  // Aside box (right column)
  const asideX = 6.6;
  const asideW = 3.0;
  s.addShape(pres.shapes.RECTANGLE, {
    x: asideX - 0.15, y: 0.55, w: asideW + 0.15, h: 3.6,
    fill: { color: '1A1A1A' }, line: { color: '222222', width: 1 }
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: asideX - 0.15, y: 0.55, w: 0.06, h: 3.6,
    fill: { color: C.red }, line: { color: C.red, width: 0 }
  });

  const items = [
    ['Lernfeld',       'LF 8'],
    ['Zeitraum',       'Apr – Mai 2026'],
    ['Gesamtaufwand',  '43 Stunden'],
    ['Stack',          'Python · SQLAlchemy · MySQL'],
  ];
  items.forEach(([label, val], i) => {
    const y = 0.72 + i * 0.86;
    s.addText(label.toUpperCase(), {
      x: asideX, y, w: asideW, h: 0.22,
      fontSize: 9, fontFace: 'Calibri', color: '666666',
      charSpacing: 2, margin: 0
    });
    s.addText(val, {
      x: asideX, y: y + 0.22, w: asideW, h: 0.36,
      fontSize: 15, fontFace: 'Calibri', bold: true, color: C.white, margin: 0
    });
  });

  // Footer
  s.addText('Auric Ergeson  ·  Azubi Anwendungsentwickler  ·  Mai 2026', {
    x: CX, y: FOOTER_Y, w: 6.5, h: 0.28,
    fontSize: 10, fontFace: 'Calibri', color: '444444', margin: 0
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: 8.3, y: FOOTER_Y - 0.01, w: 1.35, h: 0.3,
    fill: { color: C.red }, line: { color: C.red, width: 0 }
  });
  s.addText('Berufsschule', {
    x: 8.3, y: FOOTER_Y, w: 1.35, h: 0.28,
    fontSize: 10, fontFace: 'Calibri', bold: true,
    color: C.white, align: 'center', margin: 0
  });
}

// ─── SLIDE 02 — AGENDA ───────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  chrome(s, 2, 'Agenda');

  const items = [
    ['01', 'Ausgangssituation'],
    ['06', 'Systemarchitektur & Funktionen'],
    ['02', 'Aufgabenstellung & Zielsetzung'],
    ['07', 'Herausforderungen & Lösungen'],
    ['03', 'Projektplanung & Prozessschritte'],
    ['08', 'Soll-Ist-Vergleich'],
    ['04', 'Lösungskonzept & Entscheidungen'],
    ['09', 'Ergebnis'],
    ['05', 'Datenbankdesign'],
    ['10', 'Fazit & Reflexion'],
  ];

  const colW = CW / 2 - 0.1;
  items.forEach(([num, text], i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = CX + col * (colW + 0.2);
    const y = 1.0 + row * 0.82;

    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: colW, h: 0.62,
      fill: { color: C.grayUltra }, line: { color: C.grayLight, width: 1 }
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 0.06, h: 0.62,
      fill: { color: C.red }, line: { color: C.red, width: 0 }
    });
    s.addText(num, {
      x: x + 0.14, y: y + 0.1, w: 0.5, h: 0.42,
      fontSize: 14, fontFace: 'Calibri', bold: true, color: C.red, margin: 0
    });
    s.addText(text, {
      x: x + 0.62, y: y + 0.1, w: colW - 0.72, h: 0.42,
      fontSize: 14, fontFace: 'Calibri', bold: false, color: C.grayDark,
      valign: 'middle', margin: 0
    });
  });

  footer(s, 2);
}

// ─── SLIDE 03 — AUSGANGSSITUATION ────────────────────────────────────────────
{
  const s = pres.addSlide();
  chrome(s, 3, 'Ausgangssituation');

  // Quote
  s.addShape(pres.shapes.RECTANGLE, {
    x: CX, y: 0.95, w: CW, h: 0.78,
    fill: { color: C.redLight }, line: { color: 'F0C8C6', width: 1 }
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: CX, y: 0.95, w: 0.06, h: 0.78,
    fill: { color: C.red }, line: { color: C.red, width: 0 }
  });
  s.addText('„Unterrichtsmaterialien werden per E-Mail verteilt, auf verschiedenen Computern abgelegt — ohne zentrale Verwaltung, ohne Suche, ohne Versionierung."', {
    x: CX + 0.18, y: 0.95, w: CW - 0.25, h: 0.78,
    fontSize: 15, fontFace: 'Calibri', italic: true,
    color: C.grayDark, valign: 'middle', margin: 0
  });

  // 3 cards
  const cards = [
    ['Dezentrale Ablage',    'Jede Lehrkraft nutzt eine eigene Ordnerstruktur — kein einheitliches System.'],
    ['Keine Suchfunktion',   'Materialien sind schwer auffindbar. Nur wer den genauen Dateinamen kennt, findet die Datei.'],
    ['Versionschaos',        'Überarbeitungen werden nicht nachverfolgt — veraltete Versionen zirkulieren weiter.'],
  ];
  const cardW = CW / 3 - 0.12;
  cards.forEach(([title, text], i) => {
    const x = CX + i * (cardW + 0.17);
    const y = 1.9;
    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: cardW, h: 2.8,
      fill: { color: C.white }, line: { color: C.grayLight, width: 1 },
      shadow: { type: 'outer', blur: 8, offset: 2, angle: 135, color: '000000', opacity: 0.08 }
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: cardW, h: 0.06,
      fill: { color: C.red }, line: { color: C.red, width: 0 }
    });
    s.addText(title, {
      x: x + 0.18, y: y + 0.15, w: cardW - 0.28, h: 0.45,
      fontSize: 16, fontFace: 'Calibri', bold: true, color: C.black, margin: 0
    });
    s.addText(text, {
      x: x + 0.18, y: y + 0.68, w: cardW - 0.28, h: 1.9,
      fontSize: 13, fontFace: 'Calibri', color: C.grayDark,
      wrap: true, margin: 0
    });
  });

  footer(s, 3);
}

// ─── SLIDE 04 — AUFGABENSTELLUNG & ZIELSETZUNG ───────────────────────────────
{
  const s = pres.addSlide();
  chrome(s, 4, 'Aufgabenstellung & Zielsetzung');

  const colW = CW / 2 - 0.15;
  const leftX = CX;
  const rightX = CX + colW + 0.3;
  const startY = 0.95;

  // Left col header
  s.addText('FUNKTIONALE ZIELE', {
    x: leftX, y: startY, w: colW, h: 0.3,
    fontSize: 10, fontFace: 'Calibri', bold: true, color: C.red,
    charSpacing: 2, margin: 0
  });

  const goals = [
    'Materialien hochladen, herunterladen & durchsuchen',
    'Kommentarfunktion für Lehrkräfte & Azubis',
    'Benutzerverwaltung mit Rollen (Lehrer, Azubi, Admin)',
    '7 SQL-Abfragen mit Aggregation, JOINs & Filtern',
    'Strukturierte CLI-Ausgabe mit rich-Bibliothek',
  ];
  goals.forEach((g, i) => {
    const y = startY + 0.38 + i * 0.68;
    s.addShape(pres.shapes.RECTANGLE, {
      x: leftX, y, w: 0.35, h: 0.44,
      fill: { color: 'E8F5E9' }, line: { color: 'C8E6C9', width: 1 }
    });
    s.addText('✓', {
      x: leftX, y, w: 0.35, h: 0.44,
      fontSize: 16, fontFace: 'Calibri', bold: true,
      color: '2E7D32', align: 'center', valign: 'middle', margin: 0
    });
    s.addText(g, {
      x: leftX + 0.42, y: y + 0.02, w: colW - 0.42, h: 0.44,
      fontSize: 13, fontFace: 'Calibri', color: C.grayDark,
      valign: 'middle', margin: 0
    });
  });

  // Right col header
  s.addText('NICHT IM SCOPE', {
    x: rightX, y: startY, w: colW, h: 0.3,
    fontSize: 10, fontFace: 'Calibri', bold: true, color: C.grayMid,
    charSpacing: 2, margin: 0
  });

  s.addShape(pres.shapes.RECTANGLE, {
    x: rightX, y: startY + 0.38, w: colW, h: 2.98,
    fill: { color: C.grayUltra }, line: { color: C.grayLight, width: 1 }
  });
  s.addText('Bewusst ausgegrenzt', {
    x: rightX + 0.18, y: startY + 0.52, w: colW - 0.28, h: 0.3,
    fontSize: 12, fontFace: 'Calibri', bold: true, color: C.grayMid, margin: 0
  });

  const excluded = [
    'Web-Oberfläche — außerhalb des LF8-Rahmens',
    'Echtzeitsynchronisation zwischen Clients',
    'Automatische Datensicherung / Backup-System',
  ];
  excluded.forEach((e, i) => {
    const y = startY + 0.92 + i * 0.72;
    s.addText('×', {
      x: rightX + 0.15, y, w: 0.3, h: 0.5,
      fontSize: 18, fontFace: 'Calibri', bold: true,
      color: C.red, align: 'center', valign: 'middle', margin: 0
    });
    s.addText(e, {
      x: rightX + 0.5, y: y + 0.04, w: colW - 0.6, h: 0.46,
      fontSize: 13, fontFace: 'Calibri', color: C.grayDark,
      valign: 'middle', margin: 0
    });
  });

  footer(s, 4);
}

// ─── SLIDE 05 — PROJEKTPLANUNG ───────────────────────────────────────────────
{
  const s = pres.addSlide();
  chrome(s, 5, 'Projektplanung');

  const phases = [
    ['Phase 01', 'Analyse &\nPlanung',    '4 h'],
    ['Phase 02', 'Datenbank-\ndesign',    '6 h'],
    ['Phase 03', 'Implementierung',       '15 h'],
    ['Phase 04', 'Test &\nDebugging',     '4 h'],
    ['Phase 05', 'Dokumentation',         '6 h'],
  ];

  const boxW  = 1.55;
  const arrow = 0.22;
  const total = phases.length * boxW + (phases.length - 1) * arrow;
  const startX = CX + (CW - total) / 2;
  const boxY   = 0.95;
  const boxH   = 1.3;

  phases.forEach(([num, name, hours], i) => {
    const x = startX + i * (boxW + arrow);
    const highlight = i === 1; // DB-design phase gets red accent
    s.addShape(pres.shapes.RECTANGLE, {
      x, y: boxY, w: boxW, h: boxH,
      fill: { color: highlight ? C.redLight : C.grayUltra },
      line: { color: highlight ? C.red : C.grayLight, width: highlight ? 2 : 1 }
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x, y: boxY, w: boxW, h: 0.06,
      fill: { color: highlight ? C.red : C.grayLight },
      line: { color: highlight ? C.red : C.grayLight, width: 0 }
    });
    s.addText(num, {
      x: x + 0.08, y: boxY + 0.1, w: boxW - 0.16, h: 0.26,
      fontSize: 9, fontFace: 'Calibri', bold: true,
      color: highlight ? C.red : C.grayMid,
      charSpacing: 1, margin: 0
    });
    s.addText(name, {
      x: x + 0.08, y: boxY + 0.38, w: boxW - 0.16, h: 0.58,
      fontSize: 13, fontFace: 'Calibri', bold: true,
      color: C.black, margin: 0
    });
    s.addText(hours + ' (geplant)', {
      x: x + 0.08, y: boxY + 0.96, w: boxW - 0.16, h: 0.26,
      fontSize: 10, fontFace: 'Calibri', color: C.grayMid, margin: 0
    });
    // Arrow
    if (i < phases.length - 1) {
      s.addText('→', {
        x: x + boxW, y: boxY + 0.42, w: arrow, h: 0.46,
        fontSize: 16, fontFace: 'Calibri', color: C.grayMid,
        align: 'center', valign: 'middle', margin: 0
      });
    }
  });

  // DB-first rationale
  const rY = 2.45;
  s.addShape(pres.shapes.RECTANGLE, {
    x: CX, y: rY, w: CW, h: 0.58,
    fill: { color: C.grayUltra }, line: { color: C.grayLight, width: 1 }
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: CX, y: rY, w: 0.06, h: 0.58,
    fill: { color: C.red }, line: { color: C.red, width: 0 }
  });
  s.addText([
    { text: 'Warum DB-first?  ', options: { bold: true, color: C.black } },
    { text: 'Datenbankdesign vor Implementierung abgeschlossen — Schema-first verhindert späteren Refactoring-Aufwand.', options: { color: C.grayDark } }
  ], {
    x: CX + 0.18, y: rY, w: CW - 0.25, h: 0.58,
    fontSize: 14, fontFace: 'Calibri', valign: 'middle', margin: 0
  });

  // Info boxes
  const infoBoxes = [
    ['PROJEKTSTART',   '06. April 2026'],
    ['ABGABE',         '30. Mai 2026'],
    ['GESAMTPLANUNG',  '35 Stunden'],
  ];
  const ibW = CW / 3 - 0.12;
  infoBoxes.forEach(([label, val], i) => {
    const x = CX + i * (ibW + 0.17);
    const y = 3.2;
    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: ibW, h: 0.9,
      fill: { color: C.grayUltra }, line: { color: C.grayLight, width: 1 }
    });
    s.addText(label, {
      x: x + 0.12, y: y + 0.1, w: ibW - 0.2, h: 0.25,
      fontSize: 9, fontFace: 'Calibri', color: C.grayMid, charSpacing: 1, margin: 0
    });
    s.addText(val, {
      x: x + 0.12, y: y + 0.38, w: ibW - 0.2, h: 0.4,
      fontSize: 16, fontFace: 'Calibri', bold: true,
      color: i === 2 ? C.red : C.black, margin: 0
    });
  });

  footer(s, 5);
}

// ─── SLIDE 06 — LÖSUNGSKONZEPT ───────────────────────────────────────────────
{
  const s = pres.addSlide();
  chrome(s, 6, 'Lösungskonzept & Entscheidungen');

  const tableData = [
    [
      { text: 'Ansatz',               options: { bold: true, color: C.white, fill: { color: C.black } } },
      { text: 'Versionierung',        options: { bold: true, color: C.white, fill: { color: C.black } } },
      { text: 'Suchfunktion',         options: { bold: true, color: C.white, fill: { color: C.black } } },
      { text: 'DB-Anbindung',         options: { bold: true, color: C.white, fill: { color: C.black } } },
      { text: 'Zeitaufwand',          options: { bold: true, color: C.white, fill: { color: C.black } } },
    ],
    ['Freigegebener Ordner', '✗', '✗', '✗', 'Gering'],
    ['Excel-Tabelle',        '✗', '~', '✗', 'Mittel'],
    ['Web-Anwendung',        '✓', '✓', '✓', 'Sehr hoch — außerhalb LF8'],
    [
      { text: 'CLI + Python + MySQL  ★', options: { bold: true, fill: { color: C.redLight }, color: C.black } },
      { text: '✓', options: { bold: true, fill: { color: C.redLight }, color: '2E7D32' } },
      { text: '✓', options: { bold: true, fill: { color: C.redLight }, color: '2E7D32' } },
      { text: '✓', options: { bold: true, fill: { color: C.redLight }, color: '2E7D32' } },
      { text: 'Mittel — LF8-konform', options: { bold: true, fill: { color: C.redLight }, color: C.black } },
    ],
  ];

  s.addTable(tableData, {
    x: CX, y: 0.95, w: CW, h: 2.5,
    fontFace: 'Calibri', fontSize: 13,
    colW: [2.8, 1.6, 1.6, 1.6, 1.72],
    border: { pt: 1, color: C.grayLight },
    align: 'center',
  });

  // Decision box
  s.addShape(pres.shapes.RECTANGLE, {
    x: CX, y: 3.65, w: CW, h: 0.85,
    fill: { color: C.grayUltra }, line: { color: C.grayLight, width: 1 }
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: CX, y: 3.65, w: 0.06, h: 0.85,
    fill: { color: C.red }, line: { color: C.red, width: 0 }
  });
  s.addText([
    { text: 'Entscheidung:  ', options: { bold: true, color: C.black } },
    { text: 'CLI-Anwendung mit Python, SQLAlchemy & MySQL — Datenbanklogik-fokussiert, LF8-konform, im Zeitrahmen umsetzbar.', options: { color: C.grayDark } }
  ], {
    x: CX + 0.18, y: 3.65, w: CW - 0.25, h: 0.85,
    fontSize: 15, fontFace: 'Calibri', valign: 'middle', margin: 0
  });

  footer(s, 6);
}

// ─── SLIDE 07 — DATENBANKDESIGN ───────────────────────────────────────────────
{
  const s = pres.addSlide();
  chrome(s, 7, 'Datenbankdesign');

  const decisions = [
    ['8 Tabellen in 3. Normalform',
     'benutzer · themengebiet · kategorie · tag · material · kommentar · material_tag · version'],
    ['Tags in eigener Tabelle (1NF)',
     'Statt kommaseparierter Werte — korrekte Normalisierung verhindert Anomalien.',
     'material_tag (N:M-Beziehung)'],
    ['Dualer Dateispeicher',
     'Dateien < 1 MB → LONGBLOB in DB\nDateien ≥ 1 MB → Dateisystem (app/uploads/)',
     'is_in_database (BOOLEAN Flag)'],
    ['Trigger für Versionierung',
     'MySQL-Trigger erstellt bei jeder Änderung automatisch einen Eintrag in der version-Tabelle.'],
  ];

  const leftW = 3.8;
  const rightX = CX + leftW + 0.25;
  const rightW = CW - leftW - 0.25;

  decisions.forEach(([title, text, code], i) => {
    const y = 0.95 + i * 1.02;
    const h = code ? 0.92 : 0.78;
    s.addShape(pres.shapes.RECTANGLE, {
      x: CX, y, w: leftW, h,
      fill: { color: C.grayUltra }, line: { color: C.grayLight, width: 1 }
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x: CX, y, w: 0.06, h,
      fill: { color: C.red }, line: { color: C.red, width: 0 }
    });
    s.addText(title, {
      x: CX + 0.14, y: y + 0.05, w: leftW - 0.2, h: 0.28,
      fontSize: 12, fontFace: 'Calibri', bold: true, color: C.black, margin: 0
    });
    s.addText(text, {
      x: CX + 0.14, y: y + 0.34, w: leftW - 0.2, h: 0.36,
      fontSize: 11, fontFace: 'Calibri', color: C.grayDark, margin: 0
    });
    if (code) {
      s.addText(code, {
        x: CX + 0.14, y: y + 0.7, w: leftW - 0.2, h: 0.22,
        fontSize: 10, fontFace: 'Courier New', color: C.red, margin: 0
      });
    }
  });

  // ERD image
  s.addImage({
    path: ERD_PATH,
    x: rightX, y: 0.95, w: rightW, h: 3.95,
    sizing: { type: 'contain', w: rightW, h: 3.95 }
  });
  s.addText('ERD · Erstellt mit DBeaver', {
    x: rightX, y: 4.98, w: rightW, h: 0.22,
    fontSize: 10, fontFace: 'Calibri', color: C.grayMid, align: 'center', margin: 0
  });

  footer(s, 7);
}

// ─── SLIDE 08 — SYSTEMARCHITEKTUR & FUNKTIONEN ───────────────────────────────
{
  const s = pres.addSlide();
  chrome(s, 8, 'Systemarchitektur & Funktionen');

  const leftW = 4.4;
  const rightX = CX + leftW + 0.3;
  const rightW = CW - leftW - 0.3;

  // 3-layer architecture
  const layers = [
    ['main.py',      'CLI-Oberfläche & Benutzerinteraktion', 'rich 15.0',          'E3F2FD', '1565C0'],
    ['services.py',  'Geschäftslogik, CRUD, SQL-Abfragen',   'SQLAlchemy 2.0',      'F3E5F5', '6A1B9A'],
    ['database.py',  'Verbindungsmanagement & ORM',          'PyMySQL · MySQL 8',   'E8F5E9', '2E7D32'],
  ];
  layers.forEach(([name, desc, tech, bg, accent], i) => {
    const y = 0.95 + i * 1.02;
    s.addShape(pres.shapes.RECTANGLE, {
      x: CX, y, w: leftW, h: 0.78,
      fill: { color: bg }, line: { color: C.grayLight, width: 1 }
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x: CX, y, w: 0.06, h: 0.78,
      fill: { color: accent }, line: { color: accent, width: 0 }
    });
    s.addText(name, {
      x: CX + 0.14, y: y + 0.06, w: 2.0, h: 0.3,
      fontSize: 14, fontFace: 'Courier New', bold: true, color: C.black, margin: 0
    });
    s.addText(desc, {
      x: CX + 0.14, y: y + 0.38, w: leftW - 0.24, h: 0.28,
      fontSize: 11, fontFace: 'Calibri', color: C.grayDark, margin: 0
    });
    s.addText(tech, {
      x: CX + leftW - 1.4, y: y + 0.06, w: 1.3, h: 0.28,
      fontSize: 10, fontFace: 'Calibri', bold: true,
      color: accent, align: 'right', margin: 0
    });
    // Arrow
    if (i < 2) {
      s.addText('↓', {
        x: CX + leftW / 2 - 0.2, y: y + 0.78, w: 0.4, h: 0.24,
        fontSize: 14, fontFace: 'Calibri', color: C.grayMid,
        align: 'center', margin: 0
      });
    }
  });

  // SQL queries box
  s.addShape(pres.shapes.RECTANGLE, {
    x: CX, y: 4.0, w: leftW, h: 0.7,
    fill: { color: C.grayUltra }, line: { color: C.grayLight, width: 1 }
  });
  s.addText('7 SQL-ABFRAGEN', {
    x: CX + 0.12, y: 4.04, w: leftW - 0.2, h: 0.22,
    fontSize: 9, fontFace: 'Calibri', bold: true, color: C.grayMid, charSpacing: 1, margin: 0
  });
  s.addText('COUNT · AVG · INNER JOIN · Multi-JOIN · JOIN+COUNT · Volltextsuche mit WHERE', {
    x: CX + 0.12, y: 4.28, w: leftW - 0.2, h: 0.36,
    fontSize: 12, fontFace: 'Calibri', color: C.grayDark, margin: 0
  });

  // 8 Functions grid (right)
  s.addText('8 FUNKTIONEN', {
    x: rightX, y: 0.95, w: rightW, h: 0.28,
    fontSize: 9, fontFace: 'Calibri', bold: true, color: C.grayMid, charSpacing: 1, margin: 0
  });
  const fns = [
    '01  Material hochladen',
    '02  Material herunterladen',
    '03  Suche & Filter',
    '04  Material löschen',
    '05  Kommentare verwalten',
    '06  Listen & Übersichten',
    '07  SQL-Abfragen ausführen',
    '08  Einträge erstellen',
  ];
  const fnW = rightW / 2 - 0.08;
  fns.forEach((fn, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = rightX + col * (fnW + 0.16);
    const y = 1.3 + row * 0.82;
    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: fnW, h: 0.58,
      fill: { color: C.grayUltra }, line: { color: C.grayLight, width: 1 }
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 0.05, h: 0.58,
      fill: { color: C.red }, line: { color: C.red, width: 0 }
    });
    s.addText(fn, {
      x: x + 0.12, y: y + 0.04, w: fnW - 0.18, h: 0.5,
      fontSize: 12, fontFace: 'Calibri', color: C.grayDark,
      valign: 'middle', margin: 0
    });
  });

  footer(s, 8);
}

// ─── SLIDE 09 — HERAUSFORDERUNGEN & LÖSUNGEN ─────────────────────────────────
{
  const s = pres.addSlide();
  chrome(s, 9, 'Herausforderungen & Lösungen');

  const challenges = [
    {
      num:   'Herausforderung 01',
      title: 'SQLAlchemy Automap',
      prob:  'automap_base() erkannte Fremdschlüsselbeziehungen nicht korrekt — führte zu Laufzeitfehlern bei JOINs.',
      sol:   'Manuelle Definition mit relationship() und expliziten foreign_keys=[]-Parametern. Dokumentation vertieft studiert.',
      probCode: 'automap_base()',
      solCode:  'relationship()  |  foreign_keys=[]',
    },
    {
      num:   'Herausforderung 02',
      title: 'Datei-Upload Kodierung',
      prob:  'Beim Einlesen von Binärdateien (PDF, DOCX) trat UnicodeDecodeError auf — Dateien wurden im Textmodus geöffnet.',
      sol:   'Konsequenter Wechsel zum Binärmodus für alle Dateioperationen (Upload & Download).',
      probCode: 'open(path, "r")  →  Fehler',
      solCode:  'open(path, "rb")  →  Korrekt',
    },
  ];

  const cardW = CW / 2 - 0.15;
  challenges.forEach((ch, i) => {
    const x = CX + i * (cardW + 0.3);
    const y = 0.95;
    const cardH = 4.0;

    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: cardW, h: cardH,
      fill: { color: C.white }, line: { color: C.grayLight, width: 1 },
      shadow: { type: 'outer', blur: 8, offset: 2, angle: 135, color: '000000', opacity: 0.08 }
    });
    // Header
    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: cardW, h: 0.78,
      fill: { color: C.black }, line: { color: C.black, width: 0 }
    });
    s.addText(ch.num, {
      x: x + 0.15, y: y + 0.06, w: cardW - 0.2, h: 0.26,
      fontSize: 10, fontFace: 'Calibri', color: C.red, bold: true, charSpacing: 1, margin: 0
    });
    s.addText(ch.title, {
      x: x + 0.15, y: y + 0.34, w: cardW - 0.2, h: 0.36,
      fontSize: 16, fontFace: 'Calibri', bold: true, color: C.white, margin: 0
    });

    // Problem section
    s.addShape(pres.shapes.RECTANGLE, {
      x: x + 0.15, y: y + 0.9, w: 0.72, h: 0.24,
      fill: { color: C.red }, line: { color: C.red, width: 0 }
    });
    s.addText('PROBLEM', {
      x: x + 0.15, y: y + 0.9, w: 0.72, h: 0.24,
      fontSize: 9, fontFace: 'Calibri', bold: true, color: C.white,
      align: 'center', valign: 'middle', margin: 0
    });
    s.addText(ch.prob, {
      x: x + 0.15, y: y + 1.18, w: cardW - 0.28, h: 0.72,
      fontSize: 12, fontFace: 'Calibri', color: C.grayDark, margin: 0
    });
    s.addText(ch.probCode, {
      x: x + 0.15, y: y + 1.92, w: cardW - 0.28, h: 0.3,
      fontSize: 11, fontFace: 'Courier New', color: C.red,
      fill: { color: C.redLight }, margin: 4
    });

    // Solution section
    s.addShape(pres.shapes.RECTANGLE, {
      x: x + 0.15, y: y + 2.35, w: 0.72, h: 0.24,
      fill: { color: '2E7D32' }, line: { color: '2E7D32', width: 0 }
    });
    s.addText('LÖSUNG', {
      x: x + 0.15, y: y + 2.35, w: 0.72, h: 0.24,
      fontSize: 9, fontFace: 'Calibri', bold: true, color: C.white,
      align: 'center', valign: 'middle', margin: 0
    });
    s.addText(ch.sol, {
      x: x + 0.15, y: y + 2.63, w: cardW - 0.28, h: 0.72,
      fontSize: 12, fontFace: 'Calibri', color: C.grayDark, margin: 0
    });
    s.addText(ch.solCode, {
      x: x + 0.15, y: y + 3.38, w: cardW - 0.28, h: 0.3,
      fontSize: 11, fontFace: 'Courier New', color: '2E7D32',
      fill: { color: 'E8F5E9' }, margin: 4
    });
  });

  footer(s, 9);
}

// ─── SLIDE 10 — SOLL-IST-VERGLEICH ───────────────────────────────────────────
{
  const s = pres.addSlide();
  chrome(s, 10, 'Soll-Ist-Vergleich');

  const tableData = [
    [
      { text: 'Phase',              options: { bold: true, color: C.white, fill: { color: C.black } } },
      { text: 'Soll',               options: { bold: true, color: C.white, fill: { color: C.black } } },
      { text: 'Ist',                options: { bold: true, color: C.white, fill: { color: C.black } } },
      { text: 'Δ',                  options: { bold: true, color: C.white, fill: { color: C.black } } },
    ],
    ['Analyse & Planung',   '4 h',  '5 h',  '+1 h'],
    ['Datenbankdesign',     '6 h',  '8 h',  '+2 h'],
    ['Implementierung',     '15 h', '18 h', '+3 h'],
    ['Test & Debugging',    '4 h',  '5 h',  '+1 h'],
    ['Dokumentation',       '6 h',  '7 h',  '+1 h'],
    [
      { text: 'Gesamt', options: { bold: true, fill: { color: C.grayUltra } } },
      { text: '35 h',   options: { bold: true, fill: { color: C.grayUltra } } },
      { text: '43 h',   options: { bold: true, color: C.red, fill: { color: C.grayUltra } } },
      { text: '+8 h',   options: { bold: true, color: C.red, fill: { color: C.grayUltra } } },
    ],
  ];

  s.addTable(tableData, {
    x: CX, y: 0.95, w: 4.5, h: 3.95,
    fontFace: 'Calibri', fontSize: 13,
    colW: [2.1, 0.8, 0.8, 0.8],
    border: { pt: 1, color: C.grayLight },
    align: 'center',
  });

  // Right side
  const rx = CX + 4.7;
  const rw = CW - 4.7;

  s.addText('Zeitplanung', {
    x: rx, y: 0.95, w: rw, h: 0.3,
    fontSize: 11, fontFace: 'Calibri', bold: true,
    color: C.grayMid, charSpacing: 1, margin: 0
  });
  s.addText([
    { text: '35', options: { color: C.grayMid } },
    { text: ' → ', options: { color: C.grayLight } },
    { text: '43', options: { color: C.red } },
  ], {
    x: rx, y: 1.28, w: rw, h: 1.1,
    fontSize: 72, fontFace: 'Calibri', bold: true, margin: 0
  });
  s.addText('Stunden', {
    x: rx, y: 2.45, w: rw, h: 0.36,
    fontSize: 18, fontFace: 'Calibri', color: C.grayMid, margin: 0
  });

  // +23% badge
  s.addShape(pres.shapes.RECTANGLE, {
    x: rx, y: 2.9, w: 1.5, h: 0.6,
    fill: { color: C.red }, line: { color: C.red, width: 0 }
  });
  s.addText('+23 %', {
    x: rx, y: 2.9, w: 1.5, h: 0.6,
    fontSize: 22, fontFace: 'Calibri', bold: true, color: C.white,
    align: 'center', valign: 'middle', margin: 0
  });
  s.addText('Mehraufwand', {
    x: rx + 1.6, y: 2.9, w: rw - 1.6, h: 0.6,
    fontSize: 13, fontFace: 'Calibri', color: C.grayMid, valign: 'middle', margin: 0
  });

  // Why box
  s.addShape(pres.shapes.RECTANGLE, {
    x: rx, y: 3.65, w: rw, h: 1.1,
    fill: { color: C.grayUltra }, line: { color: C.grayLight, width: 1 }
  });
  s.addShape(pres.shapes.RECTANGLE, {
    x: rx, y: 3.65, w: 0.06, h: 1.1,
    fill: { color: C.red }, line: { color: C.red, width: 0 }
  });
  s.addText('HAUPTURSACHEN', {
    x: rx + 0.14, y: 3.7, w: rw - 0.2, h: 0.26,
    fontSize: 9, fontFace: 'Calibri', bold: true, color: C.grayMid, charSpacing: 1, margin: 0
  });
  s.addText('SQLAlchemy-Lernkurve (automap, relationships) & erhöhter Debugging-Aufwand beim Datei-Upload haben die Implementierungsphase um 3 Stunden verlängert.', {
    x: rx + 0.14, y: 4.0, w: rw - 0.2, h: 0.7,
    fontSize: 12, fontFace: 'Calibri', color: C.grayDark, margin: 0
  });

  footer(s, 10);
}

// ─── SLIDE 11 — ERGEBNIS ─────────────────────────────────────────────────────
{
  const s = pres.addSlide();
  chrome(s, 11, 'Ergebnis');

  const metrics = [
    ['8',  'Funktionen\nimplementiert',    'Upload · Download · Suche · Löschen\nKommentare · Listen · SQL · Erstellen'],
    ['7',  'SQL-\nAbfragetypen',           'COUNT · AVG · INNER JOIN\nMulti-JOIN · JOIN+COUNT · Volltextsuche'],
    ['8',  'Datenbank-\ntabellen',         '3. Normalform · Trigger\nN:M-Beziehungen · Dual-Storage'],
  ];

  const mW = CW / 3 - 0.12;
  metrics.forEach(([num, label, sub], i) => {
    const x = CX + i * (mW + 0.17);
    const y = 0.95;
    const mH = 2.0;
    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: mW, h: mH,
      fill: { color: C.grayUltra }, line: { color: C.grayLight, width: 1 }
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: mW, h: 0.06,
      fill: { color: C.red }, line: { color: C.red, width: 0 }
    });
    s.addText(num, {
      x: x + 0.1, y: y + 0.1, w: mW - 0.2, h: 0.88,
      fontSize: 64, fontFace: 'Calibri', bold: true, color: C.red,
      align: 'center', margin: 0
    });
    s.addText(label, {
      x: x + 0.1, y: y + 1.0, w: mW - 0.2, h: 0.44,
      fontSize: 13, fontFace: 'Calibri', bold: true, color: C.black,
      align: 'center', margin: 0
    });
    s.addText(sub, {
      x: x + 0.05, y: y + 1.5, w: mW - 0.1, h: 0.44,
      fontSize: 10, fontFace: 'Calibri', color: C.grayMid,
      align: 'center', margin: 0
    });
  });

  // Terminal mockup
  const ty = 3.1;
  const th = 1.9;
  s.addShape(pres.shapes.RECTANGLE, {
    x: CX, y: ty, w: CW, h: th,
    fill: { color: '0D1117' }, line: { color: '30363D', width: 1 }
  });
  // Traffic lights
  [['FF5F56', 0], ['FFBD2E', 0.28], ['27C93F', 0.56]].forEach(([col, dx]) => {
    s.addShape(pres.shapes.OVAL, {
      x: CX + 0.15 + dx, y: ty + 0.12, w: 0.18, h: 0.18,
      fill: { color: col }, line: { color: col, width: 0 }
    });
  });
  s.addText('python app/main.py  —  Lernmaterialverwaltung', {
    x: CX + 1.1, y: ty + 0.1, w: CW - 1.2, h: 0.25,
    fontSize: 11, fontFace: 'Courier New', color: '8B949E', margin: 0
  });
  s.addShape(pres.shapes.LINE, {
    x: CX, y: ty + 0.42, w: CW, h: 0,
    line: { color: '30363D', width: 1 }
  });
  const termLines = [
    '┌────┬────────────────────────────┬──────────────────┬────────────┬───────────┐',
    '│ ID │ Titel                       │ Fach             │ Kategorie  │ Größe     │',
    '├────┼────────────────────────────┼──────────────────┼────────────┼───────────┤',
    '│  1 │ Python Grundlagen           │ Programmierung   │ Skript     │ 285 KB    │',
    '│  2 │ SQL-Abfragen erklärt        │ Datenbanken      │ Übung      │ 1.2 MB    │',
    '│  3 │ Netzwerkprotokolle OSI      │ Netzwerke        │ Folie      │ 450 KB    │',
    '└────┴────────────────────────────┴──────────────────┴────────────┴───────────┘',
    '▶  3 Materialien gefunden  ·  Datenbankverbindung aktiv  ·  MySQL 8.0',
  ];
  termLines.forEach((line, i) => {
    const isPrompt = i === termLines.length - 1;
    s.addText(line, {
      x: CX + 0.1, y: ty + 0.5 + i * 0.175, w: CW - 0.15, h: 0.18,
      fontSize: 10, fontFace: 'Courier New',
      color: isPrompt ? 'E6EDF3' : '58A6FF',
      margin: 0
    });
  });

  footer(s, 11);
}

// ─── SLIDE 12 — FAZIT & REFLEXION (dark) ─────────────────────────────────────
{
  const s = pres.addSlide();
  chrome(s, 12, 'Fazit & Reflexion', true);

  const colW = CW / 2 - 0.15;
  const startY = 0.95;

  // Left col
  s.addText('WAS HAT FUNKTIONIERT', {
    x: CX, y: startY, w: colW, h: 0.28,
    fontSize: 9, fontFace: 'Calibri', bold: true, color: C.red,
    charSpacing: 2, margin: 0
  });
  const worked = [
    ['DB-first Ansatz',           'Klares Schema vor Implementierung hat Refactoring verhindert.'],
    ['Drei-Schichten-Architektur','Saubere Trennung macht Änderungen lokal und beherrschbar.'],
    ['rich-Bibliothek',           'Professionelle CLI-Ausgabe ohne großen Aufwand.'],
  ];
  worked.forEach(([title, text], i) => {
    const y = startY + 0.38 + i * 1.1;
    s.addShape(pres.shapes.RECTANGLE, {
      x: CX, y, w: 0.38, h: 0.44,
      fill: { color: '1A3A1A' }, line: { color: '2E7D32', width: 1 }
    });
    s.addText('✓', {
      x: CX, y, w: 0.38, h: 0.44,
      fontSize: 18, fontFace: 'Calibri', bold: true,
      color: '27C93F', align: 'center', valign: 'middle', margin: 0
    });
    s.addText(title, {
      x: CX + 0.46, y: y, w: colW - 0.46, h: 0.3,
      fontSize: 14, fontFace: 'Calibri', bold: true, color: C.white, margin: 0
    });
    s.addText(text, {
      x: CX + 0.46, y: y + 0.32, w: colW - 0.46, h: 0.38,
      fontSize: 12, fontFace: 'Calibri', color: '888888', margin: 0
    });
  });

  // Right col
  const rx = CX + colW + 0.3;
  s.addText('WAS ICH ÄNDERN WÜRDE', {
    x: rx, y: startY, w: colW, h: 0.28,
    fontSize: 9, fontFace: 'Calibri', bold: true, color: C.grayMid,
    charSpacing: 2, margin: 0
  });
  const change = [
    ['SQLAlchemy-Docs früher lesen', 'Hätte 3 Stunden Debugging gespart.'],
    ['Zeitpuffer einplanen',          'Unbekannte Technologien direkt in Planung einkalkulieren.'],
    ['Web-Oberfläche ergänzen',       'Bessere Zugänglichkeit ohne CLI — nächster Schritt.'],
  ];
  change.forEach(([title, text], i) => {
    const y = startY + 0.38 + i * 1.1;
    s.addShape(pres.shapes.RECTANGLE, {
      x: rx, y, w: 0.38, h: 0.44,
      fill: { color: '1A1A2E' }, line: { color: '555599', width: 1 }
    });
    s.addText('→', {
      x: rx, y, w: 0.38, h: 0.44,
      fontSize: 18, fontFace: 'Calibri', bold: true,
      color: C.grayMid, align: 'center', valign: 'middle', margin: 0
    });
    s.addText(title, {
      x: rx + 0.46, y, w: colW - 0.46, h: 0.3,
      fontSize: 14, fontFace: 'Calibri', bold: true, color: C.white, margin: 0
    });
    s.addText(text, {
      x: rx + 0.46, y: y + 0.32, w: colW - 0.46, h: 0.38,
      fontSize: 12, fontFace: 'Calibri', color: '888888', margin: 0
    });
  });

  // Closing quote
  s.addShape(pres.shapes.LINE, {
    x: CX, y: 4.62, w: CW, h: 0,
    line: { color: C.red, width: 2 }
  });
  s.addText('„Strukturierte Datenbankplanung reduziert den Implementierungsaufwand — Zeitplanung mit unbekannten Technologien muss realistischer sein."', {
    x: CX, y: 4.72, w: CW - 2.0, h: 0.6,
    fontSize: 13, fontFace: 'Calibri', italic: true, bold: true,
    color: '888888', margin: 0
  });
  s.addText('Vielen Dank — Fragen?', {
    x: 7.5, y: 4.72, w: 2.2, h: 0.6,
    fontSize: 13, fontFace: 'Calibri', bold: true, color: C.red,
    align: 'right', valign: 'middle', margin: 0
  });

  footer(s, 12, true);
}

// ─── SAVE ─────────────────────────────────────────────────────────────────────
pres.writeFile({ fileName: 'Praesentation.pptx' })
  .then(() => console.log('✓  Praesentation.pptx saved'))
  .catch(err => { console.error('✗  Error:', err); process.exit(1); });
