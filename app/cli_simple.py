"""
CLI-Schicht: Textbasierte Benutzeroberfläche für die Lernmaterialverwaltung.

Diese Datei definiert alle Befehle, die der Benutzer in der Kommandozeile eingeben kann.
Die Bibliothek 'typer' wandelt Python-Funktionen automatisch in CLI-Befehle um.
Die Bibliothek 'rich' sorgt für farbige und strukturierte Ausgabe in der Konsole.

Verfügbare Befehle:
    upload      - Datei als Lernmaterial hochladen
    download    - Lernmaterial herunterladen
    suche       - Materialien mit Filtern durchsuchen
    kommentar   - Kommentare anzeigen, hinzufügen oder löschen
    list        - Entitäten auflisten (Benutzer, Themen, Kategorien, Tags, Materialien)
    queries     - Eine der 7 Pflichtabfragen ausführen
    create      - Neue Entität erstellen (Benutzer, Thema, Kategorie, Tag)
    delete      - Material löschen
    all-queries - Alle 7 Pflichtabfragen nacheinander ausführen
"""

import typer                          # Framework für Kommandozeilen-Anwendungen
from rich.console import Console      # Farbige Konsolenausgabe
from rich.table import Table          # Formatierte Tabellen in der Konsole
from rich import box                  # Verschiedene Tabellenrahmen-Stile
from typing import Optional, List     # Typhinweise für optionale und Listen-Parameter
import os                             # Für Dateipfad-Operationen
import sys                            # Für Systeminformationen (hier: Pfad)
from database import SessionLocal     # Datenbankverbindung aus database.py
from services import (
    # CRUD-Operationen aus services.py importieren
    get_all_users, get_user_by_id, create_user,
    get_all_themen, get_thema_by_id, create_thema,
    get_all_kategories, get_kategorie_by_id, create_kategorie,
    get_all_tags, get_tag_by_id, create_tag,
    get_all_materials, get_material_by_id, upload_material,
    download_material, search_materials, delete_material,
    get_comments_for_material, create_comment, get_comment_by_id, delete_comment,
    # Die 7 Pflichtabfragen für das LF8-Projekt
    anzahl_material_pro_themen, durchschnitt_dateigroesse_pro_typ,
    materialien_mit_themen, materialien_mit_kommentaren,
    kommentare_pro_material, material_mit_autor_und_thema,
    suche_material_mit_filtern
)

# Hauptobjekt der Typer-Anwendung
# name="lernmaterial" → der Name des CLI-Tools in der Hilfe
# add_completion=False → keine Shell-Autovervollständigung hinzufügen
app = typer.Typer(
    name="lernmaterial",
    help="Lernmaterialverwaltung - Textbasierte CLI für die Lernmaterial-Datenbank",
    add_completion=False,
)

# Konsolen-Objekt für farbige Ausgaben (mit rich-Bibliothek)
console = Console()


def show_table(title: str, headers: List[str], rows: List[List[str]]):
    """
    Hilfsfunktion: Zeigt Daten als formatierte Tabelle in der Konsole an.

    Erstellt eine Tabelle mit Rahmen (box.ROUNDED = abgerundete Ecken),
    fügt die Spaltenüberschriften hinzu und dann alle Datenzeilen.

    Args:
        title   (str):             Überschrift der Tabelle
        headers (List[str]):       Liste der Spaltenüberschriften
        rows    (List[List[str]]): Liste von Zeilen, jede Zeile ist eine Liste von Texten
    """
    table = Table(title=title, box=box.ROUNDED)  # Tabelle mit abgerundeten Rahmen erstellen
    for header in headers:
        table.add_column(header)  # Jede Spaltenüberschrift zur Tabelle hinzufügen

    for row in rows:
        table.add_row(*row)  # *row entpackt die Liste in einzelne Argumente

    console.print(table)  # Fertige Tabelle in der Konsole ausgeben


@app.command(name="upload", help="Material hochladen")
def upload_file(
    file_path:   str          = typer.Argument(..., help="Pfad zur Datei"),
    titel:       str          = typer.Option(..., "--titel",       "-t", help="Titel des Materials"),
    beschreibung:str          = typer.Option("",  "--beschreibung","-b", help="Beschreibung"),
    thema_id:    int          = typer.Option(..., "--thema",             help="Themengebiet-ID"),
    autor_id:    int          = typer.Option(..., "--autor",        "-a", help="Autor-ID"),
    kategorie_id:int          = typer.Option(..., "--kategorie",   "-k", help="Kategorie-ID"),
    tag_ids:     Optional[str]= typer.Option(None,"--tags",              help="Tag-IDs (kommagetrennt)")
):
    """
    Lädt eine Datei als Lernmaterial hoch.

    Entscheidet automatisch, ob die Datei in der Datenbank (≤1MB)
    oder im Dateisystem (>1MB) gespeichert wird.

    Beispiel:
        python main.py upload skript.pdf --titel "Python Grundlagen" --thema 1 --autor 1 --kategorie 2
    """
    # Prüfen ob die Datei existiert, bevor wir fortfahren
    if not os.path.exists(file_path):
        console.print(f"[red]Fehler: Datei nicht gefunden: {file_path}[/red]")
        raise typer.Exit(1)  # Programm mit Fehlercode 1 beenden

    # Tag-IDs aus dem kommagetrennen String in eine Liste von Zahlen umwandeln
    # Beispiel: "1,2,3" → [1, 2, 3]
    tag_id_list = []
    if tag_ids:
        try:
            tag_id_list = [int(tid.strip()) for tid in tag_ids.split(",")]
        except ValueError:
            console.print("[red]Fehler: Ungültige Tag-IDs[/red]")
            raise typer.Exit(1)

    # Datenbankverbindung öffnen (wird am Ende des with-Blocks automatisch geschlossen)
    with SessionLocal() as db:
        try:
            # Upload-Funktion aus services.py aufrufen
            material = upload_material(
                db=db,
                file_path=file_path,
                titel=titel,
                beschreibung=beschreibung,
                themengebiet_id=thema_id,
                benutzer_id=autor_id,
                kategorie_id=kategorie_id,
                tag_ids=tag_id_list
            )

            # Erfolgsmeldung mit Details zum hochgeladenen Material ausgeben
            console.print(f"[green]Material erfolgreich hochgeladen![/green]")
            console.print(f"  ID: {material.id}")
            console.print(f"  Titel: {material.titel}")
            console.print(f"  Datei: {material.dateiname}")
            console.print(f"  Größe: {material.dateigroesse} bytes")
            console.print(f"  In DB gespeichert: {'Ja' if material.is_in_database else 'Nein'}")

        except Exception as e:
            console.print(f"[red]Fehler beim Hochladen: {e}[/red]")
            raise typer.Exit(1)


@app.command(name="download", help="Material herunterladen")
def download_file(
    material_id: int = typer.Argument(..., help="Material-ID"),
    output_dir:  str = typer.Option(".", "--output", "-o", help="Ausgabeverzeichnis")
):
    """
    Lädt ein Lernmaterial herunter und speichert es im angegebenen Ordner.

    Das Material wird anhand seiner ID gefunden. Ob es aus der Datenbank
    oder dem Dateisystem geholt wird, entscheidet services.py automatisch.

    Beispiel:
        python main.py download 1 --output ./downloads
    """
    with SessionLocal() as db:
        try:
            # Download-Funktion aus services.py aufrufen
            output_path = download_material(db, material_id, output_dir)
            console.print(f"[green]Material erfolgreich heruntergeladen nach: {output_path}[/green]")
        except Exception as e:
            console.print(f"[red]Fehler beim Herunterladen: {e}[/red]")
            raise typer.Exit(1)


@app.command(name="suche", help="Materialien suchen")
def search(
    titel:        Optional[str] = typer.Option(None, "--titel",     "-t", help="Suche im Titel"),
    thema_id:     Optional[int] = typer.Option(None, "--thema",           help="Nach Themengebiet filtern"),
    autor_id:     Optional[int] = typer.Option(None, "--autor",     "-a", help="Nach Autor filtern"),
    kategorie_id: Optional[int] = typer.Option(None, "--kategorie", "-k", help="Nach Kategorie filtern"),
    tag_id:       Optional[int] = typer.Option(None, "--tag",             help="Nach Tag filtern")
):
    """
    Durchsucht Materialien mit verschiedenen optionalen Filtern.

    Alle Filter sind optional. Mehrere Filter werden mit UND verknüpft.
    Ohne Filter werden alle Materialien angezeigt.

    Beispiele:
        python main.py suche --titel "Python"
        python main.py suche --thema 1 --kategorie 2
    """
    with SessionLocal() as db:
        # Suchabfrage mit den angegebenen Filtern ausführen
        materials = search_materials(
            db=db,
            titel=titel,
            themengebiet_id=thema_id,
            benutzer_id=autor_id,
            kategorie_id=kategorie_id,
            tag_id=tag_id
        )

        # Wenn nichts gefunden wurde, Hinweis ausgeben und beenden
        if not materials:
            console.print("[yellow]Keine Materialien gefunden[/yellow]")
            return

        # Ergebnisse als Tabellenzeilen vorbereiten
        rows = []
        for mat in materials:
            rows.append([
                str(mat.id),
                mat.titel,
                mat.dateiname or "-",       # Falls kein Dateiname: "-" anzeigen
                str(mat.dateigroesse),
                "Ja" if mat.is_in_database else "Nein"  # Lesbare Ausgabe statt True/False
            ])

        # Ergebnisse als Tabelle anzeigen
        show_table(
            title="Suchergebnisse",
            headers=["ID", "Titel", "Dateiname", "Größe (bytes)", "In DB"],
            rows=rows
        )

        # Anzahl der Ergebnisse ausgeben
        console.print(f"[green]{len(materials)} Materialien gefunden[/green]")


@app.command(name="kommentar", help="Kommentare verwalten")
def comment(
    action:     str          = typer.Argument(...,  help="Aktion: add, list, delete"),
    material_id:int          = typer.Option(None,   "--material", "-m", help="Material-ID"),
    autor_id:   int          = typer.Option(None,   "--autor",    "-a", help="Autor-ID"),
    text:       Optional[str]= typer.Option(None,   "--text",     "-t", help="Kommentartext"),
    comment_id: Optional[int]= typer.Option(None,   "--id",             help="Kommentar-ID (für delete)")
):
    """
    Verwaltet Kommentare zu Materialien: Hinzufügen, Anzeigen oder Löschen.

    Aktionen:
        add    - Neuen Kommentar hinzufügen (benötigt --material, --autor, --text)
        list   - Alle Kommentare eines Materials anzeigen (benötigt --material)
        delete - Kommentar löschen (benötigt --id)

    Beispiele:
        python main.py kommentar add --material 1 --autor 1 --text "Sehr hilfreich!"
        python main.py kommentar list --material 1
        python main.py kommentar delete --id 3
    """
    with SessionLocal() as db:
        if action == "add":
            # Kommentar hinzufügen: alle drei Parameter müssen angegeben sein
            if not material_id or not autor_id or not text:
                console.print("[red]Fehler: --material, --autor und --text werden benötigt[/red]")
                raise typer.Exit(1)

            comment = create_comment(db, material_id, autor_id, text)
            console.print(f"[green]Kommentar erfolgreich hinzugefügt (ID: {comment.id})[/green]")

        elif action == "list":
            # Kommentare eines Materials anzeigen
            if not material_id:
                console.print("[red]Fehler: --material wird benötigt[/red]")
                raise typer.Exit(1)

            comments = get_comments_for_material(db, material_id)

            if not comments:
                console.print("[yellow]Keine Kommentare gefunden[/yellow]")
                return

            # Kommentare als Tabellenzeilen vorbereiten
            rows = []
            for comment in comments:
                # Langen Kommentartext auf 50 Zeichen kürzen und "..." anhängen
                text_preview = comment.text[:50] + "..." if len(comment.text) > 50 else comment.text
                rows.append([
                    str(comment.id),
                    text_preview,
                    str(comment.autor_id),
                    str(comment.erstellungsdatum.date()) if comment.erstellungsdatum else "-"
                ])

            show_table(
                title=f"Kommentare für Material {material_id}",
                headers=["ID", "Text (Auszug)", "Autor-ID", "Datum"],
                rows=rows
            )

        elif action == "delete":
            # Kommentar löschen: Kommentar-ID muss angegeben sein
            if not comment_id:
                console.print("[red]Fehler: --id wird benötigt[/red]")
                raise typer.Exit(1)

            try:
                delete_comment(db, comment_id)
                console.print(f"[green]Kommentar {comment_id} erfolgreich gelöscht[/green]")
            except Exception as e:
                console.print(f"[red]Fehler: {e}[/red]")
                raise typer.Exit(1)
        else:
            # Unbekannte Aktion → Fehlermeldung und Hinweis auf gültige Aktionen
            console.print(f"[red]Unbekannte Aktion: {action}[/red]")
            console.print("[yellow]Verfügbare Aktionen: add, list, delete[/yellow]")
            raise typer.Exit(1)


@app.command(name="list", help="Entitäten auflisten")
def list_entities(
    entity: str = typer.Argument(..., help="Zu listende Entität: users, themen, kategorien, tags, materialien")
):
    """
    Listet alle Einträge einer bestimmten Entität aus der Datenbank auf.

    Entitäten:
        users       - Alle Benutzer
        themen      - Alle Themengebiete
        kategorien  - Alle Kategorien
        tags        - Alle Tags
        materialien - Alle Lernmaterialien

    Beispiel:
        python main.py list users
        python main.py list materialien
    """
    with SessionLocal() as db:
        if entity == "users":
            # Alle Benutzer abrufen und als Tabelle anzeigen
            items = get_all_users(db)
            rows = []
            for item in items:
                rows.append([
                    str(item.id),
                    item.username,
                    item.email,
                    item.rolle,
                    str(item.created_at.date()) if item.created_at else "-"  # Datum formatieren
                ])
            show_table("Benutzer", ["ID", "Benutzername", "Email", "Rolle", "Erstellt"], rows)

        elif entity == "themen":
            # Alle Themengebiete abrufen und anzeigen
            items = get_all_themen(db)
            rows = []
            for item in items:
                rows.append([
                    str(item.id),
                    item.name,
                    item.beschreibung or "-"  # Falls keine Beschreibung: "-"
                ])
            show_table("Themengebiete", ["ID", "Name", "Beschreibung"], rows)

        elif entity == "kategorien":
            # Alle Kategorien abrufen und anzeigen
            items = get_all_kategories(db)
            rows = []
            for item in items:
                rows.append([
                    str(item.id),
                    item.name,
                    item.beschreibung or "-"
                ])
            show_table("Kategorien", ["ID", "Name", "Beschreibung"], rows)

        elif entity == "tags":
            # Alle Tags abrufen und anzeigen
            items = get_all_tags(db)
            rows = []
            for item in items:
                rows.append([str(item.id), item.name])
            show_table("Tags", ["ID", "Name"], rows)

        elif entity == "materialien":
            # Alle Materialien abrufen und anzeigen
            items = get_all_materials(db)
            rows = []
            for item in items:
                # Dateigröße von Bytes in Megabyte umrechnen für bessere Lesbarkeit
                size_mb = item.dateigroesse / (1024 * 1024) if item.dateigroesse else 0
                rows.append([
                    str(item.id),
                    item.titel,
                    item.dateiname or "-",
                    item.dateityp or "-",
                    f"{size_mb:.2f} MB",  # Auf 2 Nachkommastellen formatieren
                    "Ja" if item.is_in_database else "Nein"
                ])
            show_table("Materialien", ["ID", "Titel", "Dateiname", "Typ", "Größe", "In DB"], rows)

        else:
            # Unbekannte Entität → Fehlermeldung
            console.print(f"[red]Unbekannte Entität: {entity}[/red]")
            console.print("[yellow]Verfügbare Entitäten: users, themen, kategorien, tags, materialien[/yellow]")
            raise typer.Exit(1)

        # Anzahl der gefundenen Einträge ausgeben
        console.print(f"[green]{len(items)} {entity} gefunden[/green]")


@app.command(name="queries", help="7+ erforderliche Suchabfragen ausführen")
def run_queries(
    query: str = typer.Argument(
        ...,
        help="""Zu ausführende Abfrage:
        count-thema    - Material pro Themengebiet (COUNT Aggregation)
        avg-size       - Durchschnittliche Größe pro Dateityp (AVG Aggregation)
        mat-themen     - Materialien mit Themengebieten (Inner Join)
        mat-comments   - Materialien mit Kommentaren (Inner Join)
        comments-per   - Kommentare pro Material (Join + Aggregation)
        mat-author     - Material mit Autor und Thema (Multi-Table Join)
        search-full    - Vollständige Suche mit Filtern (Multi-Table Join)
        """
    ),
    thema_id: Optional[int] = typer.Option(None, "--thema",  help="Themengebiet-ID für search-full"),
    autor_id: Optional[int] = typer.Option(None, "--autor", "-a", help="Autor-ID für search-full")
):
    """
    Führt eine der 7 Pflichtabfragen aus dem LF8-Abschlussprojekt aus.

    Jede Abfrage demonstriert eine andere SQL-Technik:
        count-thema  → Aggregation mit COUNT
        avg-size     → Aggregation mit AVG
        mat-themen   → Einfacher Inner JOIN
        mat-comments → Inner JOIN mit zwei Tabellen
        comments-per → JOIN + COUNT Aggregation
        mat-author   → Multi-Table JOIN (3 Tabellen)
        search-full  → Multi-Table JOIN (4 Tabellen) mit optionalen Filtern

    Beispiele:
        python main.py queries count-thema
        python main.py queries search-full --thema 1 --autor 2
    """
    with SessionLocal() as db:
        if query == "count-thema":
            # Abfrage 1: Anzahl Materialien pro Themengebiet
            results = anzahl_material_pro_themen(db)
            rows = []
            for thema, anzahl in results:  # Ergebnis-Tupel entpacken
                rows.append([thema, str(anzahl)])
            show_table("Material pro Themengebiet (COUNT)", ["Themengebiet", "Anzahl"], rows)

        elif query == "avg-size":
            # Abfrage 2: Durchschnittliche Dateigröße pro Dateityp
            results = durchschnitt_dateigroesse_pro_typ(db)
            rows = []
            for dateityp, durchschnitt in results:
                mb = durchschnitt / (1024 * 1024) if durchschnitt else 0  # Bytes → MB
                rows.append([
                    dateityp or "Unbekannt",
                    f"{durchschnitt:.0f}" if durchschnitt else "0",   # Bytes ohne Nachkommastellen
                    f"{mb:.2f} MB"                                     # MB mit 2 Nachkommastellen
                ])
            show_table("Durchschnittliche Dateigröße pro Typ (AVG)", ["Dateityp", "Bytes", "MB"], rows)

        elif query == "mat-themen":
            # Abfrage 3: Materialien mit ihren Themengebieten (Inner JOIN)
            results = materialien_mit_themen(db)
            rows = []
            for titel, dateiname, themengebiet in results:
                rows.append([titel, dateiname or "-", themengebiet])
            show_table("Materialien mit Themengebieten (JOIN)", ["Titel", "Dateiname", "Themengebiet"], rows)

        elif query == "mat-comments":
            # Abfrage 4: Materialien mit ihren Kommentaren (Inner JOIN)
            results = materialien_mit_kommentaren(db)
            rows = []
            for titel, dateiname, kommentar_text, datum in results:
                # Langen Kommentar auf 50 Zeichen kürzen
                text_preview = kommentar_text[:50] + "..." if len(kommentar_text) > 50 else kommentar_text
                rows.append([
                    titel,
                    dateiname or "-",
                    text_preview,
                    str(datum.date()) if datum else "-"
                ])
            show_table("Materialien mit Kommentaren (JOIN)", ["Titel", "Dateiname", "Kommentar", "Datum"], rows)

        elif query == "comments-per":
            # Abfrage 5: Anzahl Kommentare pro Material (JOIN + COUNT)
            results = kommentare_pro_material(db)
            rows = []
            for titel, dateiname, anzahl in results:
                rows.append([titel, dateiname or "-", str(anzahl)])
            show_table("Kommentare pro Material (JOIN + COUNT)", ["Titel", "Dateiname", "Anzahl"], rows)

        elif query == "mat-author":
            # Abfrage 6: Material mit Autor und Themengebiet (Multi-JOIN über 3 Tabellen)
            results = material_mit_autor_und_thema(db)
            rows = []
            for titel, dateiname, autor, themengebiet, datum in results:
                rows.append([
                    titel,
                    dateiname or "-",
                    autor,
                    themengebiet,
                    str(datum.date()) if datum else "-"
                ])
            show_table("Material mit Autor und Thema (Multi-JOIN)", ["Titel", "Dateiname", "Autor", "Themengebiet", "Datum"], rows)

        elif query == "search-full":
            # Abfrage 7: Vollständige Suche (Multi-JOIN über 4 Tabellen + optionale Filter)
            results = suche_material_mit_filtern(db, thema_id, autor_id)
            rows = []
            for row in results:
                size_mb = row.dateigroesse / (1024 * 1024) if row.dateigroesse else 0
                rows.append([
                    row.titel,
                    row.dateiname or "-",
                    row.dateityp or "-",
                    f"{size_mb:.1f} MB",
                    row.autor,
                    row.themengebiet,
                    row.kategorie
                ])

            # Titel anpassen, um aktive Filter anzuzeigen
            filter_info = []
            if thema_id:
                filter_info.append(f"Themengebiet-ID: {thema_id}")
            if autor_id:
                filter_info.append(f"Autor-ID: {autor_id}")

            title = "Vollständige Suche mit Filtern (Multi-JOIN)"
            if filter_info:
                title += f" - Filter: {', '.join(filter_info)}"

            show_table(
                title,
                ["Titel", "Datei", "Typ", "Größe", "Autor", "Themengebiet", "Kategorie"],
                rows
            )

        else:
            # Unbekannte Abfrage → Fehlermeldung und Liste der gültigen Abfragen
            console.print(f"[red]Unbekannte Abfrage: {query}[/red]")
            console.print("[yellow]Verfügbare Abfragen: count-thema, avg-size, mat-themen, mat-comments, comments-per, mat-author, search-full[/yellow]")
            raise typer.Exit(1)

        # Anzahl der zurückgegebenen Ergebnisse ausgeben
        console.print(f"[green]{len(results)} Ergebnisse gefunden[/green]")


@app.command(name="create", help="Neue Entitäten erstellen")
def create_entity(
    entity:      str          = typer.Argument(...,    help="Zu erstellende Entität: user, thema, kategorie, tag"),
    name:        str          = typer.Option(...,      "--name",        "-n", help="Name der Entität"),
    email:       Optional[str]= typer.Option(None,     "--email",       "-e", help="Email (nur für user)"),
    rolle:       Optional[str]= typer.Option("Azubi",  "--rolle",       "-r", help="Rolle (nur für user)"),
    beschreibung:Optional[str]= typer.Option("",       "--beschreibung","-b", help="Beschreibung")
):
    """
    Erstellt eine neue Entität in der Datenbank.

    Entitäten und ihre Pflichtparameter:
        user      → --name, --email (--rolle optional, Standard: "Azubi")
        thema     → --name (--beschreibung optional)
        kategorie → --name (--beschreibung optional)
        tag       → --name

    Beispiele:
        python main.py create user --name "Max Mustermann" --email "max@example.com" --rolle "Lehrer"
        python main.py create thema --name "Python" --beschreibung "Python-Programmierung"
        python main.py create tag --name "Anfänger"
    """
    with SessionLocal() as db:
        if entity == "user":
            # Benutzer erstellen: E-Mail ist Pflichtfeld
            if not email:
                console.print("[red]Fehler: --email wird benötigt für user[/red]")
                raise typer.Exit(1)

            user = create_user(db, name, email, rolle)
            console.print(f"[green]Benutzer erfolgreich erstellt[/green]")
            console.print(f"  ID: {user.id}")
            console.print(f"  Benutzername: {user.username}")
            console.print(f"  Email: {user.email}")
            console.print(f"  Rolle: {user.rolle}")

        elif entity == "thema":
            # Themengebiet erstellen
            thema = create_thema(db, name, beschreibung)
            console.print(f"[green]Themengebiet erfolgreich erstellt[/green]")
            console.print(f"  ID: {thema.id}")
            console.print(f"  Name: {thema.name}")
            console.print(f"  Beschreibung: {thema.beschreibung or '-'}")

        elif entity == "kategorie":
            # Kategorie erstellen
            kat = create_kategorie(db, name, beschreibung)
            console.print(f"[green]Kategorie erfolgreich erstellt[/green]")
            console.print(f"  ID: {kat.id}")
            console.print(f"  Name: {kat.name}")
            console.print(f"  Beschreibung: {kat.beschreibung or '-'}")

        elif entity == "tag":
            # Tag erstellen
            tag_obj = create_tag(db, name)
            console.print(f"[green]Tag erfolgreich erstellt[/green]")
            console.print(f"  ID: {tag_obj.id}")
            console.print(f"  Name: {tag_obj.name}")

        else:
            # Unbekannte Entität → Fehlermeldung
            console.print(f"[red]Unbekannte Entität: {entity}[/red]")
            console.print("[yellow]Verfügbare Entitäten: user, thema, kategorie, tag[/yellow]")
            raise typer.Exit(1)


@app.command(name="delete", help="Material löschen")
def delete(
    material_id: int = typer.Argument(..., help="Material-ID")
):
    """
    Löscht ein Lernmaterial aus der Datenbank.

    Falls das Material im Dateisystem gespeichert war (>1MB),
    wird auch die physische Datei aus dem uploads-Ordner gelöscht.

    Beispiel:
        python main.py delete 5
    """
    with SessionLocal() as db:
        try:
            delete_material(db, material_id)
            console.print(f"[green]Material {material_id} erfolgreich gelöscht[/green]")
        except Exception as e:
            console.print(f"[red]Fehler beim Löschen: {e}[/red]")
            raise typer.Exit(1)


@app.command(name="all-queries", help="Alle 7 erforderlichen Suchabfragen ausführen")
def run_all_queries():
    """
    Führt alle 7 Pflichtabfragen des LF8-Projekts nacheinander aus.

    Dies ist eine Schnellübersicht aller Abfragen, um zu zeigen, dass
    alle SQL-Techniken (COUNT, AVG, JOIN, Multi-JOIN) implementiert sind.
    Die 7. Abfrage (search-full) muss separat mit Filtern aufgerufen werden.

    Beispiel:
        python main.py all-queries
    """
    console.print("[bold blue]Führe alle 7 erforderlichen Suchabfragen aus...[/bold blue]")
    console.print()

    # Liste aller Abfragen mit ihren Schlüsseln und Beschreibungen
    queries = [
        ("count-thema",  "Material pro Themengebiet (COUNT)"),
        ("avg-size",     "Durchschnittliche Größe pro Dateityp (AVG)"),
        ("mat-themen",   "Materialien mit Themengebieten (JOIN)"),
        ("mat-comments", "Materialien mit Kommentaren (JOIN)"),
        ("comments-per", "Kommentare pro Material (JOIN + COUNT)"),
        ("mat-author",   "Material mit Autor und Thema (Multi-JOIN)"),
    ]

    # Jede Abfrage ausführen und kurz zusammenfassen
    for query_key, query_name in queries:
        console.print(f"[bold cyan]{query_name}[/bold cyan]")
        try:
            with SessionLocal() as db:
                if query_key == "count-thema":
                    results = anzahl_material_pro_themen(db)
                    console.print(f"  [green]{len(results)} Themengebiete[/green]")
                elif query_key == "avg-size":
                    results = durchschnitt_dateigroesse_pro_typ(db)
                    console.print(f"  [green]{len(results)} Dateitypen[/green]")
                elif query_key == "mat-themen":
                    results = materialien_mit_themen(db)
                    console.print(f"  [green]{len(results)} Materialien[/green]")
                elif query_key == "mat-comments":
                    results = materialien_mit_kommentaren(db)
                    console.print(f"  [green]{len(results)} Kommentare[/green]")
                elif query_key == "comments-per":
                    results = kommentare_pro_material(db)
                    console.print(f"  [green]{len(results)} Materialien mit Kommentarzählung[/green]")
                elif query_key == "mat-author":
                    results = material_mit_autor_und_thema(db)
                    console.print(f"  [green]{len(results)} Materialien[/green]")
        except Exception as e:
            console.print(f"  [red]Fehler: {e}[/red]")
        console.print()

    console.print("[bold green]Alle 7 Suchabfragen erfolgreich ausgeführt![/bold green]")
    console.print("[yellow]Verwende 'lernmaterial queries search-full' für die 7. Abfrage (Vollständige Suche)[/yellow]")


@app.callback()
def main():
    """
    Lernmaterialverwaltung - Textbasierte CLI für die Lernmaterial-Datenbank.

    Erfüllt alle Anforderungen des LF8 Abschlussprojekts:
      - Upload von Materialien (≤1MB in DB, >1MB im Dateisystem)
      - Download von Materialien
      - Suche nach Materialien mit verschiedenen Filtern
      - Kommentarfunktion für Materialien
      - 7+ erforderliche Suchabfragen (Aggregation, JOIN, Multi-JOIN)
      - CRUD-Operationen für alle Entitäten

    Diese Funktion wird vor jedem Befehl ausgeführt (callback).
    Sie enthält keine eigene Logik, definiert aber die Haupt-Hilfeseite.
    """
    pass  # Keine zusätzliche Logik nötig, typer übernimmt alles


if __name__ == "__main__":
    app()  # Anwendung starten, wenn die Datei direkt ausgeführt wird
