from pydantic import BaseModel
from enum import Enum
from typing import List


class RolleEnum(str, Enum):
    Admin = "Admin"
    Azubi = "Azubi"
    Lehrer = "Lehrer"


class UserBase(BaseModel):
    username: str
    email: str
    rolle: RolleEnum

    class Config:
        from_attributes = True
        use_enum_values = True


class Themen(BaseModel):
    name: str
    beschreibung: str

    class Config:
        from_attributes  = True

class Kategorie(BaseModel):
    name: str
    beschreibung: str


    class Config:
        from_attributes = True


class Tag(BaseModel):
    name: List[str]

    class Config:
        from_attributes = True

class MaterialBase(BaseModel):
    titel: str
    beschreibung: str
    themengebiet_id: int
    benutzer_id : int
    kategorie_id: int
    dateiname: str
    dateityp : str
    dateigroesse: int
    speicherort: str
    is_in_database: bool


    class Config:
        from_attributes = True

class MaterialSmall(MaterialBase):
    inhalt : bytes

class MaterialBig(MaterialBase):
     pass

class AnzahlMaterialProThemen(BaseModel):
    themengebiet_id: int
    anzahl:int
