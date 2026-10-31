#!/usr/bin/env python3
"""Sucht zu den Lore-Items freie Bilder auf Wikimedia Commons und schreibt Vorschläge nach data/images.json.

Aufruf (braucht Internet, nur Python 3 Standardbibliothek):
  python3 tools/fetch_commons.py                 # Vorschläge für alle Items ohne Bilder, bis zu 5 je Item
  python3 tools/fetch_commons.py roemer dom      # nur diese Item-IDs
  python3 tools/fetch_commons.py --max 3 --replace

Ablauf: Commons-Suche (nur Datei-Namensraum, nur Fotos), Lizenz und Urheber kommen aus den Commons-Metadaten.
Zugelassen sind nur CC0, Public Domain, CC BY und CC BY-SA. Alles andere (NC, ND, Fair Use, unklar) wird verworfen.
Die Treffer sind Suchergebnisse: Bitte die Ausgabe kurz durchsehen und unpassende Bilder aus data/images.json löschen.
Danach `python3 tools/build.py`. Eigene Suchbegriffe pro Item: in data/commons_queries.json {"id": "Suchtext"} eintragen.
"""
import json, pathlib, re, sys, time, urllib.parse, urllib.request, html

ROOT = pathlib.Path(__file__).resolve().parent.parent
API = "https://commons.wikimedia.org/w/api.php"
UA = "LoreMapFrankfurt/0.1 (Prototyp; Kontakt ueber das Projekt)"
OK_LICENSES = re.compile(r"^(CC0|Public domain|PD\b|CC BY(-SA)? [0-9.]+( [A-Za-z]+)?$|CC BY(-SA)?( [0-9.]+)?$)", re.I)
BAD_WORDS = re.compile(r"\b(NC|ND|fair use|non-?commercial|no derivatives)\b", re.I)

def api(**params):
    params.update(format="json", formatversion="2")
    req = urllib.request.Request(API + "?" + urllib.parse.urlencode(params), headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def strip_html(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()

def candidates(query, limit=25):
    data = api(action="query", generator="search", gsrsearch=f"{query} filetype:bitmap", gsrnamespace=6, gsrlimit=limit,
               prop="imageinfo", iiprop="url|size|extmetadata|mime", iiurlwidth=960)
    for page in sorted(data.get("query", {}).get("pages", []), key=lambda p: p.get("index", 0)):
        info = (page.get("imageinfo") or [None])[0]
        if not info or info.get("mime") not in ("image/jpeg", "image/png"):
            continue
        meta = info.get("extmetadata", {})
        lic = strip_html(meta.get("LicenseShortName", {}).get("value", ""))
        if not lic or BAD_WORDS.search(lic) or not OK_LICENSES.match(lic):
            continue
        if info.get("width", 0) < 800:
            continue
        author = strip_html(meta.get("Artist", {}).get("value", "")) or "Unbekannt"
        if len(author) > 80:
            author = author[:77] + "…"
        title = page["title"].removeprefix("File:").rsplit(".", 1)[0].replace("_", " ")
        yield {
            "title": strip_html(meta.get("ObjectName", {}).get("value", "")) or title,
            "url": info["thumburl"], "width": info.get("thumbwidth"), "height": info.get("thumbheight"),
            "author": author, "license": lic, "licenseUrl": meta.get("LicenseUrl", {}).get("value", ""),
            "source": info["descriptionurl"], "alt": title,
        }

def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    maxn = int(argv[argv.index("--max") + 1]) if "--max" in argv else 5
    if "--max" in argv:
        args = [a for a in args if a != str(maxn)]
    replace = "--replace" in argv
    features = [f for path in sorted((ROOT / "data").glob("*.geojson"))
                for f in json.loads(path.read_text(encoding="utf-8"))["features"]]
    out_path = ROOT / "data" / "images.json"
    images = json.loads(out_path.read_text(encoding="utf-8")) if out_path.exists() else {}
    q_path = ROOT / "data" / "commons_queries.json"
    queries = json.loads(q_path.read_text(encoding="utf-8")) if q_path.exists() else {}
    for f in features:
        p = f["properties"]
        if args and p["id"] not in args:
            continue
        if images.get(p["id"]) and not replace:
            continue
        q = queries.get(p["id"]) or f'{p["title"]} {p["place"]["stadt"].split(" ")[0]}'
        try:
            found = list(candidates(q))[:maxn]
        except Exception as e:
            print(f'! {p["id"]}: {e}'); continue
        images[p["id"]] = found
        print(f'{p["id"]:20} {len(found)} Bilder  (Suche: {q})')
        for im in found:
            print(f'    {im["license"]:12} {im["title"][:70]}  [{im["source"]}]')
        time.sleep(0.5)
    out_path.write_text(json.dumps(images, ensure_ascii=False, indent=1), encoding="utf-8")
    print("geschrieben:", out_path)

if __name__ == "__main__":
    main(sys.argv[1:])
