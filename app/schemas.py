"""
Datenklassen (Schemas) für die CLI-Anwendung.

Diese Datei definiert einfache Python-Klassen, die die Struktur
unserer Datenobjekte beschreiben. Sie enthalten keine Datenbanklogik –
sie sind nur "Behälter" für Daten, die wir im Programm weitergeben.
"""


class User:
    """
    Repräsentiert einen Benutzer der Lernmaterialverwaltung.

    Ein Benutzer kann drei verschiedene Rollen haben:
      - 'Lehrer': Erstellt und verwaltet Materialien
      - 'Azubi': Kann Materialien ansehen und kommentieren
      - 'Admin': Hat vollen Zugriff auf alle Funktionen

    Attribute:
        id       (int): Eindeutige Nummer des Benutzers in der Datenbank
        username (str): Benutzername (z.B. "max.mustermann")
        email    (str): E-Mail-Adresse des Benutzers
        rolle    (str): Rolle des Benutzers: "Lehrer", "Azubi" oder "Admin"
    """
    def __init__(self, id, username, email, rolle):
        self.id       = id        # Eindeutige ID in der Datenbank
        self.username = username  # Benutzername für die Anmeldung
        self.email    = email     # E-Mail-Adresse des Benutzers
        self.rolle    = rolle     # Rolle: bestimmt die Berechtigungen


class Thema:
    """
    Repräsentiert ein Themengebiet.

    Themengebiete gruppieren Lernmaterialien nach ihrem fachlichen Inhalt,
    z.B. "Python-Programmierung", "Netzwerktechnik" oder "Datenbanken".

    Attribute:
        id           (int): Eindeutige Nummer des Themas
        name         (str): Name des Themengebiets (muss eindeutig sein)
        beschreibung (str): Kurze Erklärung des Themas (optional)
    """
    def __init__(self, id, name, beschreibung):
        self.id           = id           # Eindeutige ID in der Datenbank
        self.name         = name         # Name des Themengebiets
        self.beschreibung = beschreibung # Optionale Beschreibung des Themas


class Kategorie:
    """
    Repräsentiert eine Kategorie für Lernmaterialien.

    Kategorien helfen dabei, Materialien nach ihrer Art zu sortieren,
    z.B. "Präsentation", "Skript", "Aufgabenblatt" oder "Video".

    Attribute:
        id           (int): Eindeutige Nummer der Kategorie
        name         (str): Name der Kategorie (muss eindeutig sein)
        beschreibung (str): Kurze Erklärung der Kategorie (optional)
    """
    def __init__(self, id, name, beschreibung):
        self.id           = id           # Eindeutige ID in der Datenbank
        self.name         = name         # Name der Kategorie
        self.beschreibung = beschreibung # Optionale Beschreibung der Kategorie


class Tag:
    """
    Repräsentiert ein Tag (Schlagwort) für Materialien.

    Tags ermöglichen eine flexible Zuordnung von Schlüsselwörtern zu Materialien.
    Ein Material kann mehrere Tags haben, und ein Tag kann zu mehreren
    Materialien gehören (n:m-Beziehung über die Tabelle 'material_tag').

    Beispiele: "Python3", "Anfänger", "Übung", "LF8", "Klausur"

    Attribute:
        id   (int): Eindeutige Nummer des Tags
        name (str): Schlagwort (muss eindeutig sein)
    """
    def __init__(self, id, name):
        self.id   = id    # Eindeutige ID in der Datenbank
        self.name = name  # Schlagwort, z.B. "Python" oder "Anfänger"


class MaterialCount:
    """
    Speichert das Ergebnis einer Zählung: Name und Anzahl.

    Diese Hilfsklasse wird für Aggregationsabfragen verwendet.
    Sie speichert z.B. wie viele Materialien zu einem bestimmten
    Thema oder einer bestimmten Kategorie gehören.

    Beispiel:
        MaterialCount("Python", 5) → 5 Materialien im Thema "Python"

    Attribute:
        name   (str): Name des Themas, der Kategorie oder des Typs
        anzahl (int): Anzahl der zugehörigen Materialien
    """
    def __init__(self, name, anzahl):
        self.name   = name    # Name des gruppierten Eintrags
        self.anzahl = anzahl  # Wie viele Materialien in dieser Gruppe existieren
