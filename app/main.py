from typing import Optional
from fastapi import FastAPI, Request, Depends, HTTPException, Form, File
from database import *
from services import *
from schemas import *
# from fastapi.templating import Jinja2Templates
# from fastapi.staticfiles import StaticFiles


app = FastAPI()


@app.get("/users")
async def get_users(db: Session = Depends(get_db)):
    return get_all_users(db)


@app.post("/users")
async def create_new_user(data: UserBase, db: Session = Depends(get_db)):
    return create_user(db, data)


@app.get("/themen")
async def get_themen(db: Session = Depends(get_db)):
    return get_all_themen(db)


@app.post("/themen")
async def create_new_theme(data: Themen, db: Session = Depends(get_db)):
    return create_themen(db, data)


@app.get("/kategorie")
async def get_kategories(db: Session = Depends(get_db)):
    return get_all_kategories(db)


@app.post("/kategorie")
async def create_new_kategorie(data: Kategorie, db: Session = Depends(get_db)):
    return create_kategorie(db, data)


@app.get("/tag")
async def get_tags(db: Session = Depends(get_db)):
    return get_all_tags(db)


@app.post("/tag")
async def create_new_tag(data: Tag, db: Session = Depends(get_db)):
    return create_tag(db, data)


@app.post("/material")
async def upload_material(
    titel: str = Form(...),
    beschreibung: str = Form(...),
    themengebiet_id: int = Form(...),
    benutzer_id: int = Form(...),
    kategorie_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    return await create_material(
        db, file, titel, beschreibung, themengebiet_id, benutzer_id, kategorie_id
    )


@app.get("/material_count", response_model=List[AnzahlMaterialProThemen])
async def get_material_count(db: Session = Depends(get_db)):
    return anzahl_material_pro_themen(db)
