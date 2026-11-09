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
- Die Geschichten stehen im Blatt „Einträge“ (Berlin) bzw. „Frankfurt“. Ein Pin pro Ort-ID: alle Zeilen mit derselben Ort-ID landen auf einem Pin. Ortsname, Koordinaten, Adresse, Bezirk und Genauigkeit nimmt das Skript aus der ersten Zeile, die sie ausfüllt; weichen spätere Zeilen um mehr als 100 m ab, gibt es einen Hinweis. Ein eigenes Blatt „Orte“ wird nicht mehr gebraucht (ist es noch da, wird es ignoriert).
- Flag → Wichtigkeit: Touri 1x1 = 3, Sehenswürdigkeit = 2, Lokal = 1. Der Pin bekommt die höchste Stufe seiner Geschichten.
- Spalte „Vorgeschlagen“ (Ja/Nein, auch j, x, 1): vierte Punktkategorie, Punkt in Bernstein, gleiche Priorität und Beschriftung wie Touri 1x1.
  Ein Ort ist vorgeschlagen, sobald eine seiner Geschichten es ist. Fehlt die Spalte, gilt alles als nicht vorgeschlagen (das Skript weist darauf hin).
  Im Filter steht „Vorgeschlagen“ (mit Bernstein-Punkt) als erstes Tag und zeigt nur Vorgeschlagenes.
- Ist die Spalte „Region“ leer, gilt die Stadt aus dem Dateinamen (z. B. „… Einträge Frankfurt.xlsx“ → frankfurt).
- Tags werden über das Blatt „Tags“ in Epochen und Themen getrennt. Kategorien, Epochen und Themen bleiben so in den Daten; welche davon Nutzer als Tags sehen, steht in `data/tags.json` (siehe „Tags im Filter“).
- Stadt, Kreis und Bundesland kommen aus dem Blatt „Geo“ (über die Spalte Bezirk/Stadtteil).
- Status „Idee“ und „Verworfen“ fehlen auf der Karte. „Prüfen“ erscheint mit dem Hinweis „wird geprüft“, die Notiz aus „Prüfen / unsicher“ steht im Tooltip.
- Genauigkeit „ungefähr“ oder „Straße“ wird in der Detailansicht angezeigt.
- Am Ende listet das Skript Hinweise: fehlende Koordinaten, unbekannte Tags oder Kategorien, doppelte IDs.
- Die Frankfurter und Hofheimer IDs (z. B. `roemer`, `hofheim-ringwall`) stammen aus der alten Karte und bleiben so, weil `data/images.json` daran hängt.

## Aufbau
- `index.html`: App (MapLibre GL 4.7.1, Kartenstile OpenFreeMap bzw. CARTO auf OpenStreetMap-Daten).
- `data/berlin.geojson`: ein Feature pro Ort mit `id, title, importance, place{stadtteil, stadt, kreis, bundesland}, address, precision, stories[]`.
  Jede Geschichte hat `id, title, teaser, story[], categories[], epochs[], tags[], flag, importance, period, year, status, note, sources[], imageQuery, images[]`.
  `images[]` sind die Bilder aus der Tabelle (siehe Bilder), gleiches Format wie in `data/images.json` plus `slot` (1 = Hauptbild, 2 = zweites Bild).
  Oben in der Datei steht unter `lore` die Reihenfolge der Excel-Stammdaten (für die Filter zählt `data/tags.json`).
- `data/frankfurt.geojson`: gleiches Format wie Berlin, Frankfurt und Hofheim zusammen. Die App liest auch noch das ältere Format mit einer Geschichte pro Feature.
- Die alten Startdaten (`seed_frankfurt.py`, `seed_hofheim.py`, `data/hofheim.geojson`) liegen in „00 Lore Sicherungskopien/Frankfurt und Hofheim vor der Excel (2026-10-31)“.
- `tools/sheet_to_geojson.py`: Tabellen → GeoJSON. `tools/sicherung.py`: Sicherungskopien der Tabellen.
- `data/tags.json`: welche Tags Nutzer im Filter sehen und woraus sie entstehen.
- `tools/build.py`: baut die Einzeldateien (bettet auch `data/tags.json` ein).

## Tags im Filter
Für Nutzer gibt es nur noch Tags, ohne Überschriften und ohne Wichtigkeits-Filter (die Wichtigkeit sieht man an den Punkten).
Die Kategorien, Epochen und Themen der Excel bleiben unverändert in den Daten und in der Suche, die App übersetzt sie nur.
Reihenfolge im Panel: oben Stadtteil bzw. Bezirk, darunter alle Tags in einem Fluss ohne Umbruch: „Vorgeschlagen“ (nur wenn es welche gibt), die Zeit-Tags, die Themen-Tags. Gemerktes hat kein eigenes Tag, dafür gibt es „Meine Orte“.
Innerhalb der Zeit-Tags und innerhalb der Themen-Tags reicht eins (oder), Zeit und Thema zusammen müssen beide passen (und).

Die Übersetzung steht in `data/tags.json` und lässt sich dort ändern (danach `python3 tools/build.py`):
- `zeit`: Frühzeit, Mittelalter, Neuzeit, Moderne, Gegenwart. `aus` nennt die Excel-Epochen.
  Teilen sich zwei Zeit-Tags eine Epoche („Mittelalter & früher“), entscheidet das Jahr über `bisJahr` (bis 499 Frühzeit, sonst Mittelalter);
  ohne Jahr gilt der letzte. Das Jahr kommt aus der Spalte Jahr, sonst grob aus dem Zeitraum („um 400 v. Chr.“, „14. Jh.“).
  Geschichten ohne Epoche bekommen ihren Zeit-Tag allein über das Jahr, ohne Jahr gar keinen.
  Aktuell: Frühzeit ← Mittelalter & früher bis 499 · Mittelalter ← Mittelalter & früher ab 500 · Neuzeit ← Frühe Neuzeit, 19. Jahrhundert ·
  Moderne ← Kaiserreich, Weimarer Republik, NS-Zeit, Nachkriegszeit & Kalter Krieg · Gegenwart ← Wende & Gegenwart.
- `themen`: die übrigen Tags in Filter-Reihenfolge. `aus` nennt Excel-Kategorien, -Epochen oder -Themen (genau wie dort geschrieben).
  Ohne passenden Eintrag bekommt eine Geschichte kein Themen-Tag, das ist in Ordnung („Geschichte & Politik“, Stadt-Ikonen,
  Kiez-Geschichten, Verkehr, Sport, Spitzname, Friedhof, Erinnerung und Religion sind bewusst nicht übersetzt).
- „Politik“ kommt aus dem Thema Protest und zusätzlich über Stichwörter (`woerter`) in Titel oder Teaser, aber nur bei Geschichten
  mit der Kategorie „Geschichte & Politik“ (`woerterNurMit`). Stichwörter gelten am Wortanfang und mit Groß-/Kleinschreibung.
  Ist ein Treffer falsch, das Stichwort entfernen oder in der Excel ein eigenes Thema „Politik“ anlegen und hier unter `aus` eintragen.
- `minGeschichten`: Tags mit weniger Geschichten in einer Stadt erscheinen dort nicht (aktuell 3).
- Von den Themen-Tags sind erst 12 sichtbar, „+N weitere“ klappt den Rest auf (`TAGS_VISIBLE` in `index.html`).
- Die Liste zeigt bei einer Geschichte die ersten zwei Themen-Tags, „Entdecken“ nutzt die Themen-Tags für die Kacheln und die Zeit-Tags für die Zeitreise.

## Meine Orte (Merken und Kenn ich)
In der Detailansicht jedes Orts gibt es oben rechts neben dem Schließen-Knopf zwei Icon-Knöpfe: Lesezeichen („Merken“) und Haken („Kenn ich“), erklärt per Tooltip. Beides liegt nur im Browser (localStorage, Schlüssel `lore-user`), ohne Konto.
- Darstellung, in dieser Reihenfolge: **Kenn ich** (kleiner grauer Punkt, immer sichtbar ab Zoom 10, verdrängt keine anderen Punkte) vor **Gemerkt** (grün, wie Touri 1x1)
  vor **Vorgeschlagen** (Bernstein) vor der Wichtigkeit aus der Excel. Die Kategorie bleibt in der Detailansicht sichtbar.
- Der Knopf mit dem Lesezeichen oben rechts öffnet „Meine Orte“ mit den Listen „Gemerkt“ und „Kenne ich“ (über alle Städte), dazu „Daten sichern“
  (JSON-Datei herunterladen) und „Wiederherstellen“ (führt zusammen, löscht nichts). `#meine` in der Adresse öffnet die Ansicht direkt.
- Datenmodell: `{ app: "sagenhaft", v: 1, updated, places: { "<ort-id>": { saved?: Zeitstempel, known?: Zeitstempel } } }`. Schlüssel ist die Ort-ID
  aus der Haupttabelle, deshalb Ort-IDs nicht mehr ändern. Die Zeitstempel erlauben später einen Abgleich mit einem Login,
  eigene Listen wären später weitere Sammlungen von Ort-IDs. Schemaänderungen gehören in `migrateUser()` in `index.html`.

## Entdecken
Kuratierte Seite je Stadt: Geschichte des Tages (wechselt täglich, bevorzugt Bedeutendes, nicht mehr in Prüfung und, wenn vorhanden, mit Bild),
„Rund um die Mitte“ (Orte nahe der Stadtmitte), das 1x1 der Stadt, Themen-Kacheln aus den Themen-Tags und eine Zeitreise nach Zeit-Tags.
Jede Karte springt zum Ort auf der Karte, Themen und Zeiten öffnen die Karte mit passendem Filter.

## Bilder
Die Detailansicht zeigt die Bilder eines Orts als Slideshow mit Namensnennung. Bilder werden direkt von Wikimedia geladen (Hotlink, keine Kopie).

### Aus der Tabelle (Vorrang)
Im Geschichten-Blatt gibt es zwei Spalten: **Bild 1 (Hauptbild)** und **Bild 2** (z. B. aktuell und historisch).
In Frankfurt ist „Bild 1“ die frühere Spalte „Bildlink“ (Spalte L), „Bild 2“ steht ganz hinten (Spalte V) und darf in Excel an jede Stelle geschoben werden, das Skript sucht die Spalten über den Namen.
In Berlin stehen beide hinten (X und Y).

- In die Zelle kommt ein Link auf die Bilddatei bei Wikimedia Commons. Es reicht der Link aus der Adresszeile, wenn das Bild
  auf Commons oder in Wikipedia groß angezeigt wird (er enthält `File:` oder `Datei:`), z. B.
  `https://de.wikipedia.org/wiki/Saalhof#/media/Datei:Frankfurt_Am_Main-Saalhof-Ansicht_vom_Eisernen_Steg.jpg`.
  Ein Link auf eine Kategorie- oder Artikelseite ohne Bild reicht nicht, das Skript meldet ihn.
- Angezeigt wird ein Vorschaubild mit etwa 800 px Breite (Commons rundet auf seine festen Größen, z. B. 960 px), nicht das Original.
- Urheber und Lizenz fragt `tools/sheet_to_geojson.py` einmal bei Commons ab und merkt sie sich in `data/bildinfos.json`
  (Internet nötig, sonst Hinweis und „Urheber und Lizenz: Wikimedia Commons“ als Link; einfach später nochmal laufen lassen).
  `--offline` überspringt die Abfrage. Lizenzen außer CC0, Public Domain, CC BY und CC BY-SA werden als Hinweis gemeldet.
- Unter dem Bild steht nur die Quellenangabe (Urheber, Lizenz, Link zur Quelle), keine Bildunterschrift. Der Bildtitel dient als Alt-Text.
- Bilder von anderswo: `Link | Urheber | Lizenz` in die Zelle. So lassen sich auch die Commons-Angaben überschreiben.
- Reihenfolge in der App: wichtigste Geschichte des Orts zuerst, je Geschichte Bild 1 vor Bild 2. Das erste Bild ist auch das Bild auf der Entdecken-Seite.
- Sobald eine Geschichte eines Orts ein Bild aus der Tabelle hat, zeigt der Ort nur noch die Tabellenbilder, die Vorschläge aus `data/images.json` entfallen dort.
- Die Bilder stehen danach als `images[]` an der Geschichte in `data/<region>.geojson`. Die Umwandlung steckt in `tools/bildlinks.py`.

### Automatische Vorschläge (Fallback)
Für Orte ohne Tabellenbild: `data/images.json` (Schlüssel = Orts- oder Geschichten-ID, Liste von Bildern mit
`title, url, author, license, licenseUrl, source, alt`). Hat ein Ort mehrere Geschichten, werden ihre Bilder zusammengeführt.

- Vorschläge holen: `python3 tools/fetch_commons.py` (Internet nötig). Das Skript nimmt nur CC0, Public Domain, CC BY und CC BY-SA.
- Ausgabe kurz durchsehen, Unpassendes aus `data/images.json` löschen, eigene Suchbegriffe in `data/commons_queries.json`.
- Danach `python3 tools/build.py`.

## Mehrere Städte
In `index.html` stehen die Städte in der Liste `REGIONS` (id, Name, Datei, Kartenmitte, Zoom, Bezeichnung für Stadtteil/Bezirk).
Für eine neue Stadt: GeoJSON anlegen (IDs mit Ortskürzel, z. B. `hofheim-...`), in `REGIONS` eintragen, `python3 tools/build.py`.
„In meiner Nähe“ zoomt nur auf den Standort laut Browser (blauer Punkt). Liegt er in einer anderen Stadt der Karte, wird diese gewählt. Entfernungen werden nirgends angezeigt; die Liste ist nach Nähe zur Kartenmitte sortiert.

## Zoom-Logik
Die Karte geht von Zoom 5 bis 19. Alle Stufen dürfen auf jeder Zoomstufe erscheinen; die Dichte regelt die Überlappung, so dass in dünn besetzten
Gegenden auch lokale Punkte früh sichtbar sind. Feste Schwellen lassen sich in `MIN_ZOOM` setzen (oder je Stadt über `minZoom` in `REGIONS`),
falls es mit mehr Daten zu voll wird. Was sich auf dem Bildschirm überlappen würde,
wird ausgeblendet statt zu einer Zahl zusammengefasst; Reihenfolge nach Wichtigkeit, dann nach Zahl der Geschichten, innerhalb einer Stufe zufällig.
Unter Zoom 10 erscheinen höchstens 4 Orte. Bei höchstens 15 Treffern werden alle gezeigt.
Beschriftung: Weiter draußen zeigt die Karte nur Punkte, damit sie nicht wie ein Standard-Reiseführer wirkt. Namen von Touri 1x1
(und Vorgeschlagen, Gemerkt) stehen erst ab Zoom 14 fest am Pin, davor erscheinen sie beim Darüberfahren. Mit Maus bleiben alle anderen
beim Darüberfahren. Auf Touch-Geräten erscheinen Namen bei Sehenswürdigkeiten ebenfalls ab Zoom 14 und bei Lokalem ab 15,3; Antippen öffnet die Geschichte.
Die Schwellen stehen in `index.html` unter `LABEL_ZOOM` (Startansicht: Frankfurt 13,2, Berlin 12,4, also noch ohne Namen).

## Stadtteile (Frankfurt)
Die Frankfurter Stadtteile sind zart eingefärbt und dezent abgegrenzt, ab Zoom 12 steht ihr Name in der Fläche.
Nachbarn bekommen verschiedene Töne. Unterteilte Stadtteile (Nordend-Ost/West, Westend-Nord/Süd, Sachsenhausen-Nord/Süd) sind zusammengelegt.
- Daten: `data/frankfurt-stadtteile.geojson`, erzeugt mit `python3 tools/make_districts.py` (braucht shapely, lädt die Grenzen von GitHub).
- Quelle: Stadtteilgrenzen der Stadt Frankfurt am Main (Bürgeramt, Statistik und Wahlen), Datenlizenz Deutschland Namensnennung 2.0;
  die Namensnennung steht unten rechts in der Karte. GeoJSON-Aufbereitung aus dem Projekt codeforgermany/click_that_hood.
- Eingebunden über `areas:` im `REGIONS`-Eintrag; Töne und Deckkraft stehen in `index.html` unter `AREA_TONES` und `AREA`.
- Im Einfachmodus ohne WebGL gibt es Flächen und Grenzen, aber keine Stadtteilnamen.

## Gewässernamen und Brunnen
Namen von Flüssen und Seen sowie Brunnen aus der Grundkarte sind ausgeblendet, weil viele Brunnen eigene Einträge haben
(weitere POI-Arten lassen sich in `HIDE_POI` in `index.html` ergänzen). Im Einfachmodus ohne WebGL
sind die Namen fest in die Rasterkacheln gedruckt und lassen sich nicht ausblenden.

## Dunkelmodus
Der dunkle Kartenstil wird nach dem Laden aufgehellt: Straßen nach Klasse gestaffelt (Hauptstraßen am hellsten), Wasser, Parks und Gebäude
leicht abgesetzt, Beschriftungen heller. Die Farben stehen in `index.html` unter `DARK`. Im Einfachmodus ohne WebGL werden die Rasterkacheln per Filter aufgehellt.

## Ohne WebGL
Ist WebGL im Browser aus (z. B. Hardwarebeschleunigung deaktiviert), läuft die Karte automatisch im Einfachmodus mit Leaflet und Rasterkacheln (`vendor/fallback-map.js`). Alles andere bleibt gleich.

## Hinweise
- Koordinaten sind von Hand gesetzt und auf wenige Dutzend Meter genau; Texte sind eigene Kurzfassungen und sollten vor einer Veröffentlichung redaktionell geprüft werden.
- Die CARTO-Kartenstile sind für nicht-kommerzielle Nutzung frei; für einen öffentlichen Start eigene Kacheln (z. B. OpenFreeMap oder Protomaps) einplanen.
- „Sagenhaft“ ist ein Arbeitsname und steht nur in `index.html` (Kopfzeile und Seitentitel).
