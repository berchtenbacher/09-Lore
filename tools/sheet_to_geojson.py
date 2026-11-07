"""Lore-Tabelle (Excel) → GeoJSON für die Karte.

Liest die Tabelle nur, verändert sie nie. Ein Feature pro Ort (Blatt „Orte“), die Geschichten
aus „Einträge“ hängen über die Ort-ID daran.

    python3 tools/sheet_to_geojson.py                                    # alle „Lore Tags, Kategorien und Einträge *.xlsx“
    python3 tools/sheet_to_geojson.py "Lore Tags, Kategorien und Einträge Berlin.xlsx"  # nur diese Datei
    python3 tools/sheet_to_geojson.py --region frankfurt                 # nur eine Region schreiben
    python3 tools/sheet_to_geojson.py --out data                         # Zielordner

Die Geschichten stehen im Blatt „Einträge“ oder in einem Blatt mit dem Namen der Stadt (z. B. „Frankfurt“).

Pro Region (Spalte „Region“) entsteht data/<region>.geojson. „Verworfen“ fehlt auf der Karte, alles
andere wird gezeigt, „Prüfen“ und „Idee“ markiert. Prototyp: Ideen sind vorerst mit auf der Karte,
mit --ohne-ideen fehlen sie wieder. Braucht openpyxl (pip install openpyxl).
"""
import argparse, json, pathlib, re, sys, unicodedata
from collections import Counter, defaultdict

from bildlinks import Bildinfos, finish, story_images  # Spalten „Bild 1 (Hauptbild)“ und „Bild 2“

try:
    import openpyxl
except ImportError:
    sys.exit("Bitte zuerst openpyxl installieren: pip install openpyxl")

HIDDEN_STATUS = {"Verworfen"}
MIN_TAG = 3  # Tags mit weniger Geschichten pro Region erscheinen nicht als Filter und nicht an den Geschichten
FLAG_IMPORTANCE = {"Touri 1x1": 3, "Sehenswürdigkeit": 2, "Lokal": 1}
# Spalte „Vorgeschlagen“ (Ja/Nein): eigene Punktkategorie auf der Karte, gleiche Priorität wie Touri 1x1.
SUGGESTED_COLUMN = "Vorgeschlagen"


def yes(v):
    """Ja/Nein-Zelle: „Ja“, „j“, „x“, „1“, WAHR zählen als ja, alles andere (auch leer) als nein."""
    if v is True:
        return True
    return text(v).lower() in {"ja", "j", "x", "1", "y", "yes", "wahr", "true"}


def rows(ws):
    """Zeilen als Dicts über die Kopfzeile; leere Zeilen und Spalten ohne Überschrift fallen weg."""
    it = ws.iter_rows(values_only=True)
    head = [str(h).strip() if h is not None else None for h in next(it)]
    for r in it:
        d = {h: v for h, v in zip(head, r) if h}
        if any(v not in (None, "") for v in d.values()):
            yield d


def text(v):
    if v is None:
        return ""
    if hasattr(v, "isoformat"):
        return v.isoformat()[:10]
    return str(v).strip()


def split_list(v):
    return [s.strip() for s in re.split(r"[,;\n]", text(v)) if s.strip()]


def coords(v):
    """„52.51750, 13.40300“ (lat, lon) → [lon, lat]."""
    m = re.match(r"^\s*(-?\d+(?:\.\d+)?)\s*[,;]\s*(-?\d+(?:\.\d+)?)\s*$", text(v))
    if not m:
        return None
    lat, lon = float(m.group(1)), float(m.group(2))
    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
        return None
    return [round(lon, 6), round(lat, 6)]


def sources(v):
    out = []
    for line in text(v).splitlines():
        line = line.strip()
        if not line:
            continue
        if "|" in line:
            label, url = (s.strip() for s in line.split("|", 1))
        else:
            label, url = "", line
        if url.startswith("http"):
            out.append({"label": label or re.sub(r"^https?://(www\.)?([^/]+).*", r"\2", url), "url": url})
    return out


def paragraphs(v):
    return [p.strip() for p in re.split(r"\n\s*\n|\r\n\s*\r\n", text(v)) if p.strip()]


ROOT = pathlib.Path(__file__).resolve().parent.parent
PATTERN = "Lore Tags, Kategorien und Einträge *.xlsx"


def tables():
    """Alle Lore-Tabellen im Projektordner. macOS speichert Umlaute zerlegt, deshalb wird normalisiert verglichen."""
    return sorted(f for f in ROOT.glob("*.xlsx")
                  if unicodedata.normalize("NFC", f.name).startswith(PATTERN.split("*")[0]) and not f.name.startswith("~$"))


def entries_sheet(wb):
    """Blatt mit den Geschichten: „Einträge“ oder das erste Blatt mit den Spalten ID und Ort-ID."""
    if "Einträge" in wb.sheetnames:
        return wb["Einträge"]
    for ws in wb.worksheets:
        head = [str(c).strip() if c is not None else "" for c in next(ws.iter_rows(max_row=1, values_only=True), ())]
        if "ID" in head and "Ort-ID" in head:
            return ws
    sys.exit("Kein Blatt mit Geschichten gefunden (erwartet „Einträge“ oder ein Blatt mit den Spalten ID und Ort-ID).")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("xlsx", nargs="*", help=f"Excel-Dateien; ohne Angabe alle „{PATTERN}“ im Projektordner")
    ap.add_argument("--out", default=str(ROOT / "data"))
    ap.add_argument("--region", help="nur diese Region schreiben, z. B. berlin")
    ap.add_argument("--ohne-ideen", action="store_true", help="Status „Idee“ nicht auf die Karte")
    ap.add_argument("--offline", action="store_true", help="Urheber und Lizenz neuer Bilder nicht bei Commons abfragen")
    args = ap.parse_args()
    files = [pathlib.Path(f) for f in args.xlsx] or tables()
    if not files:
        sys.exit(f"Keine Excel-Datei gefunden ({PATTERN}).")
    infos = Bildinfos(ROOT / "data" / "bildinfos.json", offline=args.offline)
    for f in files:
        if args.ohne_ideen:
            HIDDEN_STATUS.add("Idee")
        convert(f, args.out, args.region, infos)


def convert(xlsx, out_dir, only_region, infos):
    print(f"== {xlsx.name}")

    wb = openpyxl.load_workbook(xlsx, read_only=True, data_only=True)
    sheet = lambda name: wb[name] if name in wb.sheetnames else None
    warn = []
    tail = unicodedata.normalize("NFC", xlsx.stem).split("Einträge")[-1].strip().lower()
    default_region = tail.split()[0] if tail else "berlin"

    # Stammdaten: Tag-Gruppen, Reihenfolgen, Geo-Zuordnung
    epochs, topics = [], []
    for r in rows(sheet("Tags")):
        tag, group = text(r.get("Tag")), text(r.get("Gruppe"))
        if not tag:
            continue
        if group == "Epoche":
            epochs.append(tag)
        elif group.startswith("Thema"):
            topics.append(tag)
    categories = [text(r.get("Kategorien")) for r in rows(sheet("Kategorien")) if text(r.get("Kategorien"))]
    geo = {text(r.get("Bezirk")): r for r in rows(sheet("Geo")) if text(r.get("Bezirk"))}

    places = {}
    for r in rows(sheet("Orte")):
        pid = text(r.get("Ort-ID"))
        if not pid:
            continue
        c = coords(r.get("Koordinaten"))
        if not c:
            warn.append(f"Ort {pid}: Koordinaten fehlen oder sind ungültig ({text(r.get('Koordinaten'))!r})")
        places[pid] = {"id": pid, "title": text(r.get("Ort")), "coord": c, "address": text(r.get("Adresse")),
                       "bezirk": text(r.get("Bezirk")), "precision": text(r.get("Genauigkeit")) or "genau", "stories": []}

    if SUGGESTED_COLUMN not in [str(c).strip() for c in next(entries_sheet(wb).iter_rows(max_row=1, values_only=True)) if c]:
        warn.append(f"Spalte „{SUGGESTED_COLUMN}“ fehlt im Blatt mit den Geschichten, alle Einträge gelten als nicht vorgeschlagen")
    seen, skipped = set(), Counter()
    for n, r in enumerate(rows(entries_sheet(wb)), start=2):
        sid = text(r.get("ID"))
        status = text(r.get("Status")) or "Entwurf"
        if not sid:
            warn.append(f"Zeile {n}: keine ID, übersprungen")
            continue
        if status in HIDDEN_STATUS:
            skipped[status] += 1
            continue
        if sid in seen:
            warn.append(f"{sid}: ID kommt doppelt vor, zweite Zeile übersprungen")
            continue
        seen.add(sid)
        pid = text(r.get("Ort-ID")) or sid
        if pid not in places:
            # Ort noch nicht im Blatt „Orte“: aus der Zeile selbst anlegen.
            c = coords(r.get("Koordinaten"))
            warn.append(f"{sid}: Ort-ID {pid!r} fehlt im Blatt „Orte“, Ort aus der Zeile übernommen")
            places[pid] = {"id": pid, "title": text(r.get("Ort")) or text(r.get("Name")), "coord": c,
                           "address": text(r.get("Adresse")), "bezirk": text(r.get("Bezirk")),
                           "precision": text(r.get("Genauigkeit Koordinaten")) or "genau", "stories": []}
        p = places[pid]
        region = text(r.get("Region")).lower()
        if not region:
            # Ohne Region gilt die Stadt aus dem Dateinamen, sonst würde z. B. eine Frankfurter Zeile berlin.geojson überschreiben.
            region = default_region
            warn.append(f"{sid}: Spalte „Region“ leer, als {region} übernommen")
        p.setdefault("region", region)
        tags = split_list(r.get("Tags"))
        unknown = [t for t in tags if t not in epochs and t not in topics]
        if unknown:
            warn.append(f"{sid}: Tags nicht im Blatt „Tags“: {', '.join(unknown)}")
        cats = split_list(r.get("Kategorie"))
        bad = [c for c in cats if categories and c not in categories]
        if bad:
            warn.append(f"{sid}: Kategorie nicht im Blatt „Kategorien“: {', '.join(bad)}")
        flag = text(r.get("Flag")) or "Lokal"
        if flag not in FLAG_IMPORTANCE:
            warn.append(f"{sid}: unbekanntes Flag {flag!r}, als Lokal behandelt")
        year = r.get("Jahr")
        p["stories"].append({
            "id": sid,
            "title": text(r.get("Name")),
            "teaser": text(r.get("Teaser Text")) or ("Idee, noch ohne Text." if status == "Idee" else ""),
            "story": paragraphs(r.get("Volltext")),
            "categories": cats,
            "epochs": [t for t in tags if t in epochs],
            "tags": [t for t in tags if t not in epochs],
            "flag": flag if flag in FLAG_IMPORTANCE else "Lokal",
            "importance": FLAG_IMPORTANCE.get(flag, 1),
            "period": text(r.get("Zeitraum")),
            "year": int(year) if isinstance(year, (int, float)) else None,
            "status": status,
            "note": text(r.get("Prüfen / unsicher")),
            "sources": sources(r.get("Quellen")),
            "imageQuery": text(r.get("Bildsuche")),
            # Bilder aus der Tabelle, Hauptbild zuerst. Gehen in der App vor den Vorschlägen aus data/images.json.
            "images": story_images(r, sid, text(r.get("Name")), infos, warn),
            "suggested": yes(r.get(SUGGESTED_COLUMN)),
            "photosImportant": text(r.get("Fotos wichtig j/n?")).lower().startswith("j"),
            "author": text(r.get("Autor")),
            "updated": text(r.get("Aktualisiert")),
        })

    # Urheber und Lizenz der Commons-Bilder (einmal abfragen, dann aus data/bildinfos.json)
    infos.fetch()
    if infos.failed:
        warn.append(f"Commons nicht erreichbar ({infos.failed}): neue Bilder ohne Urheber und Lizenz, später nochmal laufen lassen")
        infos.failed = None
    for p in places.values():
        for s in p["stories"]:
            s["images"] = finish(s["images"], infos, warn, s["id"])

    by_region = defaultdict(list)
    for p in places.values():
        if not p["stories"]:
            continue
        if not p["coord"]:
            warn.append(f"Ort {p['id']}: ohne Koordinaten, nicht auf der Karte ({len(p['stories'])} Geschichten)")
            continue
        g = geo.get(p["bezirk"], {})
        # Wichtigste Geschichte zuerst, sonst Reihenfolge der Tabelle.
        p["stories"].sort(key=lambda s: -s["importance"])
        by_region[p["region"]].append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": p["coord"]},
            "properties": {
                "id": p["id"],
                "title": p["title"],
                "importance": max(s["importance"] for s in p["stories"]),
                "suggested": any(s["suggested"] for s in p["stories"]),
                "place": {"stadtteil": p["bezirk"], "stadt": text(g.get("Stadt / Ort")) or p["region"].title(),
                          "kreis": text(g.get("Kreis")), "bundesland": text(g.get("Bundesland"))},
                "address": p["address"],
                "precision": p["precision"],
                "stories": p["stories"],
            },
        })

    out = pathlib.Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    for region, feats in sorted(by_region.items()):
        if only_region and region != only_region:
            continue
        feats.sort(key=lambda f: f["properties"]["id"])
        tc = Counter(t for f in feats for s in f["properties"]["stories"] for t in s["tags"])
        rare = {t for t, n in tc.items() if n < MIN_TAG}
        for f in feats:
            for s in f["properties"]["stories"]:
                s["tags"] = [t for t in s["tags"] if t not in rare]
        if rare:
            print(f"{region}: Tags mit weniger als {MIN_TAG} Geschichten ausgeblendet: {', '.join(sorted(rare))}")
        used = lambda key: {v for f in feats for s in f["properties"]["stories"] for v in s[key]}
        fc = {
            "type": "FeatureCollection",
            # Reihenfolge der Filter wie in den Stammdaten-Blättern
            "lore": {
                "categories": [c for c in categories if c in used("categories")] + sorted(used("categories") - set(categories)),
                "epochs": [e for e in epochs if e in used("epochs")],
                "tags": [t for t in topics if t in used("tags")] + sorted(used("tags") - set(topics)),
                "source": xlsx.name,
            },
            "features": feats,
        }
        path = out / f"{region}.geojson"
        path.write_text(json.dumps(fc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        n = sum(len(f["properties"]["stories"]) for f in feats)
        status = Counter(s["status"] for f in feats for s in f["properties"]["stories"])
        sug = sum(f["properties"]["suggested"] for f in feats)
        print(f"{path}: {len(feats)} Orte, {n} Geschichten ({', '.join(f'{v} {k}' for k, v in status.most_common())})"
              + (f", {sug} Orte vorgeschlagen" if sug else ""))
    if skipped:
        print("Nicht auf der Karte: " + ", ".join(f"{v} × {k}" for k, v in skipped.items()))
    if warn:
        print(f"\n{len(warn)} Hinweise:")
        for w in warn:
            print("  - " + w)


if __name__ == "__main__":
    main()
