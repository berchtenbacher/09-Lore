"""Erzeugt data/hofheim.geojson. Aufruf: python3 tools/seed_hofheim.py data/hofheim.geojson
Koordinaten sind von Hand gesetzt und auf einige Dutzend Meter genau."""
import json, sys

I = []
def add(*a): I.append(a)

add("hofheim-ringwall", "Ringwall auf dem Kapellenberg", "Archäologische Stätte", 3, ["Geschichte"], ["Vorgeschichte"],
    "Kernstadt", "Kapellenberg, Archäologischer Rundweg", "um 3700 v. Chr.", 50.09780, 8.43900,
    "Lange vor Hofheim lebten hier oben Hunderte Menschen hinter Wall und Palisade, vor fast 6.000 Jahren.",
    ["Der bewaldete Kapellenberg über Hofheim trägt eines der ältesten noch sichtbaren Bodendenkmäler im Rhein-Main-Gebiet. In der Jungsteinzeit, zur Zeit der Michelsberger Kultur, war der Bergrücken eine befestigte Siedlung. Der äußere Wall ist gut drei Kilometer lang und umschließt rund 45 Hektar.",
     "Die Innenfläche von etwa 24 Hektar war um 3750 bis 3650 v. Chr. bewohnt, geschätzt von mehreren hundert Menschen. Schon zu Beginn dieser Zeit entstand ein gewaltiger Grabhügel, heute noch 90 Meter breit und 6 Meter hoch. In seiner Grabkammer lagen zwei Steinbeile, eines davon aus Jadeit.",
     "Auf der höchsten Stelle liegen zwei jüngere Gräber der Schnurkeramik (um 2800 bis 2200 v. Chr.). Wer genau hinsieht, erkennt die Wälle beim Spaziergang noch im Gelände."])

add("hofheim-bergkapelle", "Bergkapelle und das Pestgelübde", "Kapelle", 3, ["Religion", "Geschichte"], ["Frühe Neuzeit"],
    "Kernstadt", "Kapellenberg", "1666", 50.09620, 8.44120,
    "Als 1666 die Pest wütete, zog die ganze Gemeinde auf den Berg und legte ein Gelübde ab. Danach soll niemand mehr an der Pest gestorben sein.",
    ["Im Pestjahr 1666 führte Pfarrer Johannes Gleidener die Hofheimer am Himmelfahrtstag in einer Prozession auf den Rabberg, wie der Berg damals hieß. Sie gelobten, dort eine Kapelle zu bauen und jedes Jahr dorthin zu pilgern, wenn die Stadt verschont bliebe.",
     "In den Kirchenbüchern ist nach diesem Tag kein weiterer Pesttoter verzeichnet. 1667 wurde die Kapelle geweiht. Weil immer mehr Pilger kamen, ersetzte man den Fachwerkbau später durch die heutige größere Steinkapelle, und aus dem Rabberg wurde der Kapellenberg.",
     "Die Wallfahrt gibt es bis heute. Das Königsteiner Kreuz von 1792 am Weg markiert die Stelle, an der sich früher die Pilger aus Königstein den Hofheimern anschlossen."])

add("hofheim-hexenturm", "Hexenturm an der Kellerei", "Turm, Gedenkort", 3, ["Geschichte", "Erinnerung"], ["Mittelalter", "Frühe Neuzeit"],
    "Kernstadt", "Kellereiplatz", "14. Jahrhundert", 50.08800, 8.45000,
    "In diesem Turm der alten Stadtmauer saßen Frauen gefangen, die als Hexen angeklagt waren.",
    ["Der runde Turm am östlichen Eck des Kellereigebäudes ist einer der wenigen erhaltenen Türme der Stadtmauer aus dem 14. Jahrhundert. Die barocke Haube bekam er erst später.",
     "Seinen Namen verdankt er einem dunklen Kapitel: Während der Hexenverfolgung in der Frühen Neuzeit wurden hier Frauen eingesperrt, denen Hexerei vorgeworfen wurde. Gedenktafeln am Turm erinnern an die Verfolgten.",
     "In den 2010er Jahren wurde in Hofheim über die Rehabilitierung der Opfer diskutiert. Der Pfarrer und Forscher Hartmut Hegeler hat dazu im Jahrbuch des Main-Taunus-Kreises 2013 geschrieben."])

add("hofheim-kellerei", "Kellerei und Alte Burg", "Amtsgebäude", 1, ["Geschichte", "Architektur"], ["Mittelalter", "Frühe Neuzeit"],
    "Kernstadt", "Kellereiplatz", "1425 / 1719", 50.08820, 8.44960,
    "Hier saß der Mainzer Keller, der für den Kurfürsten die Abgaben eintrieb.",
    ["Am Kellereiplatz stand die Alte Burg der Stadt, von ihr sind Mauer- und Brückenreste erhalten. Daneben entstand die Kellerei, der Verwaltungssitz für den Amtmann, der Steuern und Naturalabgaben einzog. Daher der Name: Im Keller lagerte, was abgeliefert wurde.",
     "Teile des Kellereigebäudes stammen von 1425/26. Der Mainzer Kurfürst Lothar Franz von Schönborn ließ es 1717 bis 1719 ausbauen."])

add("hofheim-stadtrechte", "Stadtmauer in der Bärengasse", "Stadtbefestigung", 2, ["Geschichte"], ["Mittelalter"],
    "Kernstadt", "Bärengasse / Mauergasse", "1352", 50.08890, 8.44760,
    "Kaiser Karl IV. machte das Dorf 1352 zur Stadt, und die Bürger durften sich eine Mauer bauen.",
    ["Am 21. März 1352 verlieh Kaiser Karl IV. Hofheim die Stadtrechte. Damit durfte es sich mit Mauern, Toren und Brücken befestigen, ein eigenes Gericht halten und einen Wochenmarkt abhalten.",
     "Die Mauer aus der Mitte des 14. Jahrhunderts ist in der Bärengasse und der Mauergasse noch zu sehen. Die Gassen folgen bis heute ihrem Verlauf um die Altstadt."])

add("hofheim-rathaus", "Altes Rathaus", "Rathaus", 1, ["Architektur", "Geschichte"], ["Frühe Neuzeit"],
    "Kernstadt", "Hauptstraße", "1529", 50.08860, 8.44830,
    "Erst Kaufhaus, dann Rathaus: Fachwerk auf Bruchstein aus dem Jahr 1529.",
    ["Das Haus wurde 1529 unter den Grafen von Eppstein-Königstein gebaut, ursprünglich als Kaufhaus. Später zog die Stadtverwaltung ein.",
     "Das Erdgeschoss ist aus Bruchstein gemauert, darüber steht Fachwerk. Der verzierte Westgiebel kam erst 1901 dazu."])

add("hofheim-kirche", "St. Peter und Paul", "Kirche", 1, ["Religion", "Architektur"], ["Mittelalter"],
    "Kernstadt", "Kirchplatz", "ab 1481", 50.08930, 8.44950,
    "Die Pfarrkirche mit dem Stadtpatron Petrus, der auch das Hofheimer Wappen ziert.",
    ["Mit dem Bau der heutigen Kirche wurde 1481 begonnen, Seitenchor und Teile des Turms stammen noch aus dieser Zeit. Die geschwungene Turmhaube kam 1926 dazu.",
     "Der heilige Petrus ist der Stadtpatron. Er steht auch im Stadtwappen, das auf die Gerichtssiegel zurückgeht, die seit 1368 belegt sind."])

add("hofheim-roemerkastell", "Römerkastell unter dem Landratsamt", "Archäologische Stätte", 2, ["Geschichte"], ["Antike"],
    "Kernstadt", "Am Kreishaus, Hochfeld", "1. Jahrhundert", 50.08480, 8.45700,
    "Wo heute der Main-Taunus-Kreis verwaltet wird, standen vor fast 2.000 Jahren rund 500 römische Soldaten.",
    ["Spätestens um 40 n. Chr. legten die Römer auf dem Hochfeld ein erstes Erdlager an. Es wurde später durch ein Kastell mit Holztürmen und Rasenmauer und schließlich durch ein Steinkastell ersetzt. Von hier aus führten die Römer Feldzüge gegen die Chatten.",
     "Südlich des Lagers lag ein Dorf mit Handwerkern und Händlern, die die Soldaten versorgten. Um 110 n. Chr. wurde das Kastell aufgegeben.",
     "Auf dem Gelände steht seit 1987 das Landratsamt. Bei Grabungen 2021 für einen Erweiterungsbau stieß man wieder auf einen Graben des alten Erdlagers."])

add("hofheim-blaues-haus", "Das Blaue Haus", "Wohnhaus", 2, ["Persönlichkeit", "Kultur", "Geschichte"], ["20. Jahrhundert"],
    "Kernstadt", "Kapellenstraße", "ab 1921", 50.09250, 8.44400,
    "In diesem Haus am Kapellenberg zeigte Hanna Bekker vom Rath Kunst, die die Nazis verboten hatten.",
    ["Die Sammlerin und Kunsthändlerin Hanna Bekker vom Rath erwarb das Landhaus 1921. Die Malerin Ida Kerkovius gab ihm den Namen „Blaues Haus“. Es wurde ein Treffpunkt der Moderne, Alexej von Jawlensky war eng mit Bekker vom Rath befreundet.",
     "1933 verboten die Nationalsozialisten eine geplante Ausstellung von Karl Schmidt-Rottluff in Frankfurt. Bekker vom Rath zeigte die Bilder kurzerhand in ihrem Haus in Hofheim. Auch später vermittelte sie heimlich Werke verfemter Künstler.",
     "Nach dem Krieg holte sie den Maler Ernst Wilhelm Nay nach Hofheim, dessen Berliner Atelier zerbombt war. Er arbeitete hier bis 1951 im früheren Atelier der Malerin Ottilie Roederstein, die seit 1909 mit der Chirurgin Elisabeth Winterhalter in Hofheim gelebt hatte. Das Blaue Haus ist heute in Privatbesitz."])

add("hofheim-meisterturm", "Meisterturm", "Aussichtsturm", 1, ["Natur", "Geschichte"], ["19. Jahrhundert", "20. Jahrhundert"],
    "Kernstadt", "Kapellenberg", "1895 / 1929", 50.09870, 8.43620,
    "Benannt nach einem Landrat, der Vorgänger aus Holz fiel einem Blitz zum Opfer.",
    ["Auf dem höchsten Punkt des Kapellenbergs stand ab 1895 ein hölzerner Aussichtsturm. Er soll am Ende durch einen Blitzschlag zerstört worden sein.",
     "1929 ersetzte ihn ein Turm aus Stahl. Er wurde nach Wilhelm von Meister benannt, dem ersten Landrat des Kreises Höchst. Daneben lädt ein Ausflugslokal zur Rast ein."])

add("hofheim-cohausentempel", "Cohausentempel", "Aussichtspunkt", 1, ["Persönlichkeit", "Natur"], ["20. Jahrhundert"],
    "Kernstadt", "Westhang des Kapellenbergs", "Jugendstil", 50.09520, 8.43350,
    "Ein kleiner Tempel für den Mann, der als Erster den Ringwall erforschte.",
    ["Der Aussichtspunkt in den Formen des späten Jugendstils erinnert an Karl August von Cohausen. Der nassauische Konservator untersuchte im 19. Jahrhundert zahlreiche Altertümer im Taunus, darunter den Limes und den Ringwall auf dem Kapellenberg.",
     "Vom Tempel blickt man über das Main-Taunus-Vorland bis zur Frankfurter Skyline."])

add("hofheim-wasserschloss", "Wasserschloss", "Burg", 1, ["Geschichte", "Architektur"], ["Mittelalter"],
    "Kernstadt", "östlich der Altstadt", "um 1352–1356", 50.08740, 8.45180,
    "Ein Adelssitz im Wassergraben, vor den Toren der mittelalterlichen Stadt.",
    ["Schon im 13. Jahrhundert ist ein Geschlecht „von Hofheim“ belegt, das eine Wasserburg als Lehen hielt. Das heutige Wasserschloss entstand vermutlich um 1352 bis 1356, also in den Jahren, als Hofheim Stadt wurde.",
     "1356 wird das „Slois zu Hofheim“ erwähnt, besetzt mit Burgmannen. Es lag außerhalb der Stadtmauer und ist heute in Privatbesitz."])

add("hofheim-wallau-kelten", "Keltengräber von Wallau", "Fundort", 1, ["Geschichte"], ["Vorgeschichte"],
    "Wallau", "Westlicher Ortsrand", "Fund 1959", 50.05650, 8.36600,
    "Beim Bauen stieß man 1959 auf reiche Gräber der Kelten.",
    ["1959 wurden am westlichen Ortsrand von Wallau reich ausgestattete keltische Gräber entdeckt. Sie zeigen, dass die Gegend lange vor den Römern besiedelt war.",
     "Wallau selbst wird 950 als „Wanaloha“ in einer Schenkung Ottos I. erwähnt. Von 1643 bis 1817 war es Hauptort des evangelischen „Ländchens“. Heute kennt man Wallau vor allem wegen des Wiesbadener Kreuzes, das auf seiner Gemarkung liegt."])

add("hofheim-lorsbach-leder", "Lederfabrik Lorsbach", "Industriedenkmal", 1, ["Geschichte", "Architektur"], ["19. Jahrhundert", "20. Jahrhundert"],
    "Lorsbach", "Schwarzbachtal", "ab 1881", 50.10900, 8.41800,
    "Im engen Schwarzbachtal trieb das Wasser erst Mühlen und dann eine Lederindustrie an.",
    ["Lorsbach liegt im schmalen Tal des Schwarzbachs, umgeben von bewaldeten Taunushängen. Über Jahrhunderte nutzten Mühlen die Wasserkraft.",
     "1881 entstand in der Trutzmühle die erste Lederfabrik, das Dorf wurde zum Gerberort. Nach dem Zweiten Weltkrieg ging die Lederindustrie zurück. Die Gebäude der früheren Lederfabrik stehen heute unter Denkmalschutz."])

feats = []
for (id_, title, kind, imp, themes, epochs, st, addr, year, lat, lon, teaser, story) in I:
    feats.append({
        "type": "Feature", "id": id_,
        "geometry": {"type": "Point", "coordinates": [lon, lat]},
        "properties": {
            "id": id_, "title": title, "kind": kind, "importance": imp,
            "themes": themes, "epochs": epochs,
            "place": {"stadtteil": st, "stadt": "Hofheim am Taunus", "kreis": "Main-Taunus-Kreis", "bundesland": "Hessen"},
            "address": addr, "period": year, "teaser": teaser, "story": story,
            "sources": [{"label": "Wikipedia", "url": "https://de.wikipedia.org/w/index.php?search=" + title.replace(" ", "+") + "+Hofheim"}],
            "status": "published", "author": "redaktion", "updated": "2026-10-20",
        }})

out = {"type": "FeatureCollection",
       "meta": {"schemaVersion": 1, "region": "Hofheim am Taunus", "importanceScale": {"3": "Wahrzeichen", "2": "Bedeutend", "1": "Lokal"}},
       "features": feats}
json.dump(out, open(sys.argv[1], "w"), ensure_ascii=False, indent=2)
print(len(feats))
