# Hier sind alle Funktionen für die Datenbank.
# Wir können Materialien hochladen, suchen und löschen.
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import *
import os
import time

# Ordner für große Dateien
uploads_dir = "uploads"
os.makedirs(uploads_dir, exist_ok=True)

# Dateien kleiner als 1 MB kommen direkt in die Datenbank
MAX_SIZE = 1 * 1024 * 1024

# Liste von erlaubten Dateitypen
SUPPORTED_FILE_TYPES = {
    "pdf":  "application/pdf",
    "doc":  "application/msword",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "jpg":  "image/jpeg",
    "jpeg": "image/jpeg",
    "png":  "image/png",
    "py":   "text/x-python",
    "txt":  "text/plain",
    "csv":  "text/csv",
}


# Alle Benutzer aus der Datenbank holen
def get_all_users(db):
    return db.query(benutzer).all()

# Einen Benutzer anhand der ID suchen
def get_user_by_id(db, user_id):
    return db.query(benutzer).filter(benutzer.id == user_id).first()

# Neuen Benutzer anlegen
def create_user(db, username, email, rolle="Azubi"):
    user = benutzer(username=username, email=email, rolle=rolle)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# Alle Themengebiete holen
def get_all_themen(db):
    return db.query(themengebiet).all()

# Ein Themengebiet anhand der ID suchen
def get_thema_by_id(db, thema_id):
    return db.query(themengebiet).filter(themengebiet.id == thema_id).first()

# Neues Themengebiet anlegen
def create_thema(db, name, beschreibung=""):
    thema = themengebiet(name=name, beschreibung=beschreibung)
    db.add(thema)
    db.commit()
    db.refresh(thema)
    return thema


# Alle Kategorien holen
def get_all_kategories(db):
    return db.query(kategorie).all()

# Eine Kategorie anhand der ID suchen
def get_kategorie_by_id(db, kategorie_id):
    return db.query(kategorie).filter(kategorie.id == kategorie_id).first()

# Neue Kategorie anlegen
def create_kategorie(db, name, beschreibung=""):
    kat = kategorie(name=name, beschreibung=beschreibung)
    db.add(kat)
    db.commit()
    db.refresh(kat)
    return kat


# Alle Tags holen
def get_all_tags(db):
    return db.query(tag).all()

# Einen Tag anhand der ID suchen
def get_tag_by_id(db, tag_id):
    return db.query(tag).filter(tag.id == tag_id).first()

# Neuen Tag anlegen
def create_tag(db, name):
    tag_obj = tag(name=name)
    db.add(tag_obj)
    db.commit()
    db.refresh(tag_obj)
    return tag_obj


# Alle Materialien holen
def get_all_materials(db):
    return db.query(material).all()

# Ein Material anhand der ID suchen
def get_material_by_id(db, material_id):
    return db.query(material).filter(material.id == material_id).first()


# Eine Datei hochladen – kleine Dateien kommen in die Datenbank, große auf die Festplatte
def upload_material(db, file_path, titel, beschreibung, themengebiet_id, benutzer_id, kategorie_id, tag_ids=None):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Datei nicht gefunden: {file_path}")

    file_size = os.path.getsize(file_path)
    file_name = os.path.basename(file_path)
    file_ext  = os.path.splitext(file_name)[1].lower().lstrip('.')
    file_type = SUPPORTED_FILE_TYPES.get(file_ext, "application/octet-stream")

    with open(file_path, 'rb') as f:
        file_content = f.read()

    if file_size <= MAX_SIZE:
        new_material = material(
            titel=titel,
            beschreibung=beschreibung,
            themengebiet_id=themengebiet_id,
            benutzer_id=benutzer_id,
            kategorie_id=kategorie_id,
            dateiname=file_name,
            dateityp=file_type,
            dateigroesse=file_size,
            inhalt=file_content,
            is_in_database=True,
            speicherort=None
        )
    else:
        import shutil
        unique_name  = f"{os.path.splitext(file_name)[0]}_{int(time.time())}{os.path.splitext(file_name)[1]}"
        storage_path = os.path.join(uploads_dir, unique_name)
        shutil.copy2(file_path, storage_path)
        new_material = material(
            titel=titel,
            beschreibung=beschreibung,
            themengebiet_id=themengebiet_id,
            benutzer_id=benutzer_id,
            kategorie_id=kategorie_id,
            dateiname=file_name,
            dateityp=file_type,
            dateigroesse=file_size,
            inhalt=None,
            is_in_database=False,
            speicherort=storage_path
        )

    db.add(new_material)
    db.flush()

    if tag_ids:
        for tid in tag_ids:
            db.add(material_tag(material_id=new_material.id, tag_id=tid))

    db.commit()
    db.refresh(new_material)
    return new_material


# Eine Datei herunterladen – aus Datenbank oder von der Festplatte
def download_material(db, material_id, output_dir="."):
    mat = db.query(material).filter(material.id == material_id).first()
    if not mat:
        raise ValueError(f"Material {material_id} nicht gefunden")

    output_path = os.path.join(output_dir, mat.dateiname)

    if mat.is_in_database:
        if not mat.inhalt:
            raise ValueError("Kein Inhalt in der Datenbank")
        with open(output_path, 'wb') as f:
            f.write(mat.inhalt)
    else:
        if not mat.speicherort or not os.path.exists(mat.speicherort):
            raise FileNotFoundError(f"Datei nicht gefunden: {mat.speicherort}")
        import shutil
        shutil.copy2(mat.speicherort, output_path)

    return output_path


# Materialien suchen – man kann nach Titel, Thema, Autor oder Kategorie filtern
def search_materials(db, titel=None, themengebiet_id=None, benutzer_id=None, kategorie_id=None, tag_id=None):
    query = db.query(material)
    if titel:
        query = query.filter(material.titel.ilike(f"%{titel}%"))
    if themengebiet_id:
        query = query.filter(material.themengebiet_id == themengebiet_id)
    if benutzer_id:
        query = query.filter(material.benutzer_id == benutzer_id)
    if kategorie_id:
        query = query.filter(material.kategorie_id == kategorie_id)
    if tag_id:
        query = query.join(material_tag).filter(material_tag.tag_id == tag_id)
    return query.all()


# Ein Material löschen – wenn die Datei auf der Festplatte liegt, wird sie auch gelöscht
def delete_material(db, material_id):
    mat = db.query(material).filter(material.id == material_id).first()
    if not mat:
        raise ValueError(f"Material {material_id} nicht gefunden")
    if not mat.is_in_database and mat.speicherort and os.path.exists(mat.speicherort):
        os.remove(mat.speicherort)
    db.delete(mat)
    db.commit()
    return True


# Alle Kommentare für ein Material holen
def get_comments_for_material(db, material_id):
    return db.query(kommentar).filter(kommentar.material_id == material_id).all()

# Neuen Kommentar schreiben
def create_comment(db, material_id, autor_id, text):
    k = kommentar(material_id=material_id, autor_id=autor_id, text=text)
    db.add(k)
    db.commit()
    db.refresh(k)
    return k

# Einen Kommentar anhand der ID suchen
def get_comment_by_id(db, comment_id):
    return db.query(kommentar).filter(kommentar.id == comment_id).first()

# Einen Kommentar löschen
def delete_comment(db, comment_id):
    k = db.query(kommentar).filter(kommentar.id == comment_id).first()
    if not k:
        raise ValueError(f"Kommentar {comment_id} nicht gefunden")
    db.delete(k)
    db.commit()
    return True


# Abfrage 1: Wie viele Materialien gibt es pro Themengebiet? (COUNT)
def anzahl_material_pro_themen(db):
    return (
        db.query(themengebiet.name, func.count().label("anzahl"))
        .join(material, material.themengebiet_id == themengebiet.id)
        .group_by(themengebiet.name)
        .all()
    )

# Abfrage 2: Wie groß sind die Dateien im Durchschnitt pro Dateityp? (AVG)
def durchschnitt_dateigroesse_pro_typ(db):
    return (
        db.query(material.dateityp, func.avg(material.dateigroesse).label("durchschnitt"))
        .group_by(material.dateityp)
        .all()
    )

# Abfrage 3: Materialien mit ihrem Themengebiet anzeigen (JOIN)
def materialien_mit_themen(db):
    return (
        db.query(material.titel, material.dateiname, themengebiet.name.label("themengebiet"))
        .join(themengebiet, material.themengebiet_id == themengebiet.id)
        .all()
    )

# Abfrage 4: Materialien mit ihren Kommentaren anzeigen (JOIN)
def materialien_mit_kommentaren(db):
    return (
        db.query(material.titel, material.dateiname, kommentar.text, kommentar.erstellungsdatum)
        .join(kommentar, material.id == kommentar.material_id)
        .all()
    )

# Abfrage 5: Wie viele Kommentare hat jedes Material? (JOIN + COUNT)
def kommentare_pro_material(db):
    return (
        db.query(material.titel, material.dateiname, func.count(kommentar.id).label("anzahl"))
        .join(kommentar, material.id == kommentar.material_id)
        .group_by(material.id, material.titel, material.dateiname)
        .all()
    )

# Abfrage 6: Material mit Autor und Themengebiet anzeigen (zwei JOINs)
def material_mit_autor_und_thema(db):
    return (
        db.query(
            material.titel,
            material.dateiname,
            benutzer.username.label("autor"),
            themengebiet.name.label("themengebiet"),
            material.erstellungsdatum
        )
        .join(benutzer, material.benutzer_id == benutzer.id)
        .join(themengebiet, material.themengebiet_id == themengebiet.id)
        .all()
    )

# Abfrage 7: Vollständige Suche mit Autor, Thema und Kategorie (drei JOINs)
def suche_material_mit_filtern(db, thema_id=None, autor_id=None):
    query = (
        db.query(
            material.titel,
            material.beschreibung,
            material.dateiname,
            material.dateityp,
            material.dateigroesse,
            benutzer.username.label("autor"),
            themengebiet.name.label("themengebiet"),
            kategorie.name.label("kategorie")
        )
        .join(benutzer, material.benutzer_id == benutzer.id)
        .join(themengebiet, material.themengebiet_id == themengebiet.id)
        .join(kategorie, material.kategorie_id == kategorie.id)
    )
    if thema_id:
        query = query.filter(material.themengebiet_id == thema_id)
    if autor_id:
        query = query.filter(material.benutzer_id == autor_id)
    return query.all()