from fastapi import UploadFile,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.testing.pickleable import User
from database import *
from schemas import*
import os


def get_all_users(db:Session):
    users = db.query(benutzer).all()
    return users

def create_user(db:Session, data:UserBase):
    user = benutzer(**data.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)


def get_all_themen(db:Session):
    themen = db.query(themengebiet).all()
    return themen

def create_themen(db:Session, data:Themen):
    themen = themengebiet(**data.model_dump())
    db.add(themen)
    db.commit()
    db.refresh(themen)

def get_all_kategories(db:Session):
    kategories = db.query(kategorie).all()
    return kategories

def create_kategorie(db:Session, data:Kategorie):
    new_kategorie = kategorie(**data.model_dump())
    db.add(new_kategorie)
    db.commit()
    db.refresh(new_kategorie)

def get_all_tags(db:Session):
    tags = db.query(tag).all()
    return tags

def create_tag(db:Session, data:Tag):
    for name in data.name:
        new_tag = tag(name=name)
        db.add(new_tag)
    db.commit()


## materials
ordner = "uploads"
Big_uploads =os.makedirs("uploads",exist_ok=True)

Max_size = 1*1024*1024

file_type= [
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.ms-powerpoint",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",

    "application/pdf",
    "application/octet-stream",
    "text/plain",
    "text/csv",

    "application/vnd.oasis.opendocument.text",
    "application/vnd.oasis.opendocument.spreadsheet",
    "application/vnd.oasis.opendocument.presentation",

    "application/rtf",
    "application/json",
    "application/zip",
]

async def create_material(db: Session, file: UploadFile, titel: str, beschreibung: str, themengebiet_id: int, benutzer_id: int, kategorie_id: int,tag_ids: list[int] = []):
    inhalt = await file.read()
    dateigroesse = len(inhalt)
    dateiname = file.filename
    dateityp = file.content_type

    if dateityp not in file_type:
        raise HTTPException(status_code=404,detail="File type not supported")

    if dateigroesse < Max_size:
        new_material = material(
              titel=titel,
              beschreibung=beschreibung,
              themengebiet_id=themengebiet_id,
              benutzer_id=benutzer_id,
              kategorie_id=kategorie_id,
              dateiname=dateiname,
              dateityp=dateityp,
              dateigroesse=dateigroesse,
              inhalt=inhalt,
              is_in_database=True,
              speicherort=None
          )
    else:
        path = f"uploads/{dateiname}"
        with open(path, "wb") as f:
            f.write(inhalt)

        new_material = material(
            titel=titel,
            beschreibung=beschreibung,
            themengebiet_id=themengebiet_id,
            benutzer_id=benutzer_id,
            kategorie_id=kategorie_id,
            dateiname=dateiname,
            dateityp=dateityp,
            dateigroesse=dateigroesse,
            inhalt=None,
            is_in_database=False,
            speicherort=path
        )

    db.add(new_material)
    db.flush()

    for tag_id in tag_ids:
        link = material_tag(material_id=new_material.id, tag_id=tag_id)
        db.add(link)

    db.commit()
    db.refresh(new_material)
    return new_material

def anzahl_material_pro_themen(db: Session):
    materials = (
        db.query(themengebiet.name, func.count().label("anzahl"))
        .join(material, material.themengebiet_id == themengebiet.id)
        .group_by(themengebiet.name)
        .all()
    )
    return materials

