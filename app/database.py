from sqlalchemy import *
from sqlalchemy.engine import URL
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=r'C:\Users\auric\Desktop\Auric\Learning Stuff\Python\daten-system-bergreifend\.env')

mysql_url = URL.create(
    drivername=os.getenv("DB_DRIVER") or "mysql+pymysql",
    username=os.getenv("DB_USERNAME") or "root",
    password=os.getenv("DB_PASSWORD") or "",
    host=os.getenv("DB_HOST") or "localhost",
    port=int(os.getenv("DB_PORT") or "3306"),
    database=os.getenv("DB_NAME") or "lernmaterialverwaltung"
)

engine = create_engine(mysql_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = automap_base()
Base.prepare(autoload_with=engine)

benutzer     = Base.classes.benutzer
kategorie    = Base.classes.kategorie
kommentar    = Base.classes.kommentar
material     = Base.classes.material
material_tag = Base.classes.material_tag
tag          = Base.classes.tag
themengebiet = Base.classes.themengebiet
version      = Base.classes.version