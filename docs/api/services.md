# Datenbankoperationen (Services)

Alle Funktionen für CRUD-Operationen, Datei-Upload/-Download und die 7 Pflichtabfragen.

## Benutzer-Operationen

::: services.get_all_users
::: services.get_user_by_id
::: services.create_user

## Themengebiet-Operationen

::: services.get_all_themen
::: services.get_thema_by_id
::: services.create_thema

## Kategorie-Operationen

::: services.get_all_kategories
::: services.get_kategorie_by_id
::: services.create_kategorie

## Tag-Operationen

::: services.get_all_tags
::: services.get_tag_by_id
::: services.create_tag

## Material-Operationen

::: services.upload_material
::: services.download_material
::: services.search_materials
::: services.get_material_by_id
::: services.delete_material
::: services.get_all_materials

## Kommentar-Operationen

::: services.get_comments_for_material
::: services.create_comment
::: services.get_comment_by_id
::: services.delete_comment

## 7 Pflichtabfragen (LF8)

::: services.anzahl_material_pro_themen
::: services.durchschnitt_dateigroesse_pro_typ
::: services.materialien_mit_themen
::: services.materialien_mit_kommentaren
::: services.kommentare_pro_material
::: services.material_mit_autor_und_thema
::: services.suche_material_mit_filtern
