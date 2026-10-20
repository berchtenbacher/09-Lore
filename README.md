# Lore-Karte Frankfurt (Prototyp)

Interaktive Karte mit Geschichten, Sagen und Persönlichkeiten zu Orten in Frankfurt am Main.

## Öffnen
- **Einfach:** `dist/lore-map-frankfurt.html` per Doppelklick im Browser öffnen (Daten sind eingebettet, Internet nötig für Karte und Schriften).
- **Entwicklung:** im Ordner einen Webserver starten, z. B. `python3 -m http.server`, dann `http://localhost:8000` öffnen. `index.html` lädt dann `data/frankfurt.geojson`.
- Nach Änderungen an den Daten: `python3 tools/build.py` erzeugt die Einzeldatei neu.

## Aufbau
- `index.html`: App (MapLibre GL 4.7.1, Kartenstile CARTO Positron/Dark Matter auf OpenStreetMap-Daten).
- `data/frankfurt.geojson`: alle Lore-Items. Ein Feature pro Ort mit
  `id, title, kind, importance (1 Lokal, 2 Bedeutend, 3 Wahrzeichen), themes[], epochs[],
  place{stadtteil, stadt, kreis, bundesland}, address, period, teaser, story[], sources[], status, author, updated`.
  `status`, `author` und `updated` sind schon für spätere Konten und Moderation vorgesehen.
- `tools/seed_frankfurt.py`: erzeugt die Startdaten. `tools/build.py`: baut die Einzeldatei.

## Zoom-Logik
Wahrzeichen sind immer sichtbar, "Bedeutend" ab Zoom 12,4, "Lokal" ab 13,9. Was sich auf dem Bildschirm überlappen würde,
wird ausgeblendet statt zu einer Zahl zusammengefasst; Reihenfolge nach Wichtigkeit, innerhalb einer Stufe zufällig
("Andere vorschlagen" mischt neu). Weit herausgezoomt erscheinen höchstens 4 Wahrzeichen.

## Hinweise
- Koordinaten sind von Hand gesetzt und auf wenige Dutzend Meter genau; Texte sind eigene Kurzfassungen und sollten vor einer Veröffentlichung redaktionell geprüft werden.
- Die CARTO-Kartenstile sind für nicht-kommerzielle Nutzung frei; für einen öffentlichen Start eigene Kacheln (z. B. OpenFreeMap oder Protomaps) einplanen.
