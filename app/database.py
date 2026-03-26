from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base

#mysql+pymysql://<username>:<password>@<host>:<port>/<database>
URL_DATABASE ="mysql+pymysql://auric:Nitondeauric%4015@82.165.20.39:3306/lernmaterialverwaltung"
engine = create_engine(URL_DATABASE,pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = automap_base()
Base.prepare(autoload_with=engine)

User = Base.classes.benutzer

