"""
Datenbankverbindung und Konfiguration.

Diese Datei stellt die Verbindung zur MySQL-Datenbank her.
Alle Tabellen werden automatisch aus der bestehenden Datenbank ausgelesen (automap).
Das bedeutet: Python erkennt die Tabellenstruktur selbst – wir müssen sie nicht
nochmal manuell beschreiben.
"""

from sqlalchemy import *                       # Alle wichtigen SQLAlchemy-Werkzeuge importieren
from sqlalchemy.engine import URL              # Hilft beim Erstellen der Verbindungs-URL
from sqlalchemy.ext.automap import automap_base  # Liest Tabellen automatisch aus der Datenbank
from sqlalchemy.orm import sessionmaker        # Erstellt Datenbank-Sitzungen (Sessions)
from sqlalchemy import create_engine           # Erstellt die Datenbankverbindung (Engine)
from dotenv import load_dotenv                 # Liest Umgebungsvariablen aus einer .env-Datei
import os                                      # Für den Zugriff auf Umgebungsvariablen

# Lädt die Einstellungen aus der .env-Datei (z.B. Passwort, Hostname)
# So müssen geheime Daten nicht direkt im Code stehen
load_dotenv(dotenv_path=r'C:\Users\auric\Desktop\Auric\Learning Stuff\Python\daten-system-bergreifend\.env')

# Lese die Datenbankeinstellungen aus den Umgebungsvariablen
# Falls eine Variable nicht gesetzt ist, wird ein sicherer Standardwert verwendet
db_driver   = os.getenv("DB_DRIVER")   or "mysql+pymysql"       # Treiber: MySQL über PyMySQL
db_username = os.getenv("DB_USERNAME") or "root"                 # Datenbankbenutzer
db_password = os.getenv("DB_PASSWORD") or ""                     # Datenbankpasswort
db_host     = os.getenv("DB_HOST")     or "localhost"            # Adresse des Datenbankservers
db_port_str = os.getenv("DB_PORT")     or "3306"                 # Port (Standard bei MySQL: 3306)
db_name     = os.getenv("DB_NAME")     or "lernmaterialverwaltung"  # Name der Datenbank

# Baut die Verbindungs-URL für SQLAlchemy zusammen
# Format: mysql+pymysql://benutzer:passwort@host:port/datenbankname
mysql_url = URL.create(
    drivername=db_driver,
    username=db_username,
    password=db_password,
    host=db_host,
    port=int(db_port_str),  # Port muss als Zahl (int) übergeben werden, nicht als Text
    database=db_name
)

# Erstellt die Datenbankverbindung (Engine)
# Die Engine ist das zentrale Objekt für alle Datenbankoperationen
engine = create_engine(mysql_url)

# Erstellt eine Fabrik (Factory) für Datenbank-Sitzungen
# autocommit=False → Änderungen müssen manuell mit db.commit() gespeichert werden
# autoflush=False  → Daten werden nicht automatisch in die DB geschrieben
# bind=engine      → Verknüpft die Sitzungen mit unserer Datenbankverbindung
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Erstellt die Basis für das automatische Einlesen der Tabellenstruktur
# automap_base() erkennt Tabellen und ihre Beziehungen ohne manuelle Klassendefinitionen
Base = automap_base()
Base.prepare(autoload_with=engine)  # Verbindet sich mit der DB und liest alle Tabellen ein


# Direkte Python-Verweise auf die einzelnen Datenbanktabellen
# So können wir kurz "benutzer" schreiben statt "Base.classes.benutzer"
benutzer     = Base.classes.benutzer       # Tabelle: Benutzer (Lehrer, Azubi, Admin)
kategorie    = Base.classes.kategorie      # Tabelle: Kategorien für Materialien
kommentar    = Base.classes.kommentar      # Tabelle: Kommentare zu Materialien
material     = Base.classes.material       # Tabelle: Lernmaterialien (die eigentlichen Dateien)
material_tag = Base.classes.material_tag   # Tabelle: Verknüpfung zwischen Material und Tag (n:m)
tag          = Base.classes.tag            # Tabelle: Tags / Schlagwörter
themengebiet = Base.classes.themengebiet   # Tabelle: Themengebiete (z.B. "Python", "Netzwerk")
version      = Base.classes.version        # Tabelle: Versionshistorie von Materialien


def get_db():
    """
    Erstellt eine neue Datenbank-Sitzung und gibt sie zurück.

    Diese Funktion funktioniert als Generator (yield statt return):
      1. Eine neue Verbindung (Session) zur Datenbank wird geöffnet.
      2. Die Session wird an den Aufrufer weitergegeben (yield).
      3. Egal ob ein Fehler passiert oder nicht – die Session wird danach
         immer automatisch geschlossen (finally-Block).

    Verwendung:
        db = next(get_db())
        # oder in FastAPI als Dependency:
        # def route(db: Session = Depends(get_db)): ...
    """
    db = SessionLocal()   # Neue Datenbank-Sitzung öffnen
    try:
        yield db          # Sitzung an den Aufrufer weitergeben
    finally:
        db.close()        # Sitzung am Ende immer schließen – auch bei Fehlern