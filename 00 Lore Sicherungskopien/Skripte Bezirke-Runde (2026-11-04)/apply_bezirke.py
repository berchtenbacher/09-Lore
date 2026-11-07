# Bezirke-Runde (04.11.2026): Nordend, Westend, Gallus, Bockenheim, Bornheim, Bahnhofsviertel.
# Aufruf: python3 apply_bezirke.py ein.xlsx aus.xlsx '{}'
# Koordinaten aus Wikipedia-, Waymarking-, Jewish-Places- und Reiseportal-Angaben (per Websuche), sonst von Hand nach Adresse
# und dann als „Straße“ oder „ungefähr“ markiert. Jeder Punkt wurde gegen die Stadtteilflächen in data/frankfurt-stadtteile.geojson geprüft.
import sys, copy, re, json, unicodedata, openpyxl
from openpyxl.worksheet.datavalidation import DataValidation

TODAY = "2026-11-04"
GP, PERS, KIEZ, ERF, WEG, SAGE = ("Geschichte & Politik", "Persönlichkeiten", "Kiez-Geschichten", "Erfindungen",
                                  "Verschwundenes", "Sagen & Legenden")
T1, SW, LO = "Touri 1x1", "Sehenswürdigkeit", "Lokal"
GEO_NEW = [("Nordend-Ost", "Frankfurt am Main", "frankfurt", "Kreisfreie Stadt Frankfurt am Main", "Hessen"),
           ("Bornheim", "Frankfurt am Main", "frankfurt", "Kreisfreie Stadt Frankfurt am Main", "Hessen")]

# id -> (Name, Koordinaten, Adresse, Bezirk, Genauigkeit)
ORTE = {
    # Nordend
    "nordend-bethmannpark": ("Bethmannpark", "50.11899, 8.69080", "Friedberger Landstraße / Berger Straße", "Nordend-Ost", "genau"),
    "nordend-guenthersburgpark": ("Günthersburgpark und Orangerie", "50.13060, 8.70320", "Günthersburgallee", "Nordend-Ost", "ungefähr"),
    "nordend-nationalbibliothek": ("Deutsche Nationalbibliothek", "50.13121, 8.68329", "Adickesallee 1", "Nordend-West", "genau"),
    # Westend
    "westend-synagoge": ("Westend-Synagoge", "50.12129, 8.66395", "Freiherr-vom-Stein-Straße 30", "Westend-Süd", "genau"),
    "westend-wollheim-memorial": ("Wollheim Memorial", "50.12480, 8.66600", "Norbert-Wollheim-Platz 1", "Westend-Nord", "ungefähr"),
    "westend-grueneburgpark": ("Grüneburgpark", "50.12720, 8.66110", "Grüneburgweg / August-Siebert-Straße", "Westend-Nord", "ungefähr"),
    "westend-clara-schumann": ("Haus von Clara Schumann", "50.11950, 8.66600", "Myliusstraße 32", "Westend-Süd", "Straße"),
    # Gallus
    "gallus-galluswarte": ("Galluswarte", "50.10520, 8.64430", "Mainzer Landstraße, Platz an der Galluswarte", "Gallus", "ungefähr"),
    "gallus-adlerwerke": ("Adlerwerke und Geschichtsort Adlerwerke", "50.10170, 8.64080", "Kleyerstraße 17", "Gallus", "Straße"),
    "gallus-hellerhof": ("Hellerhofsiedlung", "50.10380, 8.63300", "Idsteiner Straße / Frankenallee", "Gallus", "ungefähr"),
    # Bockenheim
    "bockenheimer-depot": ("Bockenheimer Depot", "50.12083, 8.65167", "Carlo-Schmid-Platz 1", "Bockenheim", "genau"),
    "bockenheim-synagoge": ("Ehemalige Synagoge Bockenheim", "50.12377, 8.63640", "Schloßstraße 3–5", "Bockenheim", "genau"),
    "bockenheim-kurfuerstenplatz": ("Kurfürstenplatz mit Obeliskbrunnen", "50.12220, 8.63900", "Kurfürstenplatz", "Bockenheim", "ungefähr"),
    # Bornheim
    "bornheim-johanniskirche": ("Johanniskirche Bornheim", "50.13083, 8.71172", "Turmstraße 12", "Bornheim", "genau"),
    "bornheim-uhrtuermchen": ("Uhrtürmchen an der Berger Straße", "50.12650, 8.71000", "Berger Straße / Arnsburger Straße", "Bornheim", "ungefähr"),
    "bornheim-friedberger-warte": ("Friedberger Warte", "50.13932, 8.69844", "Friedberger Landstraße / Homburger Landstraße", "Bornheim", "ungefähr"),
    "bornheim-bornheimer-hang": ("Siedlung Bornheimer Hang", "50.12850, 8.72100", "Ernst-May-Platz", "Bornheim", "ungefähr"),
    # Bahnhofsviertel
    "bahnhofsviertel-kaiserstrasse": ("Kaiserstraße", "50.10870, 8.67200", "Kaiserstraße / Weserstraße", "Bahnhofsviertel", "Straße"),
    "bahnhofsviertel-niddastrasse": ("Niddastraße (Drogenhilfe)", "50.10930, 8.66750", "Niddastraße / Moselstraße", "Bahnhofsviertel", "Straße"),
}

NEW = [
    # ---------- Nordend ----------
    dict(ort="nordend-bethmannpark", Name="Napoleon im Gartenhaus", Kategorie=f"{GP}, {PERS}", Tags="19. Jahrhundert", Flag=LO,
         teaser="Nach der verlorenen Völkerschlacht bei Leipzig zog Napoleon im Herbst 1813 mit seiner Armee nach Westen und quartierte sich "
                "im Gartenhaus des Bankiers Simon Moritz von Bethmann vor dem Friedberger Tor ein. Am 31. Oktober 1813 kam es zu einem Artilleriegefecht um die Mainbrücke. "
                "Bethmann soll den Kaiser überredet haben, den Beschuss von Sachsenhausen einzustellen. Der Garten der Familie ist heute der Bethmannpark.",
         quellen=["Simon Moritz von Bethmann (dewiki) | https://dewiki.de/Lexikon/Simon_Moritz_von_Bethmann",
                  "Journal Frankfurt | https://www.journal-frankfurt.de/journal_news/Stadtleben-2/Frankfurter-Parks-Gaerten-und-Anlagen-Gruener-wirds-nicht-der-Bethmannpark-42577.html"],
         zeitraum="1813", jahr=1813, status="Prüfen"),
    dict(ort="nordend-bethmannpark", Name="Ein chinesischer Garten im Nordend", Kategorie=KIEZ, Tags="Wende & Gegenwart, Natur, Architektur", Flag=LO,
         teaser="Hinter einer Mauer im Bethmannpark liegt seit 1989 ein chinesischer Garten mit Pavillon, Wasserlauf und Felsen. "
                "Der Park selbst ist der alte Garten der Bankiersfamilie Bethmann und steht seit 1976 unter Denkmalschutz.",
         quellen=["Journal Frankfurt | https://www.journal-frankfurt.de/journal_news/Stadtleben-2/Frankfurter-Parks-Gaerten-und-Anlagen-Gruener-wirds-nicht-der-Bethmannpark-42577.html",
                  "Frankfurt Rhein-Main | https://www.frankfurt-rhein-main.de/en/poi/detail/bethmannpark-d6f255264a"],
         zeitraum="seit 1989", jahr=1989, status="Prüfen"),
    dict(ort="nordend-guenthersburgpark", Name="Der Park der Rothschilds", Kategorie=f"{GP}, {WEG}", Tags="19. Jahrhundert, Natur, Jüdisches Leben", Flag=LO,
         teaser="Der Park geht auf den Gutshof Günthersburg zurück, der einst von Wassergräben umgeben war. 1837 kaufte ihn Carl von Rothschild, "
                "sein Sohn Mayer Carl ließ das alte Schlösschen 1855 abreißen und baute eine Sommervilla. Er starb 1886 ohne Söhne und vermachte das Anwesen der Stadt, "
                "seit 1892 ist der Park öffentlich. Von der Rothschild-Zeit blieb nur die Orangerie.",
         quellen=["Rothschild Archive | https://family.rothschildarchive.org/estates/5-villa-gunthersburg",
                  "Frankfurt-Tipp | https://www.frankfurt-tipp.de/en/index/leisure/s/freizeit/the-guenthersburgpark-not-only-in-summer-one-of-frankfurts-most-popular-parks.html",
                  "Societäts-Verlag, Stadtteilserie Bornheim (Leseprobe) | https://societaets-verlag.de/wp-content/uploads/sites/2/2026/02/Leseprobe_Stadtteilserie_Bornheim.pdf"],
         zeitraum="1837–1892", jahr=1837, status="Prüfen"),
    dict(ort="nordend-nationalbibliothek", Name="Das Gedächtnis der Bücher", Kategorie=GP, Tags="Nachkriegszeit & Kalter Krieg, Literatur & Bühne, Architektur", Flag=LO,
         teaser="1946/47 entstand in Frankfurt die Deutsche Bibliothek, das westdeutsche Gegenstück zur Deutschen Bücherei in Leipzig. "
                "Seit der Wiedervereinigung gehören beide zusammen, heute als Deutsche Nationalbibliothek, die jede in Deutschland erscheinende Publikation sammelt. "
                "1997 bezog sie den Neubau an der Adickesallee, der rund 250 Millionen Mark kostete.",
         quellen=["Wikipedia (en) | https://en.wikipedia.org/wiki/German_National_Library",
                  "Deutsche Nationalbibliothek, Gebäude | https://www.dnb.de/EN/Ueber-uns/Gebaeude/gebaeude.html"],
         zeitraum="seit 1946", jahr=1947, status="Entwurf"),
    # ---------- Westend ----------
    dict(ort="westend-synagoge", Name="Die Synagoge, die stehen blieb", Kategorie=GP, Tags="Kaiserreich, NS-Zeit, Jüdisches Leben, Religion, Architektur", Flag=SW,
         teaser="Franz Roeckle baute die Westend-Synagoge 1908 bis 1910, sie ist die größte Synagoge Frankfurts. Im Novemberpogrom 1938 wurde sie innen schwer beschädigt, "
                "blieb aber als einzige der großen Frankfurter Synagogen stehen, und überstand 1944 auch Brandbomben. "
                "Heute ist sie das Hauptgotteshaus der Jüdischen Gemeinde und Ort des Gedenkens am 9. November.",
         quellen=["Jüdische Allgemeine | https://www.juedische-allgemeine.de/unsere-woche/neuanfang-nach-der-schoa-erster-gottesdienst-in-frankfurts-westendsynagoge/",
                  "Jewish Places | https://cms.jewish-places.de/en/node/12374",
                  "Jüdische Gemeinde Frankfurt, 100 Jahre Westend-Synagoge | https://jg-ffm.de/uploads/mediaLibrary/100_Jahre_Westend_Synagoge.pdf"],
         zeitraum="seit 1910", jahr=1910, status="Entwurf"),
    dict(ort="westend-wollheim-memorial", Name="Der Mann, der IG Farben verklagte", Kategorie=f"{GP}, {PERS}", Tags="NS-Zeit, Nachkriegszeit & Kalter Krieg, Erinnerung, Jüdisches Leben", Flag=LO,
         teaser="Norbert Wollheim musste im IG-Farben-Lager Buna/Monowitz bei Auschwitz Zwangsarbeit leisten. Im November 1951 verklagte er als Erster den Konzern, "
                "1957 zahlte IG Farben in einem Vergleich 30 Millionen Mark an ehemalige Häftlinge, ohne Schuld anzuerkennen. "
                "Seit 2008 erinnert vor dem früheren Konzernsitz ein Pavillon von Heiner Blum mit Wollheims Häftlingsnummer an ihn, der Platz trägt seit 2014 seinen Namen.",
         quellen=["Deutsche Biographie | https://www.deutsche-biographie.de/sfz142966.html",
                  "Fritz Bauer Institut | https://www.fritz-bauer-institut.de/en/norbert-wollheim-memorial",
                  "Wikipedia (en) | https://en.wikipedia.org/wiki/Wollheim_Memorial"],
         zeitraum="1951–1957", jahr=1951, status="Entwurf"),
    dict(ort="westend-grueneburgpark", Name="Das verschwundene Schloss der Grüneburg", Kategorie=f"{WEG}, {GP}", Tags="NS-Zeit, Natur, Jüdisches Leben", Flag=LO,
         teaser="Der Name geht auf eine „grüne Burg“ aus dem 14. Jahrhundert zurück. Im 18. Jahrhundert machte Peter Heinrich von Bethmann-Metzler das Gut zum Landsitz, "
                "im 19. Jahrhundert kauften es die Rothschilds. In der NS-Zeit verlor die Familie das Anwesen an die Stadt, das Schloss wurde im Krieg zerstört. "
                "Ein schwarzer Obelisk markiert heute den Platz. Seit 2006 liegt im Park ein Koreanischer Garten, ein Geschenk des Buchmessen-Gastlands Südkorea.",
         quellen=["Wikipedia (en) | https://en.wikipedia.org/wiki/Gr%C3%BCneburgpark",
                  "Goethe-Universität, The Grüneburg | https://www.uni-frankfurt.de/68266101/The_Gr%C3%BCneburg",
                  "Stadt Frankfurt, Koreanischer Garten | https://frankfurt.de/english/discover-and-experience/sightseeing/gardens/korean-garden"],
         zeitraum="14. Jh. bis 1945", jahr=1935, status="Prüfen"),
    dict(ort="westend-clara-schumann", Name="Clara Schumanns Salon", Kategorie=PERS, Tags="Kaiserreich, Musik", Flag=LO,
         teaser="1878 zog die Pianistin Clara Schumann mit ihren Töchtern in die Myliusstraße 32 und wurde die erste Klavierlehrerin an Dr. Hoch's Konservatorium. "
                "In ihrem Haus gab sie private Konzerte, vor allem wenn Johannes Brahms, Joseph Joachim oder Julius Stockhausen zu Besuch waren. "
                "Sie starb 1896 in Frankfurt und wurde neben Robert Schumann in Bonn begraben.",
         quellen=["Schumann-Portal | https://www.schumann-portal.de/frankfurtmain-1878-1896.html",
                  "Kultur Frankfurt | https://kultur-frankfurt.de/portal/de/Music/Schumann2cClara1819-1896/2474/0/77787/mod2065-seite2-details1/1442.aspx"],
         zeitraum="1878–1896", jahr=1878, status="Prüfen"),
    # ---------- Gallus ----------
    dict(ort="gallus-galluswarte", Name="Gallus kommt vom Galgen", Kategorie=f"{KIEZ}, {SAGE}", Tags="Mittelalter & früher, Spitzname", Flag=SW,
         teaser="Anders als in vielen Orten steht hinter dem Namen Gallus kein Heiliger, sondern der Galgen: Vor dem Galgentor lag das Galgenfeld, Frankfurts Richtstätte. "
                "Der Wartturm von 1414 an der Landwehr hieß deshalb Galgenwarte und wurde erst 1903 in Galluswarte umbenannt. "
                "Ein Chronist vermutete, man wollte den Klang mildern. Seit 2007 heißt der Stadtteil offiziell nur noch Gallus.",
         quellen=["Wikipedia (en) | https://en.wikipedia.org/wiki/Gallus_(Frankfurt_am_Main)", "Komoot | https://www.komoot.com/highlight/5396748",
                  "wg-gesucht, Stadtteil Gallus | https://www.wg-gesucht.de/artikel/frankfurt-gallus-kamerun-liegt-noerdlich-des-mains-in-frankfurt"],
         zeitraum="1414 / 1903", jahr=1414, status="Prüfen"),
    dict(ort="gallus-adlerwerke", Name="Das KZ in der Fabrik", Kategorie=GP, Tags="NS-Zeit, Erinnerung", Flag=SW,
         teaser="Schon Ende 1943 arbeiteten über 2.100 ausländische Zwangsarbeiter in den Adlerwerken. Im August 1944 kamen 200 Häftlinge aus Buchenwald "
                "und mussten auf dem Werksgelände das KZ „Katzbach“ errichten, ein Außenlager von Natzweiler. 527 Häftlinge starben dort oder wurden ermordet, "
                "das Lager endete mit einem Todesmarsch nach Hünfeld. Nach rund 30 Jahren Einsatz von Bürgern gibt es im Haus Kleyerstraße 17 den Geschichtsort Adlerwerke.",
         quellen=["Fritz Bauer Institut | https://www.fritz-bauer-institut.de/en/research-projects/the-history-of-katzbach-concentration-camp-in-frankfurt-am-main/",
                  "Jüdische Allgemeine | https://www.juedische-allgemeine.de/unsere-woche/ns-geschichtsort-adlerwerke-eroeffnet",
                  "hessenschau | https://www.hessenschau.de/gesellschaft/gedenkstele-fuer-kz-opfer-in-frankfurt-eingeweiht-v1,kurz-gedenkstele-katzbach-100.html"],
         zeitraum="1944–1945", jahr=1944, status="Entwurf"),
    dict(ort="gallus-adlerwerke", Name="Fahrräder, Schreibmaschinen, Autos", Kategorie=f"{ERF}, {KIEZ}", Tags="Kaiserreich, Verkehr", Flag=LO,
         teaser="Heinrich Kleyer begann mit Fahrrädern und baute ab 1889 im Gallus sein Werk. Unter dem Namen Adler liefen hier später Schreibmaschinen, "
                "Autos und Motorräder vom Band, die Fabrik machte das Gallus zum Arbeiterviertel. Das Hauptgebäude an der Kleyerstraße steht noch.",
         quellen=["Wikipedia (en) | https://en.wikipedia.org/wiki/Adler_(cars_and_motorcycle)",
                  "Kultur Frankfurt, Adlerwerke | https://kultur-frankfurt.de/portal/en/Design/Adlerwerke/600/0/28504/mod1085-details1/1428.aspx"],
         zeitraum="ab 1889", jahr=1889, status="Prüfen"),
    dict(ort="gallus-hellerhof", Name="Mart Stams lange Zeilen", Kategorie=f"{KIEZ}, {GP}", Tags="Weimarer Republik, Architektur", Flag=LO,
         teaser="Für das Neue Frankfurt entwarf der Niederländer Mart Stam die Hellerhofsiedlung, gebaut in drei Abschnitten von 1929 bis 1932. "
                "Im ersten setzte er fünf je 165 Meter lange Zeilen in Nord-Süd-Richtung an die Idsteiner Straße. "
                "1975 stritt die Stadt über Abriss und Sanierung, die Blöcke nördlich der Idsteiner Straße sind Nachbauten von 1951.",
         quellen=["Kunstchronik (Uni Heidelberg) | https://journals.ub.uni-heidelberg.de/index.php/kchronik/article/view/95330/90212",
                  "Architectuul | https://architectuul.com/architecture/hellerhof-estate"],
         zeitraum="1929–1932", jahr=1929, status="Prüfen"),
    # ---------- Bockenheim ----------
    dict(ort="bockenheimer-depot", Name="Die Oper im Straßenbahnhof", Kategorie=f"{KIEZ}, {GP}", Tags="Kaiserreich, Verkehr, Literatur & Bühne, Architektur", Flag=LO,
         teaser="Um 1900 entstand am Carlo-Schmid-Platz das Depot und die Hauptwerkstatt der Frankfurter Straßenbahn, drei Hallen aus gelbem Backstein. "
                "Als im November 1987 ein Brand die Oper beschädigte, brauchten die Bühnen einen Ersatz. 1988 baute Klaus Peter Heinrici die Hallen zum Theater um, "
                "heute laufen dort vor allem Barockopern und zeitgenössische Stücke.",
         quellen=["Wikipedia (en) | https://en.wikipedia.org/wiki/Bockenheimer_Depot", "Structurae | https://structurae.net/de/bauwerke/bockenheimer-depot"],
         zeitraum="seit 1900", jahr=1900, status="Entwurf"),
    dict(ort="bockenheim-synagoge", Name="Die Synagoge in der Schloßstraße", Kategorie=f"{GP}, {WEG}", Tags="NS-Zeit, Jüdisches Leben, Erinnerung, Religion", Flag=LO,
         teaser="1874 weihte die jüdische Gemeinde der damals selbstständigen Stadt Bockenheim ihre Synagoge ein, mit 248 Plätzen und einer Empore für die Frauen. "
                "Im September 1938 hielt Jakob Horovitz hier den letzten Gottesdienst, in der Pogromnacht wurde sie geschändet und in Brand gesteckt. "
                "Seit November 1988 erinnert eine Gedenktafel von Willi Schmidt an das Haus.",
         quellen=["Jewish Places | https://cms.jewish-places.de/en/78237atk",
                  "Waymarking | https://www.waymarking.com/waymarks/wm1747G_Synagoge_Bockenheim_Frankfurt_am_Main_Germany"],
         zeitraum="1874–1938", jahr=1874, status="Entwurf"),
    dict(ort="bockenheim-kurfuerstenplatz", Name="Die Stadt vor der Stadt", Kategorie=f"{GP}, {KIEZ}", Tags="19. Jahrhundert, Kaiserreich", Flag=LO,
         teaser="Bockenheim gehörte nicht zu Frankfurt, sondern zu Hessen-Kassel. 1819 machte Kurfürst Wilhelm I. das Dorf zur Stadt, daran erinnert der Kurfürstenplatz, "
                "lange der Mittelpunkt des Ortes, mit einem zehn Meter hohen Obeliskbrunnen und dem Rathaus von 1869 bis 1871. "
                "Zum 1. April 1895 vereinbarten Frankfurts Oberbürgermeister Franz Adickes und Bürgermeister Adalbert Hengsberger die Eingemeindung.",
         quellen=["ich-geh-wandern.de | https://www.ich-geh-wandern.de/frankfurt-bockenheim",
                  "Archivportal-D, Eingemeindung Bockenheims | https://www.archivportal-d.de/item/RVELHTAC4NJD3XRB2DHCPRPU3K77T525?lang=en",
                  "Geocaching (Obeliskbrunnen) | https://www.geocaching.com/geocache/GC7ENAX"],
         zeitraum="1819–1895", jahr=1819, status="Prüfen"),
    # ---------- Bornheim ----------
    dict(ort="bornheim-johanniskirche", Name="Der erste Blitzableiter", Kategorie=f"{ERF}, {KIEZ}", Tags="Frühe Neuzeit, Religion, Architektur", Flag=LO,
         teaser="Die Bornheimer Dorfkirche brannte in den 1770er Jahren nach einem Blitzschlag bis auf die Mauern nieder. "
                "Johann Andreas Liebhardt baute sie 1778/79 als barocke Saalkirche neu, und diesmal bekam sie einen Blitzableiter, "
                "der Überlieferung nach den ersten auf dem Gebiet des heutigen Frankfurt.",
         quellen=["Waymarking | https://www.waymarking.com/waymarks/WMDQHM_Johanniskirche_Frankfurt_am_Main_Germany",
                  "ich-geh-wandern.de | https://www.ich-geh-wandern.de/frankfurt-bornheim"],
         zeitraum="1778/79", jahr=1778, status="Prüfen"),
    dict(ort="bornheim-johanniskirche", Name="Die Bernemer Kerb", Kategorie=KIEZ, Tags="Frühe Neuzeit, Nachtleben", Flag=LO,
         teaser="Aus dem Kirchweihfest der Bornheimer Kirche wurde eines der ältesten Volksfeste Frankfurts, gefeiert seit Anfang des 17. Jahrhunderts. "
                "Jeden August ziehen die Kerbeburschen durch Alt-Bornheim und die Berger Straße. Dazu gehören der Gickelschmiss und zum Schluss die Lisbethverbrennung.",
         quellen=["Frankfurt-Tipp | https://www.frankfurt-tipp.de/en/index/news/s/ugc/lord-mayor-peter-feldmann-opens-the-bernemer-kerb.html",
                  "Festivals in Deutschland | https://www.festivalsindeutschland.de/festival/bernemer-kerb-frankfurt-bornheim/2025"],
         zeitraum="seit ca. 1608", jahr=1608, status="Prüfen"),
    dict(ort="bornheim-uhrtuermchen", Name="Das lustige Dorf", Kategorie=f"{KIEZ}, {SAGE}", Tags="19. Jahrhundert, Spitzname, Nachtleben", Flag=LO,
         teaser="Bornheim lag jahrhundertelang vor den Toren Frankfurts und wurde erst 1877 Stadtteil. Die Frankfurter kamen zum Feiern: "
                "Apfelweinwirtschaften, Tanzböden und, so heißt es, auch käufliche Liebe brachten dem Ort den Beinamen „das lustige Dorf“. "
                "Rund um das Uhrtürmchen an der oberen Berger Straße ist bis heute Markt, der Wochenmarkt besteht seit 1873.",
         quellen=["Journal Frankfurt | https://www.journal-frankfurt.de/journal_news/stadtleben-2/Frankfurts-lustiges-Dorf-Bornheim-ist-stets-im-Wandel-44932.html",
                  "Wikipedia (en) | https://en.wikipedia.org/wiki/Bornheim_(Frankfurt_am_Main)",
                  "Visit Frankfurt, Wochenmarkt | https://www.visitfrankfurt.travel/en/event/bornheim-weekly-market"],
         zeitraum="bis 1877", jahr=1877, status="Prüfen"),
    dict(ort="bornheim-friedberger-warte", Name="Der Wachturm auf dem Eulenberg", Kategorie=GP, Tags="Mittelalter & früher, Architektur", Flag=LO,
         teaser="Die Friedberger Warte steht auf dem Eulenberg, dem höchsten Punkt Bornheims, wo die Straße nach Friedberg die Frankfurter Landwehr verließ. "
                "Schon um 1350 stand hier ein Wachturm, der heutige spätgotische Turm stammt von 1478.",
         quellen=["ich-geh-wandern.de | https://www.ich-geh-wandern.de/frankfurt-bornheim",
                  "Friedberger Landstraße (dewiki) | https://de-academic.com/dic.nsf/dewiki/471610"],
         zeitraum="1478", jahr=1478, status="Prüfen"),
    dict(ort="bornheim-bornheimer-hang", Name="Ernst Mays Siedlung am Hang", Kategorie=f"{GP}, {KIEZ}", Tags="Weimarer Republik, Architektur", Flag=LO,
         teaser="Von 1926 bis 1930 entstanden am Bornheimer Hang 1.540 Wohnungen des Neuen Frankfurt. Weil die Siedlung an alte Bebauung grenzt, "
                "gab Ernst May den Häusern dort Satteldächer statt der sonst üblichen Flachdächer. Der geplante Mittelteil wurde nie gebaut, "
                "der zentrale Platz heißt seit den 1990ern Ernst-May-Platz.",
         quellen=["Wikipedia (en), New Frankfurt | https://en.wikipedia.org/wiki/New_Frankfurt",
                  "Visit Frankfurt | https://www.visitfrankfurt.travel/en/poi/bornheimer-hang-housing-estate",
                  "modernism-in-architecture | https://modernism-in-architecture.org/buildings/bornheimer-hang/"],
         zeitraum="1926–1930", jahr=1926, status="Entwurf"),
    # ---------- Bahnhofsviertel ----------
    dict(ort="bahnhofsviertel-kaiserstrasse", Name="Ein Viertel auf alten Gleisen", Kategorie=f"{WEG}, {GP}", Tags="19. Jahrhundert, Kaiserreich, Verkehr, Architektur", Flag=LO,
         teaser="Wo heute das Bahnhofsviertel liegt, endeten bis 1888 drei Bahnen in drei Bahnhöfen nebeneinander: Main-Weser-, Taunus- und Main-Neckar-Bahnhof. "
                "Am 18. August 1888 ersetzte sie der neue Centralbahnhof, und auf den frei gewordenen Gleisflächen entstand bis zum Ersten Weltkrieg "
                "ein Gründerzeitviertel mit der Kaiserstraße als Prachtallee. Noch früher lag hier das Galgenfeld.",
         quellen=["Denkmalamt Frankfurt, Faltblatt Westbahnhöfe | https://frankfurt.de/-/media/frankfurtde/service-und-rathaus/verwaltung/aemter-und-institutionen/denkmalamt/pdf/faltblatt_01_die_westbahnhoefe_72dpi.pdf",
                  "Wikipedia (en) | https://en.wikipedia.org/wiki/Frankfurt_western_stations",
                  "entwicklungsstadt | https://www.entwicklungsstadt.de/bahnhofsviertel-die-entstehung-des-frankfurter-eingangstors/"],
         zeitraum="1839–1914", jahr=1888, status="Entwurf"),
    dict(ort="bahnhofsviertel-niddastrasse", Name="Der Frankfurter Weg", Kategorie=f"{GP}, {KIEZ}", Tags="Wende & Gegenwart", Flag=LO,
         teaser="Anfang der 1990er Jahre lebte in der Taunusanlage eine große offene Drogenszene. Stadt, Drogenhilfe, Polizei und Justiz entwickelten daraufhin "
                "den „Frankfurter Weg“: Prävention, Therapie, Überlebenshilfe und Strafverfolgung als letztes Mittel. Aus dem Spritzentausch entstanden Druckräume, "
                "der erste 1994. Heute konzentrieren sich Szene und Hilfen im Bahnhofsviertel, und mit Crack steht das Modell erneut zur Debatte.",
         quellen=["Correctiv | https://correctiv.org/aktuelles/artikel-aktuelles/2015/06/05/rausch-unter-aufsicht/",
                  "Journal Frankfurt, Frankfurter Weg 2.0 | https://www.journal-frankfurt.de//journal_news/Politik-10/Frankfurter-Weg-20-Frankfurt-richtet-seine-Drogenpolitik-neu-aus-44426.html",
                  "Drogenreferat Frankfurt, Jahresbericht | https://frankfurt.de/-/media/frankfurtde/service-und-rathaus/verwaltung/aemter-und-institutionen/drogenreferat/pdf/jahresbericht-drogenreferat-2010-2012.ashx"],
         zeitraum="seit 1990", jahr=1992, status="Prüfen"),
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
