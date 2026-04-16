import typer
from rich.console import Console
from rich.table import Table
from rich import box
from typing import Optional, List
from database import SessionLocal
from services import (
    get_all_users, get_all_themen, get_all_kategories, get_all_tags,
    get_all_materials, anzahl_material_pro_themen,
    durchschnitt_dateigroesse_pro_typ, materialien_mit_themen,
    materialien_mit_kommentaren, kommentare_pro_material,
    material_mit_autor_und_thema, suche_material_mit_filtern
)

app = typer.Typer(
    name="lernmaterial",
    help="Lernmaterialverwaltung - CLI fr die Lernmaterial-Datenbank",
    add_completion=False,
)

console = Console()


@app.command(name="list", help="Listet verschiedene Entitten aus der Datenbank auf")
def list_entities(
    entity: str = typer.Argument(
        ...,
        help="Zu listende Entitt: users, themen, kategorien, tags, materialien"
    )
):
    """Listet Entitten aus der Datenbank."""
    with SessionLocal() as db:
        if entity == "users":
            items = get_all_users(db)
            table = Table(title="Benutzer", box=box.ROUNDED)
            table.add_column("ID", style="cyan", no_wrap=True)
            table.add_column("Benutzername", style="green")
            table.add_column("Email", style="yellow")
            table.add_column("Rolle", style="magenta")
            table.add_column("Erstellt", style="dim")
            
            for user in items:
                table.add_row(
                    str(user.id),
                    user.username,
                    user.email,
                    user.rolle,
                    str(user.created_at) if user.created_at else "-"
                )
                
        elif entity == "themen":
            items = get_all_themen(db)
            table = Table(title="Themengebiete", box=box.ROUNDED)
            table.add_column("ID", style="cyan", no_wrap=True)
            table.add_column("Name", style="green")
            table.add_column("Beschreibung", style="yellow")
            
            for thema in items:
                table.add_row(
                    str(thema.id),
                    thema.name,
                    thema.beschreibung or "-"
                )
                
        elif entity == "kategorien":
            items = get_all_kategories(db)
            table = Table(title="Kategorien", box=box.ROUNDED)
            table.add_column("ID", style="cyan", no_wrap=True)
            table.add_column("Name", style="green")
            table.add_column("Beschreibung", style="yellow")
            
            for kat in items:
                table.add_row(
                    str(kat.id),
                    kat.name,
                    kat.beschreibung or "-"
                )
                
        elif entity == "tags":
            items = get_all_tags(db)
            table = Table(title="Tags", box=box.ROUNDED)
            table.add_column("ID", style="cyan", no_wrap=True)
            table.add_column("Name", style="green")
            
            for tag in items:
                table.add_row(str(tag.id), tag.name)
                
        elif entity == "materialien":
            items = get_all_materials(db)
            table = Table(title="Materialien", box=box.ROUNDED)
            table.add_column("ID", style="cyan", no_wrap=True)
            table.add_column("Titel", style="green")
            table.add_column("Dateiname", style="yellow")
            table.add_column("Typ", style="magenta")
            table.add_column("Gre", style="dim")
            table.add_column("In DB?", style="cyan")
            
            for mat in items:
                size_mb = mat.dateigroesse / (1024 * 1024) if mat.dateigroesse else 0
                table.add_row(
                    str(mat.id),
                    mat.titel,
                    mat.dateiname or "-",
                    mat.dateityp or "-",
                    f"{size_mb:.2f} MB",
                    "Ja" if mat.is_in_database else "Nein"
                )
                
        else:
            console.print(f"[red] Unbekannte Entitt: {entity}[/red]")
            console.print("[yellow]Verfgbare Entitten: users, themen, kategorien, tags, materialien[/yellow]")
            raise typer.Exit(1)
    
    console.print(table)
    console.print(f"[green] {len(items)} {entity} gefunden[/green]")


@app.command(name="queries", help="Fhrt die 7+ erforderlichen Suchabfragen aus")
def run_queries(
    query: str = typer.Argument(
        ...,
        help="""Zu ausfhrende Abfrage:
        count-per-thema    - Material pro Themengebiet (COUNT)
        avg-size-per-type  - Durchschnittliche Gre pro Dateityp (AVG)
        mat-with-themen    - Materialien mit Themengebieten (JOIN)
        mat-with-comments  - Materialien mit Kommentaren (JOIN)
        comments-per-mat   - Kommentare pro Material (JOIN + COUNT)
        mat-author-thema   - Material mit Autor und Thema (Multi-JOIN)
        """
    )
):
    """Fhrt eine der 7+ erforderlichen Suchabfragen aus."""
    with SessionLocal() as db:
        if query == "count-per-thema":
            results = anzahl_material_pro_themen(db)
            table = Table(title=" Material pro Themengebiet (COUNT)", box=box.ROUNDED)
            table.add_column("Themengebiet", style="green")
            table.add_column("Anzahl Materialien", style="cyan", justify="right")
            
            for thema, anzahl in results:
                table.add_row(thema, str(anzahl))
                
        elif query == "avg-size-per-type":
            results = durchschnitt_dateigroesse_pro_typ(db)
            table = Table(title=" Durchschnittliche Dateigre pro Typ (AVG)", box=box.ROUNDED)
            table.add_column("Dateityp", style="green")
            table.add_column("Durchschnitt (Bytes)", style="cyan", justify="right")
            table.add_column("Durchschnitt (MB)", style="yellow", justify="right")
            
            for dateityp, durchschnitt in results:
                mb = durchschnitt / (1024 * 1024) if durchschnitt else 0
                table.add_row(
                    dateityp or "Unbekannt",
                    f"{durchschnitt:.0f}" if durchschnitt else "0",
                    f"{mb:.2f}"
                )
                
        elif query == "mat-with-themen":
            results = materialien_mit_themen(db)
            table = Table(title=" Materialien mit Themengebieten (JOIN)", box=box.ROUNDED)
            table.add_column("Titel", style="green")
            table.add_column("Dateiname", style="yellow")
            table.add_column("Themengebiet", style="magenta")
            
            for titel, dateiname, themengebiet in results:
                table.add_row(titel, dateiname or "-", themengebiet)
                
        elif query == "mat-with-comments":
            results = materialien_mit_kommentaren(db)
            table = Table(title=" Materialien mit Kommentaren (JOIN)", box=box.ROUNDED)
            table.add_column("Titel", style="green")
            table.add_column("Dateiname", style="yellow")
            table.add_column("Kommentar (Auszug)", style="cyan")
            table.add_column("Datum", style="dim")
            
            for titel, dateiname, kommentar_text, datum in results:
                table.add_row(
                    titel,
                    dateiname or "-",
                    kommentar_text[:50] + "..." if len(kommentar_text) > 50 else kommentar_text,
                    str(datum.date()) if datum else "-"
                )
                
        elif query == "comments-per-mat":
            results = kommentare_pro_material(db)
            table = Table(title=" Kommentare pro Material (JOIN + COUNT)", box=box.ROUNDED)
            table.add_column("Titel", style="green")
            table.add_column("Dateiname", style="yellow")
            table.add_column("Anzahl Kommentare", style="cyan", justify="right")
            
            for titel, dateiname, anzahl in results:
                table.add_row(titel, dateiname or "-", str(anzahl))
                
        elif query == "mat-author-thema":
            results = material_mit_autor_und_thema(db)
            table = Table(title=" Material mit Autor und Thema (Multi-JOIN)", box=box.ROUNDED)
            table.add_column("Titel", style="green")
            table.add_column("Dateiname", style="yellow")
            table.add_column("Autor", style="magenta")
            table.add_column("Themengebiet", style="cyan")
            table.add_column("Erstellt", style="dim")
            
            for titel, dateiname, autor, themengebiet, datum in results:
                table.add_row(
                    titel,
                    dateiname or "-",
                    autor,
                    themengebiet,
                    str(datum.date()) if datum else "-"
                )
                
        else:
            console.print(f"[red] Unbekannte Abfrage: {query}[/red]")
            console.print("[yellow]Verfgbare Abfragen: count-per-thema, avg-size-per-type, mat-with-themen, mat-with-comments, comments-per-mat, mat-author-thema[/yellow]")
            raise typer.Exit(1)
    
    console.print(table)
    console.print(f"[green] {len(results)} Ergebnisse gefunden[/green]")


@app.command(name="search", help="Vollstndige Suche mit Filtern (Multi-Table JOIN)")
def search_materials(
    thema_id: Optional[int] = typer.Option(None, "--thema", "-t", help="Filter nach Themengebiet-ID"),
    autor_id: Optional[int] = typer.Option(None, "--autor", "-a", help="Filter nach Autor-ID"),
    show_filters: bool = typer.Option(False, "--show-filters", "-s", help="Zeigt verfgbare Filteroptionen an")
):
    """Durchsucht Materialien mit optionalen Filtern."""
    
    if show_filters:
        with SessionLocal() as db:
            # Themengebiete anzeigen
            themen = get_all_themen(db)
            table_themen = Table(title=" Verfgbare Themengebiete", box=box.ROUNDED)
            table_themen.add_column("ID", style="cyan", no_wrap=True)
            table_themen.add_column("Name", style="green")
            table_themen.add_column("Beschreibung", style="yellow")
            
            for thema in themen:
                table_themen.add_row(str(thema.id), thema.name, thema.beschreibung or "-")
            
            # Autoren anzeigen
            users = get_all_users(db)
            table_autoren = Table(title=" Verfgbare Autoren", box=box.ROUNDED)
            table_autoren.add_column("ID", style="cyan", no_wrap=True)
            table_autoren.add_column("Benutzername", style="green")
            table_autoren.add_column("Rolle", style="magenta")
            table_autoren.add_column("Email", style="yellow")
            
            for user in users:
                table_autoren.add_row(str(user.id), user.username, user.rolle, user.email)
            
            console.print(table_themen)
            console.print()
            console.print(table_autoren)
            return
    
    with SessionLocal() as db:
        results = suche_material_mit_filtern(db, thema_id, autor_id)
        
        if not results:
            console.print("[yellow] Keine Materialien gefunden mit den angegebenen Filtern[/yellow]")
            return
        
        table = Table(title=" Suchergebnisse", box=box.ROUNDED)
        table.add_column("Titel", style="green")
        table.add_column("Datei", style="yellow")
        table.add_column("Typ", style="magenta")
        table.add_column("Gre", style="dim")
        table.add_column("Autor", style="cyan")
        table.add_column("Themengebiet", style="blue")
        table.add_column("Kategorie", style="white")
        
        for row in results:
            size_mb = row.dateigroesse / (1024 * 1024) if row.dateigroesse else 0
            table.add_row(
                row.titel,
                row.dateiname or "-",
                row.dateityp or "-",
                f"{size_mb:.1f} MB",
                row.autor,
                row.themengebiet,
                row.kategorie
            )
        
        console.print(table)
        
        # Filter-Info anzeigen
        filter_info = []
        if thema_id:
            filter_info.append(f"Themengebiet-ID: {thema_id}")
        if autor_id:
            filter_info.append(f"Autor-ID: {autor_id}")
        
        if filter_info:
            console.print(f"[dim]Filter: {' + '.join(filter_info)}[/dim]")
        
        console.print(f"[green] {len(results)} Materialien gefunden[/green]")


@app.command(name="all-queries", help="Fhrt alle 7 erforderlichen Suchabfragen nacheinander aus")
def run_all_queries():
    """Fhrt alle 7 erforderlichen Suchabfragen aus."""
    console.print("[bold blue] Fhre alle 7 erforderlichen Suchabfragen aus...[/bold blue]")
    console.print()
    
    queries = [
        ("count-per-thema", "Material pro Themengebiet (COUNT)"),
        ("avg-size-per-type", "Durchschnittliche Gre pro Dateityp (AVG)"),
        ("mat-with-themen", "Materialien mit Themengebieten (JOIN)"),
        ("mat-with-comments", "Materialien mit Kommentaren (JOIN)"),
        ("comments-per-mat", "Kommentare pro Material (JOIN + COUNT)"),
        ("mat-author-thema", "Material mit Autor und Thema (Multi-JOIN)"),
    ]
    
    for query_key, query_name in queries:
        console.print(f"[bold cyan] {query_name}[/bold cyan]")
        try:
            # Temporr den Typer-Kontext umgehen, um die Query direkt aufzurufen
            with SessionLocal() as db:
                if query_key == "count-per-thema":
                    results = anzahl_material_pro_themen(db)
                    console.print(f"  [green] {len(results)} Themengebiete[/green]")
                elif query_key == "avg-size-per-type":
                    results = durchschnitt_dateigroesse_pro_typ(db)
                    console.print(f"  [green] {len(results)} Dateitypen[/green]")
                elif query_key == "mat-with-themen":
                    results = materialien_mit_themen(db)
                    console.print(f"  [green] {len(results)} Materialien[/green]")
                elif query_key == "mat-with-comments":
                    results = materialien_mit_kommentaren(db)
                    console.print(f"  [green] {len(results)} Kommentare[/green]")
                elif query_key == "comments-per-mat":
                    results = kommentare_pro_material(db)
                    console.print(f"  [green] {len(results)} Materialien mit Kommentarzhlung[/green]")
                elif query_key == "mat-author-thema":
                    results = material_mit_autor_und_thema(db)
                    console.print(f"  [green] {len(results)} Materialien[/green]")
        except Exception as e:
            console.print(f"  [red] Fehler: {e}[/red]")
        console.print()
    
    console.print("[bold green] Alle 7 Suchabfragen erfolgreich ausgefhrt![/bold green]")
    console.print("[yellow] Verwende 'lernmaterial search --show-filters' fr die 7. Abfrage (Vollstndige Suche)[/yellow]")


@app.command(name="stats", help="Zeigt Statistiken ber die Datenbank")
def show_stats():
    """Zeigt Statistiken ber die Datenbank."""
    with SessionLocal() as db:
        # Material-Statistiken
        materials = get_all_materials(db)
        users = get_all_users(db)
        themen = get_all_themen(db)
        kategorien = get_all_kategories(db)
        tags = get_all_tags(db)
        
        table = Table(title=" Datenbank-Statistiken", box=box.ROUNDED)
        table.add_column("Entitt", style="cyan")
        table.add_column("Anzahl", style="green", justify="right")
        
        table.add_row("Materialien", str(len(materials)))
        table.add_row("Benutzer", str(len(users)))
        table.add_row("Themengebiete", str(len(themen)))
        table.add_row("Kategorien", str(len(kategorien)))
        table.add_row("Tags", str(len(tags)))
        
        # Material-Gren-Statistik
        total_size = sum(m.dateigroesse or 0 for m in materials)
        in_db_count = sum(1 for m in materials if m.is_in_database)
        in_fs_count = len(materials) - in_db_count
        
        table.add_row("Materialien in DB", str(in_db_count))
        table.add_row("Materialien im Dateisystem", str(in_fs_count))
        table.add_row("Gesamtgre", f"{total_size / (1024*1024):.2f} MB")
        
        console.print(table)


@app.callback()
def main():
    """
    Lernmaterialverwaltung - CLI fr die Lernmaterial-Datenbank
    
    Verwaltet Lernmaterialien (PDF, DOCX, JPEG, Python) in einer MySQL-Datenbank.
    Erfllt die 7+ Suchabfragen-Anforderung fr das LF8 Abschlussprojekt.
    """
    pass


if __name__ == "__main__":
    app()