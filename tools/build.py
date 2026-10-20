"""Baut eine Einzeldatei (dist/lore-map-frankfurt.html), die per Doppelklick ohne Webserver läuft."""
import json, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
html = (root / "index.html").read_text(encoding="utf-8")
data = json.loads((root / "data" / "frankfurt.geojson").read_text(encoding="utf-8"))
blob = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
out = html.replace("/*LORE_DATA*/", blob, 1)
(root / "dist").mkdir(exist_ok=True)
(root / "dist" / "lore-map-frankfurt.html").write_text(out, encoding="utf-8")
print("dist/lore-map-frankfurt.html", len(out) // 1024, "KB")
