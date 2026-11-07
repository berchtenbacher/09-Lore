"""Bildlinks aus der Lore-Tabelle (Spalten „Bild 1 (Hauptbild)“ und „Bild 2“) → Bilder an der Geschichte.

Eine Zelle enthält einen Link, am einfachsten zur Bilddatei auf Wikimedia Commons. Es geht jeder Link,
in dem der Dateiname steckt, z. B.
    https://commons.wikimedia.org/wiki/File:Hessendenkmal_2016.jpg
    https://de.wikipedia.org/wiki/Saalhof#/media/Datei:Frankfurt_Am_Main-Saalhof-Ansicht_vom_Eisernen_Steg.jpg
    https://commons.wikimedia.org/wiki/Category:Paulskirche_(Frankfurt)#/media/File:Altstadt,_60547_Frankfurt.jpg
    https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/Datei.jpg/800px-Datei.jpg
Angezeigt wird ein Vorschaubild mit 800 px Breite. Urheber und Lizenz holt das Skript einmal von Commons
und merkt sie sich in data/bildinfos.json (ohne Internet: Hinweis „siehe Wikimedia Commons“).

Andere Bilder (nicht Commons) oder eigene Angaben: „Link | Urheber | Lizenz“ in einer Zelle,
z. B. „https://example.org/bild.jpg | Stadtarchiv Frankfurt | CC BY 4.0“. Eigene Angaben gehen vor.
"""
import html, json, os, pathlib, re, time, urllib.parse, urllib.request

WIDTH = 800
API = "https://commons.wikimedia.org/w/api.php"
FREE = re.compile(r"^(cc0|public domain|pd|cc by(-sa)?( \d\.\d)?)", re.I)

FILE_PATTERNS = [
    r"/media/(?:File|Datei|Image|Bild):([^?#&]+)",
    r"/wiki/(?:File|Datei|Image|Bild):([^?#&]+)",
    r"(?:Special:FilePath|Spezial:Dateipfad)/([^?#&]+)",
    r"upload\.wikimedia\.org/wikipedia/commons/thumb/[0-9a-f]/[0-9a-f]{2}/([^/?#]+)/",
    r"upload\.wikimedia\.org/wikipedia/commons/[0-9a-f]/[0-9a-f]{2}/([^/?#]+)",
]


def slot_of(header):
    """Spaltenkopf → 1 (Hauptbild), 2 (zweites Bild) oder None."""
    h = re.sub(r"\s+", " ", (header or "").strip().lower())
    if h == "bildlink" or h.startswith("bild 1") or h.startswith("bildlink 1") or h == "hauptbild":
        return 1
    if h.startswith("bild 2") or h.startswith("bildlink 2"):
        return 2
    return None


def commons_file(link):
    """Dateiname auf Commons (mit Unterstrichen, dekodiert) oder None."""
    for pat in FILE_PATTERNS:
        m = re.search(pat, link)
        if m:
            name = urllib.parse.unquote(m.group(1)).replace(" ", "_").strip("_")
            return name[0].upper() + name[1:] if name else None
    return None


def parse_cell(value):
    """„Link“ oder „Link | Urheber | Lizenz“ → dict oder None."""
    v = str(value or "").strip()
    if not v:
        return None
    parts = [p.strip() for p in v.split("|")]
    return {"link": parts[0], "author": parts[1] if len(parts) > 1 else "", "license": parts[2] if len(parts) > 2 else ""}


def strip_html(s):
    s = re.sub(r"<[^>]+>", "", s or "")
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


class Bildinfos:
    """Merkt sich Urheber, Lizenz und Vorschau-URL je Commons-Datei in data/bildinfos.json."""

    def __init__(self, path, offline=False):
        self.path = pathlib.Path(path)
        self.offline = offline
        self.data = json.loads(self.path.read_text(encoding="utf-8")) if self.path.exists() else {}
        self.wanted = set()
        self.failed = None

    def want(self, name):
        if name not in self.data:
            self.wanted.add(name)

    def fetch(self):
        """Fehlende Dateien in Paketen zu 50 bei Commons abfragen. Fehler werden gemeldet, nicht geworfen."""
        todo = sorted(self.wanted - set(self.data))
        if not todo or self.offline:
            return
        contact = os.environ.get("LORE_CONTACT", "")
        ua = f"LoreMap-Prototyp/0.2 (sheet_to_geojson; {contact or 'kein Kontakt gesetzt'})"
        for i in range(0, len(todo), 50):
            chunk = todo[i:i + 50]
            q = {"action": "query", "format": "json", "formatversion": "2", "prop": "imageinfo",
                 "iiprop": "url|extmetadata|size", "iiurlwidth": str(WIDTH),
                 "iiextmetadatafilter": "Artist|LicenseShortName|LicenseUrl|ObjectName|ImageDescription",
                 "titles": "|".join("File:" + n for n in chunk)}
            req = urllib.request.Request(API + "?" + urllib.parse.urlencode(q), headers={"User-Agent": ua})
            try:
                with urllib.request.urlopen(req, timeout=20) as r:
                    res = json.load(r)
            except Exception as e:  # kein Internet, Sperre, Zeitüberschreitung
                self.failed = f"{type(e).__name__}: {e}"
                break
            norm = {n["to"]: n["from"] for n in res.get("query", {}).get("normalized", [])}
            for page in res.get("query", {}).get("pages", []):
                name = norm.get(page["title"], page["title"]).split(":", 1)[1].replace(" ", "_")
                if page.get("missing") or not page.get("imageinfo"):
                    self.data[name] = {"missing": True}
                    continue
                ii = page["imageinfo"][0]
                md = {k: strip_html(v.get("value", "")) for k, v in ii.get("extmetadata", {}).items()}
                self.data[name] = {
                    "thumb": ii.get("thumburl") or ii.get("url"), "page": ii.get("descriptionurl"),
                    "width": ii.get("width"), "author": md.get("Artist", ""), "license": md.get("LicenseShortName", ""),
                    "licenseUrl": md.get("LicenseUrl", ""), "title": md.get("ObjectName", ""),
                    "description": md.get("ImageDescription", "")[:300],
                }
            time.sleep(1)
        self.path.write_text(json.dumps(self.data, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")


def story_images(row, sid, title, infos, warn):
    """Bilder einer Tabellenzeile in Reihenfolge Bild 1, Bild 2. Commons-Angaben werden in finish() ergänzt."""
    cells = sorted((slot_of(k), v) for k, v in row.items() if slot_of(k) and str(v or "").strip())
    out = []
    for slot, value in cells:
        c = parse_cell(value)
        link = c["link"]
        if not link.startswith("http"):
            warn.append(f"{sid}: Bild {slot} ist kein Link ({link[:60]!r})")
            continue
        name = commons_file(link)
        if not name and re.search(r"wiki(media|pedia)\.org", link):
            warn.append(f"{sid}: Bild {slot} zeigt auf eine Seite, nicht auf eine Bilddatei (Link mit „File:“ oder „Datei:“ nehmen)")
            continue
        if name:
            infos.want(name)
        out.append({"slot": slot, "file": name, "link": link, "author": c["author"], "license": c["license"],
                    "alt": title})
    return out


def finish(images, infos, warn, sid):
    """Platzhalter aus story_images() → fertige Bild-Objekte wie in data/images.json."""
    done = []
    for im in images:
        name = im["file"]
        if name:
            meta = infos.data.get(name, {})
            if meta.get("missing"):
                warn.append(f"{sid}: Bild {im['slot']} gibt es auf Commons nicht ({name})")
                continue
            page = meta.get("page") or "https://commons.wikimedia.org/wiki/File:" + urllib.parse.quote(name)
            url = meta.get("thumb") or ("https://commons.wikimedia.org/wiki/Special:FilePath/"
                                        + urllib.parse.quote(name) + f"?width={WIDTH}")
            lic = im["license"] or meta.get("license", "")
            if lic and not FREE.match(lic):
                warn.append(f"{sid}: Bild {im['slot']} hat die Lizenz {lic!r}, bitte prüfen, ob sie für die Karte passt")
            title = meta.get("title") or re.sub(r"\.\w+$", "", name).replace("_", " ")
            done.append({"title": title, "url": url, "author": im["author"] or meta.get("author", ""), "license": lic,
                         "licenseUrl": "" if im["license"] else meta.get("licenseUrl", ""), "source": page,
                         "sourceLabel": "Wikimedia Commons", "alt": im["alt"], "slot": im["slot"]})
        else:
            if not im["author"]:
                warn.append(f"{sid}: Bild {im['slot']} ist nicht von Commons und hat keinen Urheber („Link | Urheber | Lizenz“)")
            host = re.sub(r"^https?://(www\.)?([^/]+).*", r"\2", im["link"])
            done.append({"title": "", "url": im["link"], "author": im["author"], "license": im["license"],
                         "licenseUrl": "", "source": im["link"], "sourceLabel": host, "alt": im["alt"], "slot": im["slot"]})
    return done
