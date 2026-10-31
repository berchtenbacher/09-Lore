# Sagenhaft – Lore-Karte (Prototyp)

Interaktive Karte mit Geschichten, Sagen und Persönlichkeiten zu Orten in Berlin sowie Frankfurt am Main und Umgebung (mit Hofheim am Taunus).
Zwei Ansichten, umschaltbar oben in der Kopfzeile (mobil unten): **Karte** (Startansicht) und **Entdecken** (kuratierte Seite je Stadt).

## Öffnen
- **Einfach:** eine Datei aus `dist/` per Doppelklick öffnen (Daten sind eingebettet, Internet nötig für Karte und Schriften):
  - `dist/sagenhaft.html`: alle Städte, Auswahl oben neben dem Logo
  - `dist/sagenhaft-berlin.html`, `dist/sagenhaft-frankfurt.html` (Frankfurt und Umgebung): jeweils nur eine Karte
- **Entwicklung:** im Ordner einen Webserver starten, z. B. `python3 -m http.server`, dann `http://localhost:8000` öffnen.
  `index.html` lädt dann die Dateien aus `data/`. Mit `?stadt=berlin` startet die Karte in einer bestimmten Stadt, mit `#entdecken` auf der Entdecken-Seite.
- Nach Änderungen an den Daten: `python3 tools/build.py` erzeugt die Einzeldateien neu.

## Daten aus den Excel-Tabellen
Alle Orte kommen aus zwei Tabellen im Projektordner. Die Skripte lesen sie nur, nie wird etwas darin verändert.
- „Lore Tags, Kategorien und Einträge Berlin.xlsx“ → `data/berlin.geojson`
- „Lore Tags, Kategorien und Einträge Frankfurt.xlsx“ → `data/frankfurt.geojson` (Karte „Frankfurt und Umgebung“, mit Hofheim am Taunus)

    python3 tools/sicherung.py "vor Änderung"   # Kopie beider Tabellen nach „00 Lore Sicherungskopien“
    python3 tools/sheet_to_geojson.py           # liest alle „Lore Tags, Kategorien und Einträge *.xlsx“
    python3 tools/build.py

Das Skript braucht `openpyxl` (`pip install openpyxl`) und schreibt pro Region (Spalte „Region“) eine Datei `data/<region>.geojson`.
Einzelne Datei: `python3 tools/sheet_to_geojson.py "Lore Tags, Kategorien und Einträge Berlin.xlsx"`.
- Die Geschichten stehen im Blatt „Einträge“ (Berlin) bzw. „Frankfurt“. Ein Pin pro Ort aus dem Blatt „Orte“, die Geschichten hängen über die Ort-ID daran.
- Flag → Wichtigkeit: Touri 1x1 = 3, Sehenswürdigkeit = 2, Lokal = 1. Der Pin bekommt die höchste Stufe seiner Geschichten.
- Tags werden über das Blatt „Tags“ in Epochen und Themen getrennt; Kategorien, Epochen und Themen sind Filter in der App, in der Reihenfolge der Stammdaten-Blätter.
- Stadt, Kreis und Bundesland kommen aus dem Blatt „Geo“ (über die Spalte Bezirk/Stadtteil).
- Status „Idee“ und „Verworfen“ fehlen auf der Karte. „Prüfen“ erscheint mit dem Hinweis „wird geprüft“, die Notiz aus „Prüfen / unsicher“ steht im Tooltip.
- Genauigkeit „ungefähr“ oder „Straße“ wird in der Detailansicht angezeigt.
- Am Ende listet das Skript Hinweise: fehlende Koordinaten, unbekannte Tags oder Kategorien, doppelte IDs.
- Die Frankfurter und Hofheimer IDs (z. B. `roemer`, `hofheim-ringwall`) stammen aus der alten Karte und bleiben so, weil `data/images.json` daran hängt.

## Aufbau
- `index.html`: App (MapLibre GL 4.7.1, Kartenstile OpenFreeMap bzw. CARTO auf OpenStreetMap-Daten).
- `data/berlin.geojson`: ein Feature pro Ort mit `id, title, importance, place{stadtteil, stadt, kreis, bundesland}, address, precision, stories[]`.
  Jede Geschichte hat `id, title, teaser, story[], categories[], epochs[], tags[], flag, importance, period, year, status, note, sources[], imageQuery`.
  Oben in der Datei steht unter `lore` die Reihenfolge der Filter.
- `data/frankfurt.geojson`: gleiches Format wie Berlin, Frankfurt und Hofheim zusammen. Die App liest auch noch das ältere Format mit einer Geschichte pro Feature.
- Die alten Startdaten (`seed_frankfurt.py`, `seed_hofheim.py`, `data/hofheim.geojson`) liegen in „00 Lore Sicherungskopien/Frankfurt und Hofheim vor der Excel (2026-10-31)“.
- `tools/sheet_to_geojson.py`: Tabellen → GeoJSON. `tools/sicherung.py`: Sicherungskopien der Tabellen.
- `tools/build.py`: baut die Einzeldateien.

## Entdecken
Kuratierte Seite je Stadt: Geschichte des Tages (wechselt täglich, bevorzugt Bedeutendes, nicht mehr in Prüfung und, wenn vorhanden, mit Bild),
„In deiner Nähe“ (ohne Standort: rund um die Stadtmitte), das 1x1 der Stadt, Themen-Kacheln aus den Kategorien und eine Zeitreise nach Epochen.
Jede Karte springt zum Ort auf der Karte, Themen und Epochen öffnen die Karte mit passendem Filter.

## Bilder (Wikimedia Commons)
Bilder liegen getrennt von den Texten in `data/images.json` (Schlüssel = Orts- oder Geschichten-ID, Liste von Bildern mit
`title, url, author, license, licenseUrl, source, alt`). Die Detailansicht zeigt sie als Slideshow mit Namensnennung,
Bilder werden direkt von upload.wikimedia.org geladen (Hotlink, keine Kopie). Hat ein Ort mehrere Geschichten, werden ihre Bilder zusammengeführt.

- Vorschläge holen: `python3 tools/fetch_commons.py` (Internet nötig). Das Skript nimmt nur CC0, Public Domain, CC BY und CC BY-SA.
- Ausgabe kurz durchsehen, Unpassendes aus `data/images.json` löschen, eigene Suchbegriffe in `data/commons_queries.json`.
- Danach `python3 tools/build.py`.

## Mehrere Städte
In `index.html` stehen die Städte in der Liste `REGIONS` (id, Name, Datei, Kartenmitte, Zoom, Bezeichnung für Stadtteil/Bezirk).
Für eine neue Stadt: GeoJSON anlegen (IDs mit Ortskürzel, z. B. `hofheim-...`), in `REGIONS` eintragen, `python3 tools/build.py`.
„In meiner Nähe“ springt zur nächsten Stadt.

## Zoom-Logik
Die Karte geht von Zoom 5 bis 19. Alle Stufen dürfen auf jeder Zoomstufe erscheinen; die Dichte regelt die Überlappung, so dass in dünn besetzten
Gegenden auch lokale Punkte früh sichtbar sind. Feste Schwellen lassen sich in `MIN_ZOOM` setzen (oder je Stadt über `minZoom` in `REGIONS`),
falls es mit mehr Daten zu voll wird. Was sich auf dem Bildschirm überlappen würde,
wird ausgeblendet statt zu einer Zahl zusammengefasst; Reihenfolge nach Wichtigkeit, dann nach Zahl der Geschichten, innerhalb einer Stufe zufällig
(„Andere vorschlagen“ mischt neu). Unter Zoom 10 erscheinen höchstens 4 Orte. Bei höchstens 15 Treffern werden alle gezeigt.
Beschriftung: Mit Maus steht nur bei Touri 1x1 der Name fest am Pin, alle anderen zeigen ihn beim Darüberfahren.
Auf Touch-Geräten erscheinen Namen bei Sehenswürdigkeiten ab Zoom 14 und bei Lokalem ab 15,3; Antippen öffnet die Geschichte.

## Dunkelmodus
Der dunkle Kartenstil wird nach dem Laden aufgehellt: Straßen nach Klasse gestaffelt (Hauptstraßen am hellsten), Wasser, Parks und Gebäude
leicht abgesetzt, Beschriftungen heller. Die Farben stehen in `index.html` unter `DARK`. Im Einfachmodus ohne WebGL werden die Rasterkacheln per Filter aufgehellt.

## Ohne WebGL
Ist WebGL im Browser aus (z. B. Hardwarebeschleunigung deaktiviert), läuft die Karte automatisch im Einfachmodus mit Leaflet und Rasterkacheln (`vendor/fallback-map.js`). Alles andere bleibt gleich.

## Hinweise
- Koordinaten sind von Hand gesetzt und auf wenige Dutzend Meter genau; Texte sind eigene Kurzfassungen und sollten vor einer Veröffentlichung redaktionell geprüft werden.
- Die CARTO-Kartenstile sind für nicht-kommerzielle Nutzung frei; für einen öffentlichen Start eigene Kacheln (z. B. OpenFreeMap oder Protomaps) einplanen.
- „Sagenhaft“ ist ein Arbeitsname und steht nur in `index.html` (Kopfzeile und Seitentitel).
