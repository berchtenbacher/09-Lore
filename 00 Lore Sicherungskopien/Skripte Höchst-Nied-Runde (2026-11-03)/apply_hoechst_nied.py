# Höchst-Nied-Runde (03.11.2026): neue Orte und Geschichten für Höchst und Nied, Nied im Blatt Geo angelegt.
# Aufruf: python3 apply_hoechst_nied.py ein.xlsx aus.xlsx '{"ort-id": ["lat, lon", "genau"], ...}'
# Koordinaten aus Wikimedia-Commons-Kategorien bzw. Objektstandorten der Fotos.
import sys, copy, re, json, unicodedata, openpyxl
from openpyxl.worksheet.datavalidation import DataValidation

TODAY = "2026-11-03"
WP = "https://de.wikipedia.org/wiki/"
GP, PERS, ERF, VER, WEG, SAGE, KIEZ = ("Geschichte & Politik", "Persönlichkeiten", "Erfindungen", "Verbrechen & Skandale",
                                      "Verschwundenes", "Sagen & Legenden", "Kiez-Geschichten")
T1, SW, LO = "Touri 1x1", "Sehenswürdigkeit", "Lokal"
GEO_NEW = [("Nied", "Frankfurt am Main", "frankfurt", "Kreisfreie Stadt Frankfurt am Main", "Hessen")]

# id -> (Name, Koordinaten oder None = aus Argument, Adresse, Bezirk, Genauigkeit)
ORTE = {
    "nied-roemerziegelei": ("Römische Militärziegelei Nied", None, "Nied, zwischen Nidda und Main", "Nied", "ungefähr"),
    "nied-eisenbahnbruecke": ("Eisenbahnbrücke Nied (1838)", "50.10420, 8.56556", "Nidda, Taunus-Eisenbahn", "Nied", "genau"),
    "nied-alte-niddabruecke": ("Alte Niddabrücke", "50.10044, 8.56400", "Bolongarostraße", "Nied", "genau"),
    "nied-ausbesserungswerk": ("Ausbesserungswerk und Eisenbahnersiedlung Nied", "50.10640, 8.58489", "Oeserstraße", "Nied", "ungefähr"),
    "nied-woerthspitze": ("Wörthspitze (Niddamündung)", "50.10000, 8.55417", "Mündung der Nidda in den Main", "Nied", "genau"),
    "hoechst-synagoge": ("Ettinghausenplatz (ehemalige Synagoge)", None, "Ettinghausenplatz / Leverkuser Straße", "Höchst", "Straße"),
    "hoechst-dalberger-haus": ("Dalberger Haus", None, "Bolongarostraße 186", "Höchst", "Straße"),
    "hoechst-antoniter": ("Antoniterkloster Höchst", None, "Bolongarostraße 137–139", "Höchst", "Straße"),
    "hoechst-mainufer": ("Höchster Mainufer", "50.09930, 8.54400", "Mainberg / Höchster Mainufer", "Höchst", "ungefähr"),
}

NEW = [
    dict(ort="nied-roemerziegelei", Name="Die Ziegelei der Legionen", Kategorie=f"{GP}, {WEG}", Tags="Mittelalter & früher, Architektur", Flag=SW,
         teaser="Lange vor Frankfurt gab es in Nied Industrie: Ab etwa 83 n. Chr. brannten römische Soldaten hier Ziegel für die Kastelle am Limes. "
                "Bei Grabungen 1891 legte Georg Wolff Brennöfen, Schlämmgruben, Werkstätten und Schuppen frei. "
                "Die Ziegel tragen die Stempel vieler Truppen, darunter der 22. Legion aus Mainz, Nied war die Zentralziegelei der Region.",
         quellen=["Historisches Museum Frankfurt | https://historisches-museum-frankfurt.de/iart/os-download-object/34602",
                  "Kastell Höchst (Wikipedia-Spiegel) | https://de-academic.com/dic.nsf/dewiki/2446771"],
         zeitraum="ca. 83 bis 2. Jh.", jahr=83, status="Prüfen"),
    dict(ort="nied-eisenbahnbruecke", Name="Die Brücke von 1838", Kategorie=f"{GP}, {ERF}", Tags="19. Jahrhundert, Verkehr, Architektur", Flag=SW,
         teaser="1838 baute Paul Camille von Denis für die Taunus-Eisenbahn Frankfurt–Wiesbaden eine Steinbrücke mit drei Bögen über die Nidda. "
                "Seit 1839 fahren hier Züge, inzwischen ICEs und S-Bahnen. Lange galt sie als älteste noch befahrene Eisenbahnbrücke Deutschlands, "
                "heute ist sie die zweitälteste, knapp hinter einer Brücke bei Wurzen in Sachsen.",
         quellen=["Structurae | https://structurae.net/de/bauwerke/20016999", "Deutsche Bahn | https://www.deutschebahn.com/de/presse/suche_Medienpakete/Das-sind-Deutschlands-spektakulaerste-Eisenbahnbruecken-6854290"],
         zeitraum="seit 1838", jahr=1838, status="Entwurf"),
    dict(ort="nied-alte-niddabruecke", Name="Napoleon an der Nidda", Kategorie=f"{SAGE}, {GP}", Tags="19. Jahrhundert, Verkehr", Flag=LO,
         teaser="Die steinerne Brücke von Alt-Nied trägt seit 1824 die alte Straße nach Mainz über die Nidda. "
                "Im Ort erzählt man, Napoleon sei hier geritten; auf dem Rückzug nach der Völkerschlacht zog seine Armee im Herbst 1813 über diese Straße nach Mainz, "
                "damals über den Vorgängerbau. Unter der Brücke führt ein Weg zur Wörthspitze.",
         quellen=["ich-geh-wandern.de | https://www.ich-geh-wandern.de/frankfurt-nied", "Komoot | https://www.komoot.com/tour/166284599"],
         zeitraum="1813 / 1824", jahr=1824, status="Prüfen"),
    dict(ort="nied-ausbesserungswerk", Name="Die Stadt der Lokschlosser", Kategorie=f"{KIEZ}, {GP}", Tags="Kaiserreich, Verkehr, Architektur", Flag=LO,
         teaser="1918 eröffnete die Preußische Staatsbahn in Nied ein Ausbesserungswerk für Dampfloks. Für die Arbeiter entstand daneben eine eigene Siedlung "
                "mit Reihenhäusern und Gärten. Sie ist eine der wenigen Eisenbahnersiedlungen in Deutschland, die fast im Original erhalten sind, und steht unter Denkmalschutz.",
         quellen=["ich-geh-wandern.de | https://www.ich-geh-wandern.de/frankfurt-nied", "Komoot | https://www.komoot.com/highlight/665476"],
         zeitraum="seit 1918", jahr=1918, status="Prüfen"),
    dict(ort="nied-woerthspitze", Name="Wo die Nidda den Main trifft", Kategorie=KIEZ, Tags="Natur", Flag=LO,
         teaser="An der Wörthspitze fließt die Nidda nach rund 90 Kilometern vom Vogelsberg in den Main. Die schmale Landzunge zwischen Höchst und Nied "
                "ist ein stiller Aussichtspunkt mit Blick auf die Höchster Altstadt und den Industriepark auf der anderen Seite.",
         quellen=["Komoot | https://www.komoot.com/tour/166284599"],
         zeitraum="", jahr=None, status="Prüfen"),
    dict(ort="hoechst-synagoge", Name="Der Bunker auf der Synagoge", Kategorie=f"{GP}, {WEG}", Tags="NS-Zeit, Jüdisches Leben, Erinnerung", Flag=SW,
         teaser="1905 weihte die jüdische Gemeinde Höchst ihre Synagoge ein. Im November 1938 wurde sie zerstört, die Reste abgetragen, "
                "und 1940 bis 1942 bauten die Nazis genau an diese Stelle einen Hochbunker. Bei Grabungen kamen die Fundamente wieder zum Vorschein. "
                "Heute zeigen Fernrohre auf dem Platz die Synagoge virtuell an ihrem alten Ort.",
         quellen=["Journal Frankfurt | https://www.journal-frankfurt.de/journal_news/Stadtleben-2/Grabungsarbeiten-am-Ettingshausen-Platz-Teile-der-zerstoerten-Synagoge-in-Hoechst-gefunden-35732.html",
                  "Jüdische Allgemeine | https://www.juedische-allgemeine.de/gemeinden/fernrohre-in-die-vergangenheit/",
                  "Visit Frankfurt | https://visitfrankfurt.travel/en/poi/ettingausenplatz-/-the-virtual-synagogue-of-hoechst"],
         zeitraum="1905–1938", jahr=1938, status="Prüfen"),
    dict(ort="hoechst-mainufer", Name="Die Schlacht bei Höchst", Kategorie=GP, Tags="Frühe Neuzeit", Flag=LO,
         teaser="Am 20. Juni 1622 wollte Christian von Braunschweig mit seinem protestantischen Heer bei Höchst über den Main. "
                "Während Tillys Truppen der Katholischen Liga angriffen, brach die eilig gebaute Brücke, nachdem erst ein Teil übergesetzt hatte. "
                "Viele Soldaten und Pferde ertranken, Tilly siegte, Christian entkam mit dem Rest seiner Armee.",
         quellen=["Wikipedia (en) | https://en.wikipedia.org/wiki/Battle_of_H%C3%B6chst", "Deutsche Biographie (Tilly) | https://www.deutsche-biographie.de/sfz82718.html"],
         zeitraum="1622", jahr=1622, status="Prüfen"),
    dict(ort="industriepark-hoechst", Name="Medizin aus der Farbenfabrik", Kategorie=f"{ERF}, {GP}", Tags="Kaiserreich, Wissenschaft", Flag=LO,
         teaser="Die Farbwerke Hoechst wurden zur Apotheke der Welt: 1894 brachten sie das Diphtherie-Heilserum nach Emil von Behring in großen Mengen auf den Markt, "
                "1910 Paul Ehrlichs Syphilis-Mittel Salvarsan, den Beginn der Chemotherapie. 1923 stellte Hoechst als erste deutsche Firma Insulin her.",
         quellen=["Industriepark Höchst | https://industriepark-hoechst.com/en/stp/site/history/", "Pharmazeutische Zeitung | https://www.pharmazeutische-zeitung.de/magazin-41-2001/"],
         zeitraum="1894–1923", jahr=1910, status="Entwurf"),
    dict(ort="hoechst-dalberger-haus", Name="Das Haus des Erzbischofs", Kategorie=GP, Tags="Frühe Neuzeit, Architektur", Flag=LO,
         teaser="1582 entstand das Fachwerkhaus für den Mainzer Amtmann Hartmut von Cronberg, 1586 kaufte es der Mainzer Erzbischof Wolfgang von Dalberg. "
                "Heute verkauft hier die Höchster Porzellanmanufaktur, im Keller liegt ein kleines Museum.",
         quellen=["Wikipedia (en), Höchst | https://en.wikipedia.org/wiki/H%C3%B6chst_(Frankfurt_am_Main)", "In Your Pocket | https://www.inyourpocket.com/frankfurt/dalberger-house_23780v"],
         zeitraum="seit 1582", jahr=1582, status="Entwurf"),
    dict(ort="hoechst-antoniter", Name="Die Mönche mit dem Schweineglöckchen", Kategorie=f"{GP}, {WEG}", Tags="Mittelalter & früher, Religion", Flag=LO,
         teaser="Neben der Justinuskirche hatten die Antoniter im 15. Jahrhundert ein Kloster. Der Orden pflegte Kranke mit dem „Antoniusfeuer“, "
                "einer Vergiftung durch Mutterkorn im Brot, und durfte seine Schweine frei durch die Gassen laufen lassen. An der Bolongarostraße stehen noch Häuser der Anlage aus dem 15. Jahrhundert.",
         quellen=["Wikipedia (en), History of Höchst | https://en.wikipedia.org/wiki/History_of_H%C3%B6chst_am_Main"],
         zeitraum="15. Jh.", jahr=1441, status="Prüfen"),
    dict(ort="bolongaro", Name="Das Ende der Stadt Höchst", Kategorie=f"{GP}, {KIEZ}", Tags="Weimarer Republik", Flag=LO,
         teaser="Höchst war eine eigene Stadt, mit Rathaus im Bolongaropalast. 1928 wurde sie mit Sindlingen, Unterliederbach und Zeilsheim nach Frankfurt eingemeindet. "
                "Viele Höchster nehmen das bis heute übel und sagen: Ich wohne in Höchst, nicht in Frankfurt.",
         quellen=["Wikipedia (en) | https://en.wikipedia.org/wiki/H%C3%B6chst_(Frankfurt_am_Main)"],
         zeitraum="1928", jahr=1928, status="Prüfen"),
]


def slug(s):
    s = s.lower().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def main(src, dst, coords):
    for k, (co, gen) in coords.items():
        n, _, adr, bez, _ = ORTE[k]; ORTE[k] = (n, co, adr, bez, gen)
    wb = openpyxl.load_workbook(src)
    E, O, G = wb["Frankfurt"], wb["Orte"], wb["Geo"]
    last = lambda ws: max(r for r in range(1, ws.max_row + 1) if ws.cell(r, 1).value)
    # Geo: vor der Notizzeile einfügen, falls Bezirk fehlt
    geo = {G.cell(r, 1).value for r in range(2, G.max_row + 1)}
    for g in GEO_NEW:
        if g[0] in geo: continue
        r = last(G) + 1
        for c in range(1, 7): G.cell(r, c)._style = copy.copy(G.cell(r - 1, c)._style)
        for c, v in enumerate(g, 1): G.cell(r, c, v)
        G.cell(r, 6, f"=COUNTIF(Frankfurt!$P$2:$P$2993,A{r})")
    COLS = {c.value: c.column for c in E[1] if c.value}
    orow = {O.cell(r, 1).value: r for r in range(2, last(O) + 1) if O.cell(r, 1).value}
    for k, (name, co, adr, bez, gen) in ORTE.items():
        assert co, k
        if k in orow: r = orow[k]
        else:
            r = last(O) + 1; orow[k] = r
            for c in range(1, 8): O.cell(r, c)._style = copy.copy(O.cell(r - 1, c)._style)
            O.cell(r, 7, f"=COUNTIF(Frankfurt!$C$2:$C$2993,A{r})")
        for c, v in zip(range(1, 7), [k, name, co, adr, bez, gen]): O.cell(r, c, v)
    place = {O.cell(r, 1).value: [O.cell(r, c).value for c in range(1, 7)] for r in range(2, last(O) + 1) if O.cell(r, 1).value}
    tags = {wb["Tags"].cell(i, 1).value for i in range(2, wb["Tags"].max_row + 1)}
    cats = {wb["Kategorien"].cell(i, 1).value for i in range(2, wb["Kategorien"].max_row + 1)}
    ids = {E.cell(r, 1).value for r in range(2, last(E) + 1)}
    style = last(E); r = style + 1
    for d in NEW:
        assert not {t.strip() for t in d["Tags"].split(",")} - tags, d["Tags"]
        assert not {t.strip() for t in d["Kategorie"].split(",")} - cats, d["Kategorie"]
        p = place[d["ort"]]
        sid = f"{d['ort']}-{slug(d['Name'])}"[:80]; assert sid not in ids, sid; ids.add(sid)
        for c in range(1, E.max_column + 1): E.cell(r, c)._style = copy.copy(E.cell(style, c)._style)
        vals = {"ID": sid, "Name": d["Name"], "Ort-ID": d["ort"], "Ort": f'=IFERROR(INDEX(Orte!$B$2:$B$2000,MATCH(C{r},Orte!$A$2:$A$2000,0)),"")',
                "Koordinaten": p[2], "Kategorie": d["Kategorie"], "Tags": d["Tags"], "Flag": d["Flag"], "Teaser Text": d["teaser"],
                "Quellen": "\n".join(d["quellen"]), "Zeitraum": d["zeitraum"] or None, "Jahr": d["jahr"], "Adresse": p[3], "Bezirk": p[4],
                "Region": "frankfurt", "Genauigkeit Koordinaten": p[5], "Status": d["status"], "Autor": "claude", "Aktualisiert": TODAY}
        for k, v in vals.items(): E.cell(r, COLS[k], v)
        r += 1
    have = {str(dv.sqref).split(":")[0][:1] for dv in E.data_validations.dataValidation}
    for col, f in [("C", "Orte!$A$2:$A$2000"), ("H", "Flag!$A$2:$A$4"), ("P", "Geo!$A$2:$A$100"), ("R", '"genau,Straße,ungefähr"'), ("S", "Status!$A$2:$A$6")]:
        if col not in have:
            dv = DataValidation(type="list", formula1=f, allow_blank=True); E.add_data_validation(dv); dv.add(f"{col}2:{col}1233")
    wb.save(dst)
    print("Orte", len(ORTE), "neu", len(NEW), "letzte Zeile", r - 1)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], {k: tuple(v) for k, v in json.loads(sys.argv[3]).items()})
