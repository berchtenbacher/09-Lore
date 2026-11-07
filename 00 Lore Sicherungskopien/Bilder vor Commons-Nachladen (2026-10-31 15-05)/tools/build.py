"""Baut Einzeldateien, die per Doppelklick ohne Webserver laufen:
dist/sagenhaft.html mit allen Städten und dist/sagenhaft-<stadt>.html mit jeweils nur einer Stadt.
Daten und alle lokalen Bibliotheken (Zeilen mit <!--INLINE-->) werden eingebettet."""
import json, pathlib, re
root = pathlib.Path(__file__).resolve().parent.parent
html = (root / "index.html").read_text(encoding="utf-8")
# Alle Orte aus der REGIONS-Liste in index.html einbetten (id -> GeoJSON).
regions = re.findall(r'\{ id: "([a-z0-9-]+)", name: "[^"]+", file: "([^"]+)"', html)
data = {rid: json.loads((root / f).read_text(encoding="utf-8")) for rid, f in regions if (root / f).exists()}
images_path = root / "data" / "images.json"
images = json.loads(images_path.read_text(encoding="utf-8")) if images_path.exists() else {}
pack = lambda obj: json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

def inline(m):
    path = m.group(1) or m.group(2)
    text = (root / path).read_text(encoding="utf-8")
    if m.group(1):
        return "<style>" + text + "</style>"
    return "<script>" + text.replace("</script", "<\\/script") + "</script>"

base = re.sub(r'<link rel="stylesheet" href="([^"]+)"><!--INLINE-->|<script src="([^"]+)"></script><!--INLINE-->', inline, html)
base = base.replace("/*LORE_IMAGES*/", pack(images), 1)
# Stadtteilflächen (REGIONS-Eintrag mit areas: "...") je Region einbetten.
area_files = dict(re.findall(r'\{ id: "([a-z0-9-]+)",[^}]*?areas: "([^"]+)"', html))
areas = {rid: json.loads((root / f).read_text(encoding="utf-8")) for rid, f in area_files.items() if (root / f).exists()}
(root / "dist").mkdir(exist_ok=True)
outputs = {"sagenhaft.html": data}
outputs.update({f"sagenhaft-{rid}.html": {rid: fc} for rid, fc in data.items()})
for name, subset in outputs.items():
    out = base.replace("/*LORE_DATA*/", pack(subset), 1)
    out = out.replace("/*LORE_AREAS*/", pack({rid: a for rid, a in areas.items() if rid in subset}), 1)
    (root / "dist" / name).write_text(out, encoding="utf-8")
    print(f"dist/{name}", len(out) // 1024, "KB")
