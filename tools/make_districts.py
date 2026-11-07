"""Stadtteilflächen für die Karte: zarte Einfärbung und Grenzen, damit man sieht, wo man ist.

    python3 tools/make_districts.py                 # lädt die Frankfurter Stadtteilgrenzen von GitHub
    python3 tools/make_districts.py stadtteile.geojson

Quelle: Stadtteilgrenzen der Stadt Frankfurt am Main (Bürgeramt, Statistik und Wahlen), Datenlizenz Deutschland
Namensnennung 2.0 (dl-de/by-2-0), als GeoJSON aufbereitet im Projekt codeforgermany/click_that_hood.
Unterteilte Stadtteile (Nordend-Ost/West, Westend-Nord/Süd, Sachsenhausen-Nord/Süd) werden zusammengelegt.
Schreibt data/frankfurt-stadtteile.geojson: Flächen mit Farbnummer (Nachbarn bekommen verschiedene Töne) und je
einen Punkt für die Beschriftung. Braucht shapely (pip install shapely).
"""
import json, pathlib, sys, urllib.request
from shapely.geometry import shape, mapping
from shapely.ops import unary_union, polylabel

SOURCE = "https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/frankfurt-main.geojson"
ATTRIBUTION = "Stadtteile: Stadt Frankfurt am Main, dl-de/by-2-0"
MERGE = {
    "Nordend-Ost": "Nordend", "Nordend-West": "Nordend",
    "Westend-Nord": "Westend", "Westend-Süd": "Westend",
    "Sachsenhausen-N.": "Sachsenhausen", "Sachsenhausen-S.": "Sachsenhausen",
}
COLORS = 6
out = pathlib.Path(__file__).resolve().parent.parent / "data" / "frankfurt-stadtteile.geojson"

if len(sys.argv) > 1:
    src = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
else:
    with urllib.request.urlopen(SOURCE, timeout=60) as r:
        src = json.load(r)

groups = {}
for f in src["features"]:
    name = f["properties"]["name"]
    groups.setdefault(MERGE.get(name, name), []).append(shape(f["geometry"]).buffer(0))
areas = {name: unary_union(parts).buffer(0.00002).buffer(-0.00002).simplify(0.00004, preserve_topology=True)
         for name, parts in sorted(groups.items())}

# Gierige Färbung: große Stadtteile zuerst, jeder bekommt den ersten Ton, den kein Nachbar hat.
names = sorted(areas, key=lambda n: -areas[n].area)
color = {}
for n in names:
    taken = {color[m] for m in color if areas[n].buffer(0.0003).intersects(areas[m])}
    color[n] = next((c for c in range(COLORS) if c not in taken), len(color) % COLORS)

def rounded(geom):
    def r(c):
        return [r(x) for x in c] if isinstance(c[0], (list, tuple)) else [round(c[0], 5), round(c[1], 5)]
    g = mapping(geom)
    return {"type": g["type"], "coordinates": r(g["coordinates"])}

features = []
for n in sorted(areas):
    geom = areas[n]
    features.append({"type": "Feature", "properties": {"name": n, "c": color[n]}, "geometry": rounded(geom)})
    main = max(geom.geoms, key=lambda g: g.area) if geom.geom_type == "MultiPolygon" else geom
    pt = polylabel(main, 0.0002)
    features.append({"type": "Feature", "properties": {"name": n, "label": 1},
                     "geometry": {"type": "Point", "coordinates": [round(pt.x, 5), round(pt.y, 5)]}})

out.write_text(json.dumps({"type": "FeatureCollection", "attribution": ATTRIBUTION, "features": features},
                          ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
print(f"{out}: {len(areas)} Stadtteile, {out.stat().st_size // 1024} KB, Farben {sorted(set(color.values()))}")
