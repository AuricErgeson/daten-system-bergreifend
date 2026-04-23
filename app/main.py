import os
from rich.console import Console
from rich.table import Table
from rich import box
from database import SessionLocal
from services import (
    get_all_users, create_user,
    get_all_themen, create_thema,
    get_all_kategories, create_kategorie,
    get_all_tags, create_tag,
    get_all_materials, upload_material, download_material,
    search_materials, delete_material,
    get_comments_for_material, create_comment, delete_comment,
    anzahl_material_pro_themen, durchschnitt_dateigroesse_pro_typ,
    materialien_mit_themen, materialien_mit_kommentaren,
    kommentare_pro_material, material_mit_autor_und_thema,
    suche_material_mit_filtern
)

console = Console()


def linie():
    print("─" * 50)


def zeige_tabelle(titel, spalten, zeilen):
    tabelle = Table(title=titel, box=box.ROUNDED)
    for s in spalten:
        tabelle.add_column(s)
    for z in zeilen:
        tabelle.add_row(*z)
    console.print(tabelle)


def waehle_aus_liste(eintraege, anzeige_fn):
    if not eintraege:
        console.print("[yellow]Keine Einträge vorhanden.[/yellow]")
        return None
    for i, e in enumerate(eintraege, 1):
        print(f"  [{i}] {anzeige_fn(e)}")
    eingabe = input("Auswahl: ").strip()
    try:
        index = int(eingabe) - 1
        if 0 <= index < len(eintraege):
            return eintraege[index]
    except ValueError:
        pass
    console.print("[red]Ungültige Auswahl.[/red]")
    return None


def upload_menu():
    console.print("\n[bold cyan]── MATERIAL HOCHLADEN ──[/bold cyan]")
    linie()

    datei_pfad = input("Pfad zur Datei: ").strip()
    if not os.path.exists(datei_pfad):
        console.print(f"[red]Datei nicht gefunden: {datei_pfad}[/red]")
        return

    titel = input("Titel: ").strip()
    if not titel:
        console.print("[red]Titel darf nicht leer sein.[/red]")
        return

    beschreibung = input("Beschreibung (optional): ").strip()

    with SessionLocal() as db:
        console.print("\n[bold]Themengebiet:[/bold]")
        thema = waehle_aus_liste(get_all_themen(db), lambda t: t.name)
        if not thema:
            return

        console.print("\n[bold]Autor:[/bold]")
        autor = waehle_aus_liste(get_all_users(db), lambda u: f"{u.username} ({u.rolle})")
        if not autor:
            return

        console.print("\n[bold]Kategorie:[/bold]")
        kat = waehle_aus_liste(get_all_kategories(db), lambda k: k.name)
        if not kat:
            return

        tag_ids = []
        tags = get_all_tags(db)
        if tags:
            console.print("\n[bold]Tags (optional):[/bold]")
            for i, t in enumerate(tags, 1):
                print(f"  [{i}] {t.name}")
            tag_eingabe = input("Nummern kommagetrennt (Enter = keine): ").strip()
            if tag_eingabe:
                try:
                    nummern = [int(x.strip()) - 1 for x in tag_eingabe.split(",")]
                    tag_ids = [tags[n].id for n in nummern if 0 <= n < len(tags)]
                except ValueError:
                    pass

        try:
            mat = upload_material(
                db=db,
                file_path=datei_pfad,
                titel=titel,
                beschreibung=beschreibung,
                themengebiet_id=thema.id,
                benutzer_id=autor.id,
                kategorie_id=kat.id,
                tag_ids=tag_ids
            )
            linie()
            console.print(f"[bold green]Upload erfolgreich![/bold green]")
            console.print(f"  ID: {mat.id}  |  {mat.dateiname}  |  {mat.dateigroesse:,} Bytes")
            console.print(f"  Gespeichert in: {'Datenbank' if mat.is_in_database else 'Dateisystem'}")
        except Exception as e:
            console.print(f"[red]Fehler: {e}[/red]")


def download_menu():
    console.print("\n[bold cyan]── MATERIAL HERUNTERLADEN ──[/bold cyan]")
    linie()

    with SessionLocal() as db:
        materialien = get_all_materials(db)
        if not materialien:
            console.print("[yellow]Keine Materialien vorhanden.[/yellow]")
            return

        zeilen = []
        for m in materialien:
            mb = m.dateigroesse / (1024 * 1024) if m.dateigroesse else 0
            zeilen.append([str(m.id), m.titel, m.dateiname or "-", f"{mb:.2f} MB"])
        zeige_tabelle("Materialien", ["ID", "Titel", "Dateiname", "Größe"], zeilen)

        mat_id = input("\nMaterial-ID: ").strip()
        try:
            mat_id = int(mat_id)
        except ValueError:
            console.print("[red]Ungültige ID.[/red]")
            return

        ausgabe = input("Zielordner (Enter = aktueller Ordner): ").strip() or "."
        if ausgabe != "." and not os.path.exists(ausgabe):
            os.makedirs(ausgabe)

        try:
            pfad = download_material(db, mat_id, ausgabe)
            console.print(f"[bold green]Gespeichert unter: {pfad}[/bold green]")
        except Exception as e:
            console.print(f"[red]Fehler: {e}[/red]")


def suche_menu():
    console.print("\n[bold cyan]── MATERIALIEN SUCHEN ──[/bold cyan]")
    linie()

    titel_filter = input("Titelsuche (Enter = alle): ").strip() or None
    thema_id = None
    autor_id = None

    with SessionLocal() as db:
        if input("Nach Thema filtern? (j/n): ").strip().lower() == "j":
            console.print("\n[bold]Themengebiet:[/bold]")
            thema = waehle_aus_liste(get_all_themen(db), lambda t: t.name)
            if thema:
                thema_id = thema.id

        if input("Nach Autor filtern? (j/n): ").strip().lower() == "j":
            console.print("\n[bold]Autor:[/bold]")
            autor = waehle_aus_liste(get_all_users(db), lambda u: u.username)
            if autor:
                autor_id = autor.id

        ergebnisse = search_materials(db, titel=titel_filter, themengebiet_id=thema_id, benutzer_id=autor_id)
        linie()

        if not ergebnisse:
            console.print("[yellow]Keine Materialien gefunden.[/yellow]")
            return

        zeilen = []
        for m in ergebnisse:
            mb = m.dateigroesse / (1024 * 1024) if m.dateigroesse else 0
            zeilen.append([str(m.id), m.titel, m.dateiname or "-", m.dateityp or "-", f"{mb:.2f} MB"])
        zeige_tabelle("Suchergebnisse", ["ID", "Titel", "Dateiname", "Typ", "Größe"], zeilen)
        console.print(f"[green]{len(ergebnisse)} Ergebnis(se)[/green]")


def loeschen_menu():
    console.print("\n[bold cyan]── MATERIAL LÖSCHEN ──[/bold cyan]")
    linie()

    with SessionLocal() as db:
        materialien = get_all_materials(db)
        if not materialien:
            console.print("[yellow]Keine Materialien vorhanden.[/yellow]")
            return

        zeilen = [[str(m.id), m.titel, m.dateiname or "-"] for m in materialien]
        zeige_tabelle("Materialien", ["ID", "Titel", "Dateiname"], zeilen)

        mat_id = input("\nMaterial-ID zum Löschen: ").strip()
        try:
            mat_id = int(mat_id)
        except ValueError:
            console.print("[red]Ungültige ID.[/red]")
            return

        if input(f"Material {mat_id} löschen? (j/n): ").strip().lower() != "j":
            console.print("[yellow]Abgebrochen.[/yellow]")
            return

        try:
            delete_material(db, mat_id)
            console.print(f"[bold green]Material {mat_id} gelöscht.[/bold green]")
        except Exception as e:
            console.print(f"[red]Fehler: {e}[/red]")


def kommentar_menu():
    while True:
        console.print("\n[bold cyan]── KOMMENTARE ──[/bold cyan]")
        print("  [1] Kommentare anzeigen")
        print("  [2] Kommentar hinzufügen")
        print("  [3] Kommentar löschen")
        print("  [0] Zurück")
        linie()
        wahl = input("Auswahl: ").strip()

        if wahl == "0":
            break
        elif wahl == "1":
            mat_id = input("Material-ID: ").strip()
            try:
                mat_id = int(mat_id)
            except ValueError:
                console.print("[red]Ungültige ID.[/red]")
                continue
            with SessionLocal() as db:
                kommentare = get_comments_for_material(db, mat_id)
                if not kommentare:
                    console.print("[yellow]Keine Kommentare.[/yellow]")
                    continue
                zeilen = []
                for k in kommentare:
                    vorschau = k.text[:60] + "..." if len(k.text) > 60 else k.text
                    datum = str(k.erstellungsdatum.date()) if k.erstellungsdatum else "-"
                    zeilen.append([str(k.id), vorschau, str(k.autor_id), datum])
                zeige_tabelle(f"Kommentare für Material {mat_id}", ["ID", "Text", "Autor-ID", "Datum"], zeilen)

        elif wahl == "2":
            try:
                mat_id  = int(input("Material-ID: ").strip())
                autor_id = int(input("Autor-ID: ").strip())
            except ValueError:
                console.print("[red]Ungültige ID.[/red]")
                continue
            text = input("Kommentartext: ").strip()
            if not text:
                console.print("[red]Text darf nicht leer sein.[/red]")
                continue
            with SessionLocal() as db:
                try:
                    k = create_comment(db, mat_id, autor_id, text)
                    console.print(f"[bold green]Kommentar hinzugefügt (ID: {k.id})[/bold green]")
                except Exception as e:
                    console.print(f"[red]Fehler: {e}[/red]")

        elif wahl == "3":
            try:
                k_id = int(input("Kommentar-ID: ").strip())
            except ValueError:
                console.print("[red]Ungültige ID.[/red]")
                continue
            with SessionLocal() as db:
                try:
                    delete_comment(db, k_id)
                    console.print(f"[bold green]Kommentar {k_id} gelöscht.[/bold green]")
                except Exception as e:
                    console.print(f"[red]Fehler: {e}[/red]")
        else:
            console.print("[red]Ungültige Eingabe.[/red]")


def listen_menu():
    while True:
        console.print("\n[bold cyan]── LISTEN ──[/bold cyan]")
        print("  [1] Materialien")
        print("  [2] Benutzer")
        print("  [3] Themengebiete")
        print("  [4] Kategorien")
        print("  [5] Tags")
        print("  [0] Zurück")
        linie()
        wahl = input("Auswahl: ").strip()

        if wahl == "0":
            break

        with SessionLocal() as db:
            if wahl == "1":
                eintraege = get_all_materials(db)
                zeilen = []
                for m in eintraege:
                    mb = m.dateigroesse / (1024 * 1024) if m.dateigroesse else 0
                    zeilen.append([str(m.id), m.titel, m.dateiname or "-", m.dateityp or "-", f"{mb:.2f} MB", "Ja" if m.is_in_database else "Nein"])
                zeige_tabelle("Materialien", ["ID", "Titel", "Dateiname", "Typ", "Größe", "In DB"], zeilen)
            elif wahl == "2":
                zeilen = [[str(u.id), u.username, u.email, u.rolle] for u in get_all_users(db)]
                zeige_tabelle("Benutzer", ["ID", "Benutzername", "Email", "Rolle"], zeilen)
            elif wahl == "3":
                zeilen = [[str(t.id), t.name, t.beschreibung or "-"] for t in get_all_themen(db)]
                zeige_tabelle("Themengebiete", ["ID", "Name", "Beschreibung"], zeilen)
            elif wahl == "4":
                zeilen = [[str(k.id), k.name, k.beschreibung or "-"] for k in get_all_kategories(db)]
                zeige_tabelle("Kategorien", ["ID", "Name", "Beschreibung"], zeilen)
            elif wahl == "5":
                zeilen = [[str(t.id), t.name] for t in get_all_tags(db)]
                zeige_tabelle("Tags", ["ID", "Name"], zeilen)
            else:
                console.print("[red]Ungültige Eingabe.[/red]")


def abfragen_menu():
    while True:
        console.print("\n[bold cyan]── DATENBANK-ABFRAGEN ──[/bold cyan]")
        print("  [1] Materialien pro Themengebiet  (COUNT)")
        print("  [2] Ø Dateigröße pro Dateityp     (AVG)")
        print("  [3] Materialien + Themengebiete   (JOIN)")
        print("  [4] Materialien + Kommentare      (JOIN)")
        print("  [5] Kommentare pro Material        (JOIN + COUNT)")
        print("  [6] Material + Autor + Thema       (Multi-JOIN)")
        print("  [7] Vollständige Suche mit Filter  (Multi-JOIN)")
        print("  [8] Alle 7 Abfragen ausführen")
        print("  [0] Zurück")
        linie()
        wahl = input("Auswahl: ").strip()

        if wahl == "0":
            break

        with SessionLocal() as db:
            if wahl == "1":
                ergebnisse = anzahl_material_pro_themen(db)
                zeige_tabelle("Materialien pro Themengebiet (COUNT)", ["Themengebiet", "Anzahl"],
                              [[t, str(a)] for t, a in ergebnisse])

            elif wahl == "2":
                ergebnisse = durchschnitt_dateigroesse_pro_typ(db)
                zeilen = [[dt or "Unbekannt", f"{d:.0f} Bytes", f"{d/(1024*1024):.2f} MB"] for dt, d in ergebnisse]
                zeige_tabelle("Ø Dateigröße pro Typ (AVG)", ["Dateityp", "Bytes", "MB"], zeilen)

            elif wahl == "3":
                ergebnisse = materialien_mit_themen(db)
                zeige_tabelle("Materialien + Themengebiete (JOIN)", ["Titel", "Dateiname", "Themengebiet"],
                              [[ti, da or "-", th] for ti, da, th in ergebnisse])

            elif wahl == "4":
                ergebnisse = materialien_mit_kommentaren(db)
                zeilen = []
                for ti, da, tx, datum in ergebnisse:
                    zeilen.append([ti, da or "-", tx[:50] + "..." if len(tx) > 50 else tx, str(datum.date()) if datum else "-"])
                zeige_tabelle("Materialien + Kommentare (JOIN)", ["Titel", "Dateiname", "Kommentar", "Datum"], zeilen)

            elif wahl == "5":
                ergebnisse = kommentare_pro_material(db)
                zeige_tabelle("Kommentare pro Material (JOIN + COUNT)", ["Titel", "Dateiname", "Anzahl"],
                              [[ti, da or "-", str(an)] for ti, da, an in ergebnisse])

            elif wahl == "6":
                ergebnisse = material_mit_autor_und_thema(db)
                zeilen = [[ti, da or "-", au, th, str(dt.date()) if dt else "-"] for ti, da, au, th, dt in ergebnisse]
                zeige_tabelle("Material + Autor + Thema (Multi-JOIN)", ["Titel", "Datei", "Autor", "Thema", "Datum"], zeilen)

            elif wahl == "7":
                thema_id = None
                autor_id = None
                if input("Nach Thema filtern? (j/n): ").strip().lower() == "j":
                    thema = waehle_aus_liste(get_all_themen(db), lambda t: t.name)
                    if thema:
                        thema_id = thema.id
                if input("Nach Autor filtern? (j/n): ").strip().lower() == "j":
                    autor = waehle_aus_liste(get_all_users(db), lambda u: u.username)
                    if autor:
                        autor_id = autor.id
                ergebnisse = suche_material_mit_filtern(db, thema_id, autor_id)
                zeilen = [[r.titel, r.dateiname or "-", r.dateityp or "-", r.autor, r.themengebiet, r.kategorie] for r in ergebnisse]
                zeige_tabelle("Vollständige Suche (Multi-JOIN)", ["Titel", "Datei", "Typ", "Autor", "Thema", "Kategorie"], zeilen)

            elif wahl == "8":
                console.print("\n[bold blue]Alle 7 Abfragen:[/bold blue]\n")

                e = anzahl_material_pro_themen(db)
                zeige_tabelle("1. Materialien pro Thema (COUNT)", ["Thema", "Anzahl"], [[t, str(a)] for t, a in e])

                e = durchschnitt_dateigroesse_pro_typ(db)
                zeige_tabelle("2. Ø Dateigröße (AVG)", ["Typ", "Bytes", "MB"],
                              [[dt or "?", f"{d:.0f}", f"{d/(1024*1024):.2f}"] for dt, d in e])

                e = materialien_mit_themen(db)
                zeige_tabelle("3. Materialien + Themen (JOIN)", ["Titel", "Datei", "Thema"],
                              [[ti, da or "-", th] for ti, da, th in e])

                e = materialien_mit_kommentaren(db)
                zeige_tabelle("4. Materialien + Kommentare (JOIN)", ["Titel", "Datei", "Kommentar"],
                              [[ti, da or "-", tx[:40] + "..." if len(tx) > 40 else tx] for ti, da, tx, _ in e])

                e = kommentare_pro_material(db)
                zeige_tabelle("5. Kommentare pro Material (JOIN+COUNT)", ["Titel", "Datei", "Anzahl"],
                              [[ti, da or "-", str(an)] for ti, da, an in e])

                e = material_mit_autor_und_thema(db)
                zeige_tabelle("6. Material + Autor + Thema (Multi-JOIN)", ["Titel", "Datei", "Autor", "Thema"],
                              [[ti, da or "-", au, th] for ti, da, au, th, _ in e])

                e = suche_material_mit_filtern(db)
                zeige_tabelle("7. Vollständige Suche (Multi-JOIN)", ["Titel", "Autor", "Thema", "Kategorie"],
                              [[r.titel, r.autor, r.themengebiet, r.kategorie] for r in e])

                console.print("\n[bold green]Alle 7 Abfragen abgeschlossen.[/bold green]")
            else:
                console.print("[red]Ungültige Eingabe.[/red]")

        print()


def erstellen_menu():
    while True:
        console.print("\n[bold cyan]── NEUE EINTRÄGE ──[/bold cyan]")
        print("  [1] Benutzer")
        print("  [2] Themengebiet")
        print("  [3] Kategorie")
        print("  [4] Tag")
        print("  [0] Zurück")
        linie()
        wahl = input("Auswahl: ").strip()

        if wahl == "0":
            break

        with SessionLocal() as db:
            try:
                if wahl == "1":
                    name  = input("Benutzername: ").strip()
                    email = input("E-Mail: ").strip()
                    print("Rolle: [1] Lehrer  [2] Azubi  [3] Admin")
                    rolle = {"1": "Lehrer", "2": "Azubi", "3": "Admin"}.get(input("Auswahl: ").strip(), "Azubi")
                    user = create_user(db, name, email, rolle)
                    console.print(f"[bold green]Benutzer '{user.username}' erstellt (ID: {user.id})[/bold green]")

                elif wahl == "2":
                    name = input("Name: ").strip()
                    beschreibung = input("Beschreibung (optional): ").strip()
                    thema = create_thema(db, name, beschreibung)
                    console.print(f"[bold green]Themengebiet '{thema.name}' erstellt (ID: {thema.id})[/bold green]")

                elif wahl == "3":
                    name = input("Name: ").strip()
                    beschreibung = input("Beschreibung (optional): ").strip()
                    kat = create_kategorie(db, name, beschreibung)
                    console.print(f"[bold green]Kategorie '{kat.name}' erstellt (ID: {kat.id})[/bold green]")

                elif wahl == "4":
                    name = input("Tag-Name: ").strip()
                    t = create_tag(db, name)
                    console.print(f"[bold green]Tag '{t.name}' erstellt (ID: {t.id})[/bold green]")

                else:
                    console.print("[red]Ungültige Eingabe.[/red]")
            except Exception as e:
                console.print(f"[red]Fehler: {e}[/red]")


def hauptmenu():
    while True:
        console.print("\n[bold blue]╔══════════════════════════════════════╗[/bold blue]")
        console.print("[bold blue]║      LERNMATERIALVERWALTUNG          ║[/bold blue]")
        console.print("[bold blue]╚══════════════════════════════════════╝[/bold blue]")
        print("\n  [1] Material hochladen")
        print("  [2] Material herunterladen")
        print("  [3] Materialien suchen")
        print("  [4] Material löschen")
        print("  [5] Kommentare verwalten")
        print("  [6] Listen & Übersichten")
        print("  [7] Datenbank-Abfragen")
        print("  [8] Neue Einträge erstellen")
        print("  [0] Beenden")
        linie()
        wahl = input("Auswahl: ").strip()

        if wahl == "1":
            upload_menu()
        elif wahl == "2":
            download_menu()
        elif wahl == "3":
            suche_menu()
        elif wahl == "4":
            loeschen_menu()
        elif wahl == "5":
            kommentar_menu()
        elif wahl == "6":
            listen_menu()
        elif wahl == "7":
            abfragen_menu()
        elif wahl == "8":
            erstellen_menu()
        elif wahl == "0":
            console.print("\n[bold green]Auf Wiedersehen![/bold green]\n")
            break
        else:
            console.print("[red]Ungültige Eingabe (0–8).[/red]")


if __name__ == "__main__":
    hauptmenu()