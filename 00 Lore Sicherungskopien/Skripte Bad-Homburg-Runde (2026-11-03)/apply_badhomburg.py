# Bad-Homburg-Runde (03.11.2026): Orte präzisiert und getrennt, Einträge überarbeitet und ergänzt.
# Aufruf: python3 apply_badhomburg.py ein.xlsx aus.xlsx
# Koordinaten aus Wikimedia-Commons-Kategorien bzw. Objekt-/Kamerastandorten der Fotos (Stand 03.11.2026).
import sys, copy, openpyxl
from openpyxl.worksheet.datavalidation import DataValidation

TODAY = "2026-11-03"
WP = "https://de.wikipedia.org/wiki/"
GP, PERS, ERF, VER, IKO = "Geschichte & Politik", "Persönlichkeiten", "Erfindungen", "Verbrechen & Skandale", "Frankfurt-Ikonen"
T1, SW, LO = "Touri 1x1", "Sehenswürdigkeit", "Lokal"
BH = "Bad Homburg"

# Orte: id -> (Name, Koordinaten, Adresse, Genauigkeit). Bestehende werden aktualisiert, neue angehängt.
ORTE = {
    "badhomburg-spielbank": ("Spielbank im Kurpark (Brunnensälchen)", "50.22820, 8.62645", "Kisseleffstraße 35", "genau"),
    "badhomburg-kurhaus": ("Kurhaus Bad Homburg", "50.22720, 8.61770", "Louisenstraße 58", "Straße"),
    "badhomburg-dostojewski": ("Dostojewski-Skulptur im Kurhausgarten", "50.22809, 8.61780", "Kurhausgarten", "genau"),
    "badhomburg-dichterhaus": ("Haus Elisabethenstraße / Schwedenpfad", "50.22840, 8.61760", "Ecke Elisabethenstraße / Schwedenpfad", "Straße"),
    "badhomburg-kurpark": ("Elisabethenbrunnen im Kurpark", "50.22620, 8.62929", "Kurpark, Brunnenallee", "genau"),
    "badhomburg-russische-kirche": ("Russische Kirche im Kurpark", "50.22555, 8.62500", "Kurpark, nahe Kaiser-Friedrich-Promenade", "genau"),
    "badhomburg-thai-sala": ("Thai-Sala im Kurpark", "50.23037, 8.62270", "Kurpark", "genau"),
    "badhomburg-tennis": ("Tennisanlage im Kurpark (TC Bad Homburg)", None, "Kurpark", "ungefähr"),
    "badhomburg-golf": ("Golfplatz im Kurpark (Old Course)", None, "Kurpark", "ungefähr"),
    "badhomburg-schloss": ("Schloss Bad Homburg und Weißer Turm", "50.22810, 8.61080", "Schloss", "genau"),
    "anschlag-auf-alfred-herrhausen": ("Herrhausen-Gedenkstelen am Seedammweg", None, "Seedammweg", "Straße"),
}
# Wird vor dem Lauf aus coords_final ergänzt (Tennis, Golf, Herrhausen)
EXTRA = {}

# Bestehende Einträge: ID -> Änderungen (Spaltenname -> Wert). "ort" verschiebt die Geschichte an einen anderen Pin.
UPDATE = {
    "badhomburg-spielbank-die-brueder-blanc-und-das-roulette": dict(
        Name="Die Mutter von Monte Carlo", Flag=T1,
        Kategorie=f"{GP}, {PERS}, {IKO}", Tags="19. Jahrhundert, Spitzname",
        **{"Teaser Text": "Am 23. Mai 1841 eröffneten die Zwillinge François und Louis Blanc in der kleinen Landgrafschaft Homburg eine Spielbank. "
           "Ihr Trick: Roulette mit nur einer Null, das gab den Spielern bessere Chancen und lockte Gäste aus ganz Europa. "
           "1863 holte Fürst Charles III. François Blanc nach Monaco, wo er das Casino von Monte Carlo groß machte. "
           "Deshalb nennt sich Bad Homburg „Mutter von Monte Carlo“, seit 2013 heißt das Haus François-Blanc-Spielbank.",
           "Quellen": "Wikipedia | " + WP + "Spielbank_Bad_Homburg\nWikipedia (en) | https://en.wikipedia.org/wiki/Fran%C3%A7ois_Blanc\n"
                      "Discover Germany | https://discovergermany.com/the-mother-of-monte-carlo-welcome-to-the-grand-casino-bad-homburg\n"
                      "Uni Heidelberg (heiUP) | https://heiup.uni-heidelberg.de/catalog/view/487/739/86524",
           "Zeitraum": "1841–1872", "Jahr": 1841}),
    "badhomburg-spielbank-dostojewski-am-roulettetisch": dict(
        ort="badhomburg-dostojewski", Flag=SW,
        **{"Teaser Text": "Schon 1863 verspielte Fjodor Dostojewski in Homburg seine Reisekasse. 1866 diktierte er in 26 Tagen den Roman „Der Spieler“, "
           "dessen Kurort Roulettenburg sich Homburg, Wiesbaden und Baden-Baden bis heute streitig machen. "
           "Im Frühjahr 1867, kurz nach der Hochzeit, fuhr er allein von Dresden nach Homburg, verlor wieder, schrieb seiner Frau Anna verzweifelte Briefe "
           "und trug seine Uhr zum Pfandleiher. Seit 2014 erinnert eine Skulptur von Nicolai Karlychanow im Kurhausgarten an ihn.",
           "Quellen": "Stadtlexikon Wiesbaden | https://www.wiesbaden.de/stadtlexikon/stadtlexikon-a-z/dostojewski-fjodor-michailowitsch\n"
                      "Briefe an Anna Grigorjewna (Cambridge) | https://www.cambridge.org/core/journals/advances-in-psychiatric-treatment/article/excerpts-from-the-letters-of-dostoyevsky-to-his-wife-by-fyodor-dostoyevsky/91E46918211DA1DD4E76189F9D725092\n"
                      "Stadt Bad Homburg, Denkmäler im Kurpark | https://www.bad-homburg.de/en/experience/guides/denkmaler-im-kurpark~2gy38k09D5J9?pdf=true\n"
                      "Wikipedia | " + WP + "Der_Spieler_(Dostojewski)",
           "Zeitraum": "1863–1867", "Jahr": 1867, "Adresse": "Kurhausgarten"}),
    "badhomburg-kurpark-der-aelteste-golfplatz-deutschlands": dict(
        ort="badhomburg-golf", Kategorie=f"{GP}, {ERF}",
        **{"Teaser Text": "Englische Kurgäste wollten auch in der Sommerfrische nicht auf ihr Spiel verzichten. So entstand im Kurpark der Platz, "
           "der als ältester Golfplatz Deutschlands gilt; der Royal Homburger Golf Club stammt von 1899. Heute sind es sechs Löcher mitten im Park.",
           "Quellen": "Stadt Bad Homburg | https://www.bad-homburg.de/en/living/sport-and-leisure/sports-facilities/golf-course-in-the-spa-park\n"
                      "LAGIS Hessen | https://www.lagis-hessen.de/en/odk/record/id/1213",
           "Zeitraum": "seit 1899", "Jahr": 1899}),
    "badhomburg-kurpark-der-homburger-hut": dict(
        ort="badhomburg-kurhaus",
        **{"Teaser Text": "Der britische Thronfolger Edward, später König Edward VII., kurte gern in Homburg. 1882 soll er in der Homburger Hutfabrik Möckel "
           "einen steifen Filzhut mit Mittelkniff und gerollter Krempe entdeckt und in London zur Mode gemacht haben. "
           "Der „Homburg“ wurde zum Hut der Staatsmänner, von Anthony Eden bis Konrad Adenauer.",
           "Quellen": "Wikipedia (en) | https://en.wikipedia.org/wiki/Homburg_(hat)\nEBSCO Research Starters | https://www.ebsco.com/research-starters/history/homburg-hat/",
           "Adresse": "Louisenstraße 58"}),
    "badhomburg-kurpark-die-russische-kirche": dict(
        ort="badhomburg-russische-kirche", Flag=SW, Status="Entwurf",
        **{"Teaser Text": "Für die vielen russischen Kurgäste entstand im Kurpark eine orthodoxe Kirche mit goldener Zwiebelkuppel. "
           "Am 16. Oktober 1896 legten Zar Nikolaus II. und Zarin Alexandra, eine Prinzessin aus Hessen-Darmstadt, den Grundstein, geweiht wurde sie am 22. September 1899. "
           "Entworfen hat sie Leonti Benois aus Sankt Petersburg, der Großvater von Peter Ustinov.",
           "Quellen": "Stadt Bad Homburg | https://www.bad-homburg.de/en/tourism/attractions/russian-orthodox-chapel~aX3Y7doQArk\n"
                      "LAGIS Hessen | https://www.lagis-hessen.de/en/odk/record/id/1078\nWikipedia | " + WP + "Russische_Kirche_(Bad_Homburg)",
           "Zeitraum": "1896–1899", "Jahr": 1896, "Adresse": "Kurpark, nahe Kaiser-Friedrich-Promenade"}),
    "anschlag-auf-alfred-herrhausen": dict(
        Name="Herrhausen-Anschlag", Ort="Herrhausen-Gedenkstelen am Seedammweg",
        **{"Teaser Text": "Am 30. November 1989 wurde Deutsche-Bank-Chef Alfred Herrhausen auf dem Seedammweg, wenige hundert Meter von seinem Haus, "
           "durch eine Bombe getötet. Sie war an einem Fahrrad am Straßenrand versteckt und wurde über eine Lichtschranke gezündet, als sein gepanzerter Wagen vorbeifuhr. "
           "Die RAF bekannte sich, die Täter wurden nie gefasst. Gedenkstelen markieren heute die Stelle.",
           "Quellen": "Wikipedia | " + WP + "Alfred_Herrhausen\nbpb | https://www.bpb.de/kurz-knapp/hintergrund-aktuell/196955/vor-30-jahren-ermordung-von-alfred-herrhausen/\n"
                      "hessenschau | https://www.hessenschau.de/archiv/2009/herrhausen-mord---viele-fragen-offen,archiv-2009-herrhausen-mord-viele-fragen-offen-100.html"}),
}

# Neue Einträge
NEW = [
    dict(ort="badhomburg-spielbank", Name="Comeback im Brunnensälchen", Kategorie=GP, Tags="Nachkriegszeit & Kalter Krieg", Flag=LO,
         teaser="1872 machte das Deutsche Reich alle Spielbanken dicht, die Homburger Säle blieben fast 80 Jahre stumm. "
                "Am 7. April 1949 rollte die Kugel wieder, diesmal im kleinen Brunnensälchen im Kurpark, als eine der ersten Spielbanken der jungen Bundesrepublik. "
                "Von hier aus wurde das Haus immer wieder erweitert.",
         quellen=["Wikipedia | " + WP + "Spielbank_Bad_Homburg", "Stadt Bad Homburg | https://www.bad-homburg.de/en/tourism/attractions/bad-homburg-casino~aODYonrL5mP"],
         zeitraum="seit 1949", jahr=1949, status="Prüfen"),
    dict(ort="badhomburg-kurhaus", Name="Der Palast der Spieler", Kategorie=f"{GP}, {VER}", Tags="19. Jahrhundert, Architektur, Nachtleben", Flag=SW,
         teaser="Die Brüder Blanc bezahlten das erste Kurhaus an der Louisenstraße, 1843 war es fertig: Ballsaal, Restaurant und vor allem Spielsäle. "
                "Nach einem Brand 1860 ließ François Blanc es von Jean-Pierre Cluysenaar noch prächtiger wieder aufbauen. Hier spielten Adel, Glücksritter und Dostojewski. "
                "Bomben zerstörten den Bau im März 1945, das heutige Kurhaus ist ein Neubau.",
         quellen=["LAGIS Hessen | https://www.lagis-hessen.de/en/odk/record/id/1067", "Stadt Bad Homburg | https://www.bad-homburg.de/en/tourism/attractions/kurhaus~aWbAqgoE5w2"],
         zeitraum="1843–1945", jahr=1843, status="Prüfen"),
    dict(ort="badhomburg-dichterhaus", Name="Die Spielerin im Roman", Kategorie=PERS, Tags="19. Jahrhundert, Literatur & Bühne", Flag=LO,
         teaser="Eine Tafel an der Ecke Elisabethenstraße/Schwedenpfad erinnert daran, dass hier 1870 Fjodor Dostojewski und 1872 die englische Schriftstellerin George Eliot wohnten. "
                "Eliot sah im Kursaal eine junge Engländerin am Roulettetisch ihr Geld verlieren. Die Szene eröffnet ihren Roman „Daniel Deronda“ (1876).",
         quellen=["Historical Marker Database | https://www.hmdb.org/m.asp?m=247318", "LAGIS Hessen | https://www.lagis-hessen.de/en/klhg/record/id/134561"],
         zeitraum="1870–1872", jahr=1872, status="Prüfen"),
    dict(ort="badhomburg-tennis", Name="Der erste Tennisplatz des Kontinents", Kategorie=f"{ERF}, {GP}", Tags="19. Jahrhundert, Sport", Flag=SW,
         teaser="Im Juni 1876 ließ Sir Robert Anstruther im Kurpark einen Rasenplatz anlegen, den ersten Tennisplatz auf dem europäischen Festland, kaum zwei Jahre nach Erfindung des Spiels in England. "
                "Fotos aus diesem Sommer gelten als die ältesten Tennisbilder der Welt. Der TC Bad Homburg von 1876 ist der älteste Tennisclub des Kontinents.",
         quellen=["Bad Homburg Open | https://badhomburg-open.de/en/tournament/history", "LAGIS Hessen | https://www.lagis-hessen.de/en/odk/record/id/1214",
                  "Stadt Frankfurt, Tennisgeschichte | https://frankfurt.de/-/media/frankfurtde/frankfurt-themen/sport/frankfurter-sportgeschichte/pdf/aus-der-geschichte-des-tennissports-in-frankfurt-(2015).pdf"],
         zeitraum="seit 1876", jahr=1876, status="Entwurf"),
    dict(ort="badhomburg-tennis", Name="Tennis is coming home: die Bad Homburg Open", Kategorie=f"{GP}, {IKO}", Tags="Wende & Gegenwart, Sport", Flag=SW,
         teaser="Seit 2021 spielen die Weltbesten in der Woche vor Wimbledon auf dem Rasen im Kurpark, beim ersten Rasenturnier Hessens. "
                "Angelique Kerber gewann gleich die erste Ausgabe. 2025 schlug Jessica Pegula im Finale Iga Świątek, die zwei Wochen später Wimbledon gewann. 2026 siegte Karolína Muchová.",
         quellen=["Bad Homburg Open | https://badhomburg-open.de/en/tournament/history", "WTA | https://wtatennis.com/tournament/2017/bad-homburg/past-winners",
                  "Wikipedia (en) | https://en.wikipedia.org/wiki/2025_Bad_Homburg_Open_%E2%80%93_Singles"],
         zeitraum="seit 2021", jahr=2021, status="Entwurf"),
    dict(ort="badhomburg-kurpark", Name="Liebigs Lob für den Elisabethenbrunnen", Kategorie=f"{GP}, {ERF}", Tags="19. Jahrhundert, Wissenschaft, Natur", Flag=SW,
         teaser="1834 stieß der Arzt Eduard Christian Trapp wieder auf eine alte Quelle und ließ ihr Wasser von Justus von Liebig untersuchen. "
                "Der Chemiker urteilte, Deutschland habe kaum ein zweites Mineralwasser mit solchem Reichtum an Wirkstoffen. "
                "Der Brunnen, benannt nach Landgräfin Elisabeth, einer englischen Königstochter, machte Homburg zum Kurort, ohne ihn kein Kurpark und keine Spielbank.",
         quellen=["LAGIS Hessen | https://www.lagis-hessen.de/en/odk/record/id/1086", "museum-digital Hessen | https://hessen.museum-digital.de/pdf/object/172597.pdf?lang=de"],
         zeitraum="seit 1834", jahr=1834, status="Prüfen"),
]

COLS = None


def main(src, dst, coords_final):
    global COLS
    ORTE.update({k: (ORTE[k][0], v, ORTE[k][2], g) for k, (v, g) in coords_final.items()})
    for k, v in ORTE.items():
        assert v[1], f"Koordinaten fehlen: {k}"
    wb = openpyxl.load_workbook(src)
    E, O = wb["Frankfurt"], wb["Orte"]
    COLS = {c.value: c.column for c in E[1] if c.value}
    last = lambda ws: max(r for r in range(1, ws.max_row + 1) if ws.cell(r, 1).value)
    # Orte
    orow = {O.cell(r, 1).value: r for r in range(2, last(O) + 1) if O.cell(r, 1).value}
    if "herrhausen" in orow and "anschlag-auf-alfred-herrhausen" not in orow:
        r = orow.pop("herrhausen"); O.cell(r, 1, "anschlag-auf-alfred-herrhausen"); orow["anschlag-auf-alfred-herrhausen"] = r
    for k, (name, co, adr, gen) in ORTE.items():
        if k in orow:
            r = orow[k]
        else:
            r = last(O) + 1; orow[k] = r
            for c in range(1, 8):
                O.cell(r, c)._style = copy.copy(O.cell(r - 1, c)._style)
            O.cell(r, 7, f"=COUNTIF(Frankfurt!$C$2:$C$2993,A{r})")
        for c, v in zip(range(1, 7), [k, name, co, adr, BH, gen]):
            O.cell(r, c, v)
    # Einträge
    erow = {E.cell(r, 1).value: r for r in range(2, last(E) + 1) if E.cell(r, 1).value}
    def setrow(r, ort, vals):
        o = ORTE[ort]
        base = {"Ort-ID": ort, "Koordinaten": o[1], "Adresse": o[2], "Bezirk": BH, "Region": "frankfurt", "Genauigkeit Koordinaten": o[3], "Aktualisiert": TODAY}
        if E.cell(r, COLS["Ort"]).value is None or str(E.cell(r, COLS["Ort"]).value).startswith("="):
            base["Ort"] = f'=IFERROR(INDEX(Orte!$B$2:$B$2000,MATCH(C{r},Orte!$A$2:$A$2000,0)),"")'
        base.update(vals)
        for k, v in base.items():
            E.cell(r, COLS[k], v)
    for sid, ch in UPDATE.items():
        r = erow[sid]; ch = dict(ch)
        ort = ch.pop("ort", None) or E.cell(r, COLS["Ort-ID"]).value
        setrow(r, ort, ch)
    # übrige Bad-Homburg-Einträge an präzisierten Orten nachziehen (Koordinaten, Genauigkeit)
    for sid, r in erow.items():
        ort = E.cell(r, COLS["Ort-ID"]).value
        if ort in ORTE and sid not in UPDATE:
            o = ORTE[ort]
            E.cell(r, COLS["Koordinaten"], o[1]); E.cell(r, COLS["Genauigkeit Koordinaten"], o[3]); E.cell(r, COLS["Aktualisiert"], TODAY)
    style = last(E); r = style + 1
    tags = {wb["Tags"].cell(i, 1).value for i in range(2, wb["Tags"].max_row + 1)}
    cats = {wb["Kategorien"].cell(i, 1).value for i in range(2, wb["Kategorien"].max_row + 1)}
    import re, unicodedata
    def slug(s):
        s = s.lower().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
        s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
        return re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    for d in NEW:
        assert not {t.strip() for t in d["Tags"].split(",")} - tags, d["Tags"]
        assert not {t.strip() for t in d["Kategorie"].split(",")} - cats, d["Kategorie"]
        sid = f"{d['ort']}-{slug(d['Name'])}"[:80]
        assert sid not in erow, sid
        for c in range(1, E.max_column + 1):
            E.cell(r, c)._style = copy.copy(E.cell(style, c)._style)
        setrow(r, d["ort"], {"ID": sid, "Name": d["Name"], "Kategorie": d["Kategorie"], "Tags": d["Tags"], "Flag": d["Flag"],
                             "Teaser Text": d["teaser"], "Quellen": "\n".join(d["quellen"]), "Zeitraum": d["zeitraum"], "Jahr": d["jahr"],
                             "Status": d["status"], "Autor": "claude"})
        erow[sid] = r; r += 1
    for k in UPDATE:
        for t in UPDATE[k].get("Tags", "").split(","):
            assert not t.strip() or t.strip() in tags, t
    # Auswahllisten wiederherstellen (openpyxl verwirft die Excel-Erweiterung beim Laden)
    have = {str(dv.sqref).split(":")[0][:1] for dv in E.data_validations.dataValidation}
    for col, f in [("C", "Orte!$A$2:$A$2000"), ("H", "Flag!$A$2:$A$4"), ("P", "Geo!$A$2:$A$100"), ("S", "Status!$A$2:$A$6")]:
        if col not in have:
            dv = DataValidation(type="list", formula1=f, allow_blank=True); E.add_data_validation(dv); dv.add(f"{col}2:{col}1233")
    wb.save(dst)
    print("Orte", len(ORTE), "geändert", len(UPDATE), "neu", len(NEW), "letzte Zeile", r - 1)


if __name__ == "__main__":
    import json
    main(sys.argv[1], sys.argv[2], {k: tuple(v) for k, v in json.loads(sys.argv[3]).items()})
