"""
Service-Schicht: Alle Datenbankoperationen für die Lernmaterialverwaltung.

Diese Datei enthält alle Funktionen, die direkt mit der Datenbank arbeiten:
  - CRUD-Operationen (Create, Read, Update, Delete) für alle Entitäten
  - Upload und Download von Dateien mit intelligenter Speicherstrategie
  - 7 Pflichtabfragen für das LF8-Abschlussprojekt (Aggregation, JOIN, Multi-JOIN)

Die Speicherstrategie für Dateien:
  - Dateien ≤ 1 MB → werden direkt in der Datenbank gespeichert (als BLOB)
  - Dateien > 1 MB → werden im Dateisystem gespeichert (Ordner: uploads/)
"""

from sqlalchemy.orm import Session   # Typ-Hinweis für Datenbank-Sitzungen
from sqlalchemy import func          # SQL-Funktionen wie COUNT, AVG, etc.
from database import *               # Alle Tabellenobjekte aus database.py importieren
import os                            # Für Datei- und Ordneroperationen
import time                          # Für eindeutige Dateinamen (Zeitstempel)


# ─────────────────────────────────────────────────────────────────────────────
# CRUD-Operationen für Benutzer
# CRUD = Create (Erstellen), Read (Lesen), Update (Ändern), Delete (Löschen)
# ─────────────────────────────────────────────────────────────────────────────

def get_all_users(db: Session):
    """
    Gibt alle Benutzer aus der Datenbank zurück.

    Args:
        db (Session): Aktive Datenbank-Sitzung

    Returns:
        list: Liste aller Benutzer-Objekte
    """
    users = db.query(benutzer).all()  # Alle Zeilen aus der Tabelle 'benutzer' holen
    return users


def get_user_by_id(db: Session, user_id: int):
    """
    Sucht einen einzelnen Benutzer anhand seiner ID.

    Args:
        db      (Session): Aktive Datenbank-Sitzung
        user_id (int):     Die ID des gesuchten Benutzers

    Returns:
        benutzer | None: Das Benutzer-Objekt oder None, wenn nicht gefunden
    """
    # filter() entspricht "WHERE id = user_id" in SQL
    # first() gibt den ersten Treffer zurück (oder None, wenn keiner gefunden)
    return db.query(benutzer).filter(benutzer.id == user_id).first()


def create_user(db: Session, username: str, email: str, rolle: str = "Azubi"):
    """
    Erstellt einen neuen Benutzer in der Datenbank.

    Args:
        db       (Session): Aktive Datenbank-Sitzung
        username (str):     Benutzername (muss eindeutig sein)
        email    (str):     E-Mail-Adresse (muss eindeutig sein)
        rolle    (str):     Benutzerrolle: "Lehrer", "Azubi" oder "Admin" (Standard: "Azubi")

    Returns:
        benutzer: Das neu erstellte Benutzer-Objekt mit gesetzter ID
    """
    user = benutzer(username=username, email=email, rolle=rolle)  # Neues Objekt erstellen
    db.add(user)      # Zur Datenbank-Sitzung hinzufügen (noch nicht gespeichert)
    db.commit()       # Änderungen dauerhaft in der Datenbank speichern
    db.refresh(user)  # Objekt mit den DB-Werten aktualisieren (z.B. die neue ID)
    return user


# ─────────────────────────────────────────────────────────────────────────────
# CRUD-Operationen für Themengebiete
# ─────────────────────────────────────────────────────────────────────────────

def get_all_themen(db: Session):
    """
    Gibt alle Themengebiete aus der Datenbank zurück.

    Args:
        db (Session): Aktive Datenbank-Sitzung

    Returns:
        list: Liste aller Themengebiet-Objekte
    """
    themen = db.query(themengebiet).all()  # Alle Zeilen aus der Tabelle 'themengebiet'
    return themen


def get_thema_by_id(db: Session, thema_id: int):
    """
    Sucht ein einzelnes Themengebiet anhand seiner ID.

    Args:
        db       (Session): Aktive Datenbank-Sitzung
        thema_id (int):     Die ID des gesuchten Themengebiets

    Returns:
        themengebiet | None: Das Themengebiet-Objekt oder None
    """
    return db.query(themengebiet).filter(themengebiet.id == thema_id).first()


def create_thema(db: Session, name: str, beschreibung: str = ""):
    """
    Erstellt ein neues Themengebiet in der Datenbank.

    Args:
        db           (Session): Aktive Datenbank-Sitzung
        name         (str):     Name des Themengebiets (muss eindeutig sein)
        beschreibung (str):     Optionale Beschreibung (Standard: leer)

    Returns:
        themengebiet: Das neu erstellte Themengebiet-Objekt mit gesetzter ID
    """
    thema = themengebiet(name=name, beschreibung=beschreibung)  # Neues Objekt erstellen
    db.add(thema)      # Zur Sitzung hinzufügen
    db.commit()        # In der Datenbank speichern
    db.refresh(thema)  # Objekt mit DB-Werten aktualisieren
    return thema


# ─────────────────────────────────────────────────────────────────────────────
# CRUD-Operationen für Kategorien
# ─────────────────────────────────────────────────────────────────────────────

def get_all_kategories(db: Session):
    """
    Gibt alle Kategorien aus der Datenbank zurück.

    Args:
        db (Session): Aktive Datenbank-Sitzung

    Returns:
        list: Liste aller Kategorie-Objekte
    """
    kategories = db.query(kategorie).all()  # Alle Zeilen aus der Tabelle 'kategorie'
    return kategories


def get_kategorie_by_id(db: Session, kategorie_id: int):
    """
    Sucht eine einzelne Kategorie anhand ihrer ID.

    Args:
        db           (Session): Aktive Datenbank-Sitzung
        kategorie_id (int):     Die ID der gesuchten Kategorie

    Returns:
        kategorie | None: Das Kategorie-Objekt oder None
    """
    return db.query(kategorie).filter(kategorie.id == kategorie_id).first()


def create_kategorie(db: Session, name: str, beschreibung: str = ""):
    """
    Erstellt eine neue Kategorie in der Datenbank.

    Args:
        db           (Session): Aktive Datenbank-Sitzung
        name         (str):     Name der Kategorie (muss eindeutig sein)
        beschreibung (str):     Optionale Beschreibung (Standard: leer)

    Returns:
        kategorie: Das neu erstellte Kategorie-Objekt mit gesetzter ID
    """
    kat = kategorie(name=name, beschreibung=beschreibung)  # Neues Objekt erstellen
    db.add(kat)      # Zur Sitzung hinzufügen
    db.commit()      # In der Datenbank speichern
    db.refresh(kat)  # Objekt mit DB-Werten aktualisieren
    return kat


# ─────────────────────────────────────────────────────────────────────────────
# CRUD-Operationen für Tags
# ─────────────────────────────────────────────────────────────────────────────

def get_all_tags(db: Session):
    """
    Gibt alle Tags (Schlagwörter) aus der Datenbank zurück.

    Args:
        db (Session): Aktive Datenbank-Sitzung

    Returns:
        list: Liste aller Tag-Objekte
    """
    tags = db.query(tag).all()  # Alle Zeilen aus der Tabelle 'tag'
    return tags


def get_tag_by_id(db: Session, tag_id: int):
    """
    Sucht ein einzelnes Tag anhand seiner ID.

    Args:
        db     (Session): Aktive Datenbank-Sitzung
        tag_id (int):     Die ID des gesuchten Tags

    Returns:
        tag | None: Das Tag-Objekt oder None
    """
    return db.query(tag).filter(tag.id == tag_id).first()


def create_tag(db: Session, name: str):
    """
    Erstellt ein neues Tag (Schlagwort) in der Datenbank.

    Args:
        db   (Session): Aktive Datenbank-Sitzung
        name (str):     Schlagwort (muss eindeutig sein, max. 50 Zeichen)

    Returns:
        tag: Das neu erstellte Tag-Objekt mit gesetzter ID
    """
    tag_obj = tag(name=name)  # Neues Tag-Objekt erstellen
    db.add(tag_obj)            # Zur Sitzung hinzufügen
    db.commit()                # In der Datenbank speichern
    db.refresh(tag_obj)        # Objekt mit DB-Werten aktualisieren
    return tag_obj


# ─────────────────────────────────────────────────────────────────────────────
# Material-CRUD-Operationen (Upload, Download, Suche, Löschen)
# ─────────────────────────────────────────────────────────────────────────────

# Ordner für große Dateien (>1MB), die im Dateisystem gespeichert werden
uploads_dir = "uploads"
os.makedirs(uploads_dir, exist_ok=True)  # Ordner erstellen, falls er noch nicht existiert

# Maximale Dateigröße für die Datenbankspeicherung: 1 Megabyte
# 1 MB = 1 * 1024 Kilobyte * 1024 Byte = 1.048.576 Byte
MAX_SIZE = 1 * 1024 * 1024  # 1 MB in Bytes

# Unterstützte Dateitypen mit ihren MIME-Types
# MIME-Type = Standard-Format zur Beschreibung des Dateityps im Internet
SUPPORTED_FILE_TYPES = {
    "pdf":  "application/pdf",                                                          # PDF-Dokument
    "doc":  "application/msword",                                                       # Word-Dokument (alt)
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",  # Word-Dokument (neu)
    "jpg":  "image/jpeg",                                                               # JPEG-Bild
    "jpeg": "image/jpeg",                                                               # JPEG-Bild (alternativ)
    "png":  "image/png",                                                                # PNG-Bild
    "py":   "text/x-python",                                                            # Python-Skript
    "txt":  "text/plain",                                                               # Textdatei
    "csv":  "text/csv",                                                                 # CSV-Tabellendatei
}


def upload_material(
    db: Session,
    file_path: str,
    titel: str,
    beschreibung: str,
    themengebiet_id: int,
    benutzer_id: int,
    kategorie_id: int,
    tag_ids: list[int] | None = None
):
    """
    Lädt eine Datei als Lernmaterial hoch und speichert sie intelligent.

    Speicherstrategie:
      - Datei ≤ 1 MB → Inhalt wird direkt in der Datenbank gespeichert (BLOB)
      - Datei > 1 MB → Datei wird im Ordner 'uploads/' gespeichert, nur der Pfad in der DB

    Args:
        db              (Session):         Aktive Datenbank-Sitzung
        file_path       (str):             Pfad zur lokalen Datei, die hochgeladen werden soll
        titel           (str):             Titel des Lernmaterials
        beschreibung    (str):             Beschreibung des Inhalts
        themengebiet_id (int):             ID des Themengebiets (muss in der DB existieren)
        benutzer_id     (int):             ID des Autors (muss in der DB existieren)
        kategorie_id    (int):             ID der Kategorie (muss in der DB existieren)
        tag_ids         (list[int] | None): Liste von Tag-IDs zum Verknüpfen (optional)

    Returns:
        material: Das neu erstellte Material-Objekt mit gesetzter ID

    Raises:
        FileNotFoundError: Wenn die angegebene Datei nicht existiert
    """
    # Prüfen ob die Datei überhaupt existiert, bevor wir weiterarbeiten
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Datei nicht gefunden: {file_path}")

    # Dateigröße in Bytes ermitteln
    file_size = os.path.getsize(file_path)

    # Nur den Dateinamen aus dem vollständigen Pfad extrahieren (z.B. "skript.pdf")
    file_name = os.path.basename(file_path)

    # Dateiendung extrahieren und in Kleinbuchstaben umwandeln (z.B. "PDF" → "pdf")
    # lstrip('.') entfernt den Punkt am Anfang (z.B. ".pdf" → "pdf")
    file_ext = os.path.splitext(file_name)[1].lower().lstrip('.')

    # MIME-Type bestimmen: bekannte Typen aus der Liste, sonst "Binärdatei"
    if file_ext in SUPPORTED_FILE_TYPES:
        file_type = SUPPORTED_FILE_TYPES[file_ext]
    else:
        file_type = "application/octet-stream"  # Standard für unbekannte Binärdateien

    # Dateiinhalt als Bytes einlesen (binärer Modus 'rb' = read binary)
    with open(file_path, 'rb') as f:
        file_content = f.read()

    # ──────────────────────────────────────────────────────────────────────────
    # Speicherstrategie: ≤1MB → Datenbank, >1MB → Dateisystem
    # ──────────────────────────────────────────────────────────────────────────
    if file_size <= MAX_SIZE:
        # Kleine Datei (≤1MB): Inhalt direkt in der Datenbank speichern
        # is_in_database=True zeigt an, dass der Inhalt in der DB liegt
        new_material = material(
            titel=titel,
            beschreibung=beschreibung,
            themengebiet_id=themengebiet_id,
            benutzer_id=benutzer_id,
            kategorie_id=kategorie_id,
            dateiname=file_name,        # Originaler Dateiname
            dateityp=file_type,         # MIME-Type der Datei
            dateigroesse=file_size,     # Größe in Bytes
            inhalt=file_content,        # Binärer Dateiinhalt (BLOB)
            is_in_database=True,        # Markierung: Inhalt ist in der DB
            speicherort=None            # Kein Dateipfad nötig (in DB gespeichert)
        )
    else:
        # Große Datei (>1MB): Im Dateisystem speichern, nur Pfad in DB merken
        # Eindeutigen Dateinamen erstellen, um Konflikte zu vermeiden
        # Beispiel: "skript_1716336242.pdf" (Name + Zeitstempel + Endung)
        unique_name = f"{os.path.splitext(file_name)[0]}_{int(time.time())}{os.path.splitext(file_name)[1]}"
        storage_path = os.path.join(uploads_dir, unique_name)  # Vollständiger Zieldateipfad

        # Datei in den uploads-Ordner kopieren
        import shutil
        shutil.copy2(file_path, storage_path)  # copy2 kopiert auch Metadaten (Erstellungsdatum etc.)

        # Material-Objekt ohne Dateiinhalt, aber mit Speicherort-Pfad
        new_material = material(
            titel=titel,
            beschreibung=beschreibung,
            themengebiet_id=themengebiet_id,
            benutzer_id=benutzer_id,
            kategorie_id=kategorie_id,
            dateiname=file_name,        # Originaler Dateiname
            dateityp=file_type,         # MIME-Type der Datei
            dateigroesse=file_size,     # Größe in Bytes
            inhalt=None,                # Kein BLOB (Datei liegt im Dateisystem)
            is_in_database=False,       # Markierung: Inhalt ist NICHT in der DB
            speicherort=storage_path    # Pfad zur Datei im Dateisystem
        )

    db.add(new_material)  # Material-Objekt zur Sitzung hinzufügen
    db.flush()            # Vorläufig in die DB schreiben, damit new_material.id gesetzt wird

    # Tags mit dem Material verknüpfen (n:m-Beziehung über material_tag-Tabelle)
    if tag_ids:
        for tag_id in tag_ids:
            # Für jede Tag-ID einen Eintrag in der Verknüpfungstabelle erstellen
            link = material_tag(material_id=new_material.id, tag_id=tag_id)
            db.add(link)

    db.commit()               # Alle Änderungen dauerhaft speichern
    db.refresh(new_material)  # Objekt mit finalen DB-Werten aktualisieren
    return new_material


def download_material(db: Session, material_id: int, output_dir: str = "."):
    """
    Lädt ein Lernmaterial herunter und speichert es lokal.

    Abhängig davon, wo das Material gespeichert ist:
      - In der Datenbank → Inhalt aus BLOB lesen und in Datei schreiben
      - Im Dateisystem  → Datei aus uploads-Ordner in Zielordner kopieren

    Args:
        db          (Session): Aktive Datenbank-Sitzung
        material_id (int):     ID des herunterzuladenden Materials
        output_dir  (str):     Zielordner für die heruntergeladene Datei (Standard: aktueller Ordner)

    Returns:
        str: Vollständiger Pfad der heruntergeladenen Datei

    Raises:
        ValueError:        Wenn kein Material mit dieser ID existiert oder kein Inhalt vorhanden
        FileNotFoundError: Wenn die Datei im Dateisystem nicht mehr vorhanden ist
    """
    # Material anhand der ID aus der Datenbank holen
    mat = db.query(material).filter(material.id == material_id).first()
    if not mat:
        raise ValueError(f"Material mit ID {material_id} nicht gefunden")

    # Zieldateipfad = Zielordner + originaler Dateiname
    output_path = os.path.join(output_dir, mat.dateiname)

    if mat.is_in_database:
        # Material ist als BLOB in der Datenbank gespeichert
        if mat.inhalt:
            # Binären Inhalt in eine neue Datei schreiben ('wb' = write binary)
            with open(output_path, 'wb') as f:
                f.write(mat.inhalt)
            return output_path
        else:
            raise ValueError("Material in DB hat keinen Inhalt")
    else:
        # Material liegt als Datei im Dateisystem (uploads-Ordner)
        if mat.speicherort and os.path.exists(mat.speicherort):
            import shutil
            shutil.copy2(mat.speicherort, output_path)  # Datei in Zielordner kopieren
            return output_path
        else:
            raise FileNotFoundError(f"Datei nicht gefunden: {mat.speicherort}")


def search_materials(
    db: Session,
    titel: str | None = None,
    themengebiet_id: int | None = None,
    benutzer_id: int | None = None,
    kategorie_id: int | None = None,
    tag_id: int | None = None
):
    """
    Durchsucht Materialien mit verschiedenen optionalen Filtern.

    Alle Parameter sind optional. Nur die angegebenen Filter werden angewendet.
    Mehrere Filter werden mit UND verknüpft (alle müssen passen).

    Args:
        db              (Session):    Aktive Datenbank-Sitzung
        titel           (str | None): Suche im Titel (Groß-/Kleinschreibung egal, Teilsuche möglich)
        themengebiet_id (int | None): Nur Materialien dieses Themengebiets
        benutzer_id     (int | None): Nur Materialien dieses Autors
        kategorie_id    (int | None): Nur Materialien dieser Kategorie
        tag_id          (int | None): Nur Materialien mit diesem Tag

    Returns:
        list: Liste der gefundenen Material-Objekte (kann leer sein)
    """
    query = db.query(material)  # Startpunkt: alle Materialien abfragen

    # Titelsuche: ilike() = case-insensitive LIKE → findet auch Teilwörter
    # "%titel%" bedeutet: Suchbegriff kann irgendwo im Titel stehen
    if titel:
        query = query.filter(material.titel.ilike(f"%{titel}%"))

    # Filter nach Themengebiet (exakte ID-Übereinstimmung)
    if themengebiet_id:
        query = query.filter(material.themengebiet_id == themengebiet_id)

    # Filter nach Autor (Benutzer-ID)
    if benutzer_id:
        query = query.filter(material.benutzer_id == benutzer_id)

    # Filter nach Kategorie
    if kategorie_id:
        query = query.filter(material.kategorie_id == kategorie_id)

    # Filter nach Tag: JOIN mit material_tag-Tabelle nötig (n:m-Beziehung)
    if tag_id:
        query = query.join(material_tag).filter(material_tag.tag_id == tag_id)

    return query.all()  # Alle passenden Materialien als Liste zurückgeben


def get_material_by_id(db: Session, material_id: int):
    """
    Sucht ein einzelnes Material anhand seiner ID.

    Args:
        db          (Session): Aktive Datenbank-Sitzung
        material_id (int):     Die ID des gesuchten Materials

    Returns:
        material | None: Das Material-Objekt oder None, wenn nicht gefunden
    """
    return db.query(material).filter(material.id == material_id).first()


def delete_material(db: Session, material_id: int):
    """
    Löscht ein Material aus der Datenbank und, falls vorhanden, die Datei im Dateisystem.

    Bei Materialien, die im Dateisystem gespeichert sind, wird auch die
    physische Datei aus dem uploads-Ordner gelöscht (kein verwaister Dateirest).

    Args:
        db          (Session): Aktive Datenbank-Sitzung
        material_id (int):     ID des zu löschenden Materials

    Returns:
        bool: True, wenn erfolgreich gelöscht

    Raises:
        ValueError: Wenn kein Material mit dieser ID existiert
    """
    # Material aus der Datenbank holen
    mat = db.query(material).filter(material.id == material_id).first()
    if not mat:
        raise ValueError(f"Material mit ID {material_id} nicht gefunden")

    # Wenn die Datei im Dateisystem liegt, auch dort löschen
    if not mat.is_in_database and mat.speicherort and os.path.exists(mat.speicherort):
        os.remove(mat.speicherort)  # Physische Datei löschen

    # Material aus der Datenbank löschen
    # Die zugehörigen material_tag-Einträge werden automatisch durch CASCADE gelöscht
    db.delete(mat)
    db.commit()  # Löschung dauerhaft speichern
    return True


# ─────────────────────────────────────────────────────────────────────────────
# Kommentar-Operationen
# ─────────────────────────────────────────────────────────────────────────────

def get_comments_for_material(db: Session, material_id: int):
    """
    Gibt alle Kommentare zu einem bestimmten Material zurück.

    Args:
        db          (Session): Aktive Datenbank-Sitzung
        material_id (int):     ID des Materials, dessen Kommentare gesucht werden

    Returns:
        list: Liste aller Kommentar-Objekte für dieses Material
    """
    return db.query(kommentar).filter(kommentar.material_id == material_id).all()


def create_comment(db: Session, material_id: int, autor_id: int, text: str):
    """
    Erstellt einen neuen Kommentar zu einem Material.

    Args:
        db          (Session): Aktive Datenbank-Sitzung
        material_id (int):     ID des Materials, das kommentiert wird
        autor_id    (int):     ID des Benutzers, der den Kommentar schreibt
        text        (str):     Inhalt des Kommentars

    Returns:
        kommentar: Das neu erstellte Kommentar-Objekt mit gesetzter ID
    """
    comment = kommentar(
        material_id=material_id,  # Zu welchem Material gehört der Kommentar
        autor_id=autor_id,        # Wer hat den Kommentar geschrieben
        text=text                 # Der eigentliche Kommentartext
    )
    db.add(comment)      # Zur Sitzung hinzufügen
    db.commit()          # In der Datenbank speichern
    db.refresh(comment)  # Objekt mit DB-Werten aktualisieren (z.B. ID und Datum)
    return comment


def get_comment_by_id(db: Session, comment_id: int):
    """
    Sucht einen einzelnen Kommentar anhand seiner ID.

    Args:
        db         (Session): Aktive Datenbank-Sitzung
        comment_id (int):     Die ID des gesuchten Kommentars

    Returns:
        kommentar | None: Das Kommentar-Objekt oder None, wenn nicht gefunden
    """
    return db.query(kommentar).filter(kommentar.id == comment_id).first()


def delete_comment(db: Session, comment_id: int):
    """
    Löscht einen Kommentar aus der Datenbank.

    Args:
        db         (Session): Aktive Datenbank-Sitzung
        comment_id (int):     ID des zu löschenden Kommentars

    Returns:
        bool: True, wenn erfolgreich gelöscht

    Raises:
        ValueError: Wenn kein Kommentar mit dieser ID existiert
    """
    comment = db.query(kommentar).filter(kommentar.id == comment_id).first()
    if not comment:
        raise ValueError(f"Kommentar mit ID {comment_id} nicht gefunden")

    db.delete(comment)  # Kommentar aus der Sitzung entfernen
    db.commit()         # Löschung dauerhaft speichern
    return True


# ─────────────────────────────────────────────────────────────────────────────
# Pflichtabfragen (7+ Suchabfragen für das LF8-Abschlussprojekt)
# Jede Abfrage demonstriert eine andere SQL-Technik.
# ─────────────────────────────────────────────────────────────────────────────

def anzahl_material_pro_themen(db: Session):
    """
    Abfrage 1: Aggregation mit COUNT – Wie viele Materialien gibt es pro Themengebiet?

    SQL-Äquivalent:
        SELECT themengebiet.name, COUNT(*) AS anzahl
        FROM themengebiet
        JOIN material ON material.themengebiet_id = themengebiet.id
        GROUP BY themengebiet.name

    Args:
        db (Session): Aktive Datenbank-Sitzung

    Returns:
        list[tuple]: Liste von (Themengebiet-Name, Anzahl-Materialien)
    """
    materials = (
        db.query(themengebiet.name, func.count().label("anzahl"))  # Thema + Anzahl zählen
        .join(material, material.themengebiet_id == themengebiet.id)  # Tabellen verbinden
        .group_by(themengebiet.name)  # Ergebnisse nach Thema gruppieren
        .all()
    )
    return materials


def durchschnitt_dateigroesse_pro_typ(db: Session):
    """
    Abfrage 2: Aggregation mit AVG – Durchschnittliche Dateigröße pro Dateityp.

    SQL-Äquivalent:
        SELECT dateityp, AVG(dateigroesse) AS durchschnitt
        FROM material
        GROUP BY dateityp

    Args:
        db (Session): Aktive Datenbank-Sitzung

    Returns:
        list[tuple]: Liste von (Dateityp, Durchschnittsgröße in Bytes)
    """
    result = (
        db.query(material.dateityp, func.avg(material.dateigroesse).label("durchschnitt"))
        .group_by(material.dateityp)  # Nach Dateityp (z.B. "application/pdf") gruppieren
        .all()
    )
    return result


def materialien_mit_themen(db: Session):
    """
    Abfrage 3: Inner Join – Materialien mit ihren Themengebieten.

    Verbindet die Tabellen 'material' und 'themengebiet' über die Fremdschlüssel-Beziehung.
    Nur Materialien, die ein Themengebiet haben, werden angezeigt (INNER JOIN).

    SQL-Äquivalent:
        SELECT material.titel, material.dateiname, themengebiet.name AS themengebiet
        FROM material
        JOIN themengebiet ON material.themengebiet_id = themengebiet.id

    Args:
        db (Session): Aktive Datenbank-Sitzung

    Returns:
        list[tuple]: Liste von (Material-Titel, Dateiname, Themengebiet-Name)
    """
    result = (
        db.query(material.titel, material.dateiname, themengebiet.name.label("themengebiet"))
        .join(themengebiet, material.themengebiet_id == themengebiet.id)  # JOIN über Fremdschlüssel
        .all()
    )
    return result


def materialien_mit_kommentaren(db: Session):
    """
    Abfrage 4: Inner Join – Materialien mit ihren Kommentaren.

    Verbindet 'material' und 'kommentar'. Nur Materialien, die mindestens
    einen Kommentar haben, erscheinen in der Ergebnisliste.

    SQL-Äquivalent:
        SELECT material.titel, material.dateiname, kommentar.text, kommentar.erstellungsdatum
        FROM material
        JOIN kommentar ON material.id = kommentar.material_id

    Args:
        db (Session): Aktive Datenbank-Sitzung

    Returns:
        list[tuple]: Liste von (Material-Titel, Dateiname, Kommentar-Text, Erstellungsdatum)
    """
    result = (
        db.query(
            material.titel,
            material.dateiname,
            kommentar.text,
            kommentar.erstellungsdatum
        )
        .join(kommentar, material.id == kommentar.material_id)  # Verknüpfung über material_id
        .all()
    )
    return result


def kommentare_pro_material(db: Session):
    """
    Abfrage 5: Join + Aggregation – Anzahl der Kommentare pro Material.

    Kombiniert einen JOIN mit einer COUNT-Aggregation:
    Zeigt für jedes Material, wie viele Kommentare es hat.

    SQL-Äquivalent:
        SELECT material.titel, material.dateiname, COUNT(kommentar.id) AS anzahl_kommentare
        FROM material
        JOIN kommentar ON material.id = kommentar.material_id
        GROUP BY material.id, material.titel, material.dateiname

    Args:
        db (Session): Aktive Datenbank-Sitzung

    Returns:
        list[tuple]: Liste von (Material-Titel, Dateiname, Kommentar-Anzahl)
    """
    result = (
        db.query(
            material.titel,
            material.dateiname,
            func.count(kommentar.id).label("anzahl_kommentare")  # Kommentare zählen
        )
        .join(kommentar, material.id == kommentar.material_id)
        .group_by(material.id, material.titel, material.dateiname)  # Nach Material gruppieren
        .all()
    )
    return result


def material_mit_autor_und_thema(db: Session):
    """
    Abfrage 6: Multi-Table Join – Material mit Autor und Themengebiet.

    Verbindet drei Tabellen gleichzeitig: material, benutzer (Autor) und themengebiet.
    Dies ist ein "Multi-JOIN" – mehrere Tabellen werden in einer Abfrage verknüpft.

    SQL-Äquivalent:
        SELECT material.titel, material.dateiname, benutzer.username AS autor,
               themengebiet.name AS themengebiet, material.erstellungsdatum
        FROM material
        JOIN benutzer ON material.benutzer_id = benutzer.id
        JOIN themengebiet ON material.themengebiet_id = themengebiet.id

    Args:
        db (Session): Aktive Datenbank-Sitzung

    Returns:
        list[tuple]: Liste von (Titel, Dateiname, Autor-Name, Themengebiet-Name, Erstellungsdatum)
    """
    result = (
        db.query(
            material.titel,
            material.dateiname,
            benutzer.username.label("autor"),         # Benutzername des Autors
            themengebiet.name.label("themengebiet"),  # Name des Themengebiets
            material.erstellungsdatum
        )
        .join(benutzer, material.benutzer_id == benutzer.id)              # JOIN mit Benutzer-Tabelle
        .join(themengebiet, material.themengebiet_id == themengebiet.id)  # JOIN mit Themengebiet-Tabelle
        .all()
    )
    return result


def suche_material_mit_filtern(db: Session, thema_id=None, autor_id=None):
    """
    Abfrage 7: Multi-Table Join mit optionalen Filtern – Vollständige Materialsuche.

    Verbindet vier Tabellen gleichzeitig (material, benutzer, themengebiet, kategorie)
    und erlaubt zusätzlich optionale WHERE-Filter nach Thema und Autor.
    Dies ist die komplexeste Abfrage des Projekts.

    SQL-Äquivalent:
        SELECT material.titel, material.beschreibung, material.dateiname,
               material.dateityp, material.dateigroesse,
               benutzer.username AS autor,
               themengebiet.name AS themengebiet,
               kategorie.name AS kategorie
        FROM material
        JOIN benutzer     ON material.benutzer_id     = benutzer.id
        JOIN themengebiet ON material.themengebiet_id = themengebiet.id
        JOIN kategorie    ON material.kategorie_id    = kategorie.id
        [WHERE material.themengebiet_id = thema_id]   -- optional
        [AND   material.benutzer_id     = autor_id]   -- optional

    Args:
        db       (Session):   Aktive Datenbank-Sitzung
        thema_id (int | None): Filter auf ein bestimmtes Themengebiet (optional)
        autor_id (int | None): Filter auf einen bestimmten Autor (optional)

    Returns:
        list[tuple]: Liste von Materialien mit allen Details aus vier Tabellen
    """
    query = (
        db.query(
            material.titel,
            material.beschreibung,
            material.dateiname,
            material.dateityp,
            material.dateigroesse,
            benutzer.username.label("autor"),         # Autoren-Name aus benutzer-Tabelle
            themengebiet.name.label("themengebiet"),  # Themengebiet-Name
            kategorie.name.label("kategorie")         # Kategorie-Name
        )
        .join(benutzer, material.benutzer_id == benutzer.id)              # Autoren-JOIN
        .join(themengebiet, material.themengebiet_id == themengebiet.id)  # Themengebiet-JOIN
        .join(kategorie, material.kategorie_id == kategorie.id)           # Kategorie-JOIN
    )

    # Optionaler Filter nach Themengebiet (nur anwenden, wenn angegeben)
    if thema_id:
        query = query.filter(material.themengebiet_id == thema_id)

    # Optionaler Filter nach Autor (nur anwenden, wenn angegeben)
    if autor_id:
        query = query.filter(material.benutzer_id == autor_id)

    return query.all()


def get_all_materials(db: Session):
    """
    Gibt alle Lernmaterialien aus der Datenbank zurück.

    Hilfsfunktion zum Auflisten aller Materialien ohne Filter.

    Args:
        db (Session): Aktive Datenbank-Sitzung

    Returns:
        list: Liste aller Material-Objekte
    """
    materials = db.query(material).all()  # Alle Zeilen aus der Tabelle 'material'
    return materials
