# Hier verbinden wir uns mit der MySQL-Datenbank.
# Die Zugangsdaten kommen aus der .env Datei.
from sqlalchemy import *
from sqlalchemy.engine import URL
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# .env Datei laden – dort stehen Passwort und Datenbankname
load_dotenv(dotenv_path=r'C:\Users\auric\Desktop\Auric\Learning Stuff\Python\daten-system-bergreifend\.env')

# Verbindungsadresse für die Datenbank zusammenbauen
mysql_url = URL.create(
    drivername=os.getenv("DB_DRIVER") or "mysql+pymysql",
    username=os.getenv("DB_USERNAME") or "root",
    password=os.getenv("DB_PASSWORD") or "",
    host=os.getenv("DB_HOST") or "localhost",
    port=int(os.getenv("DB_PORT") or "3306"),
    database=os.getenv("DB_NAME") or "lernmaterialverwaltung"
)

# Verbindung zur Datenbank herstellen
engine = create_engine(mysql_url)

# SessionLocal öffnet eine neue Verbindung wenn wir sie brauchen
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# SQLAlchemy liest die Tabellen automatisch aus der Datenbank
Base = automap_base()
Base.prepare(autoload_with=engine)

# Jede Tabelle bekommt einen Namen in Python
benutzer     = Base.classes.benutzer
kategorie    = Base.classes.kategorie
kommentar    = Base.classes.kommentar
material     = Base.classes.material
material_tag = Base.classes.material_tag
tag          = Base.classes.tag
themengebiet = Base.classes.themengebiet
version      = Base.classes.version