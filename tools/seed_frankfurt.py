import json, sys

# (id, title, kind, importance, themes, epochs, stadtteil, address, year, lat, lon, teaser, story[])
I = []
def add(*a): I.append(a)

add("roemer", "Römer", "Rathaus", 3, ["Geschichte", "Architektur"], ["Mittelalter", "Frühe Neuzeit"],
    "Altstadt", "Römerberg 27", "seit 1405", 50.11055, 8.68215,
    "Seit über 600 Jahren das Rathaus der Stadt und Schauplatz der Kaiserkrönungen.",
    ["1405 kaufte der Rat der Stadt die beiden Bürgerhäuser „Zum Römer“ und „Zum Goldenen Schwan“ und machte sie zum Rathaus. Woher der Name „Römer“ stammt, ist nicht sicher geklärt; eine verbreitete Deutung verweist auf italienische Kaufleute, die hier zu Messezeiten handelten.",
     "Nach den Krönungen im Dom zog der neue Kaiser über den Krönungsweg hierher. Im Kaisersaal fand das Krönungsbankett statt. Die 52 Kaiserbildnisse an den Wänden entstanden erst im 19. Jahrhundert und zeigen die Herrscher von Karl dem Großen bis Franz II.",
     "Die heute so bekannte Stufengiebel-Fassade ist im Kern spätmittelalterlich, wurde aber mehrfach verändert und nach der Zerstörung 1944 wieder aufgebaut."])

add("dom", "Kaiserdom St. Bartholomäus", "Kirche", 3, ["Geschichte", "Religion", "Architektur"], ["Mittelalter", "Frühe Neuzeit", "19. Jahrhundert"],
    "Altstadt", "Domplatz 1", "Wahlort seit 1356", 50.11070, 8.68525,
    "Hier wurden die römisch-deutschen Könige gewählt und später gekrönt, obwohl der Dom nie Bischofssitz war.",
    ["Streng genommen ist der „Dom“ keine Kathedrale, denn Frankfurt war nie Sitz eines Bischofs. Seine Bedeutung kam von woanders: Die Goldene Bulle Kaiser Karls IV. legte 1356 Frankfurt als Ort der Königswahl fest, die Kurfürsten berieten dafür in der Wahlkapelle.",
     "Von 1562 bis 1792 fanden hier auch die Krönungen statt, die zuvor in Aachen stattgefunden hatten. Zehn Kaiser wurden in dieser Zeit im Dom gekrönt.",
     "Der rund 95 Meter hohe Westturm wurde ab 1415 gebaut, blieb aber jahrhundertelang unvollendet. Erst nach dem großen Dombrand von 1867 erhielt er seine heutige Spitze."])

add("pfalz", "Kaiserpfalz Franconofurd", "Archäologische Stätte", 3, ["Geschichte"], ["Mittelalter"],
    "Altstadt", "Archäologischer Garten, Domplatz", "794", 50.11045, 8.68440,
    "Die erste schriftliche Erwähnung Frankfurts stammt von 794, als Karl der Große hier eine Synode abhielt.",
    ["Am 22. Februar 794 stellte Karl der Große eine Urkunde „super fluvium Moin in loco nuncupante Franconofurd“ aus, am Main an dem Ort, der Franconofurd genannt wird. Das ist die älteste bekannte Nennung der Stadt.",
     "Im selben Jahr versammelte Karl hier eine große Reichssynode, auf der unter anderem über die Bilderverehrung und Glaubensfragen gestritten wurde.",
     "Zwischen Dom und Schirn sind im Archäologischen Garten und im Stadthaus Mauerreste der karolingischen Königspfalz und älterer römischer Bauten zu sehen."])

add("furt-sage", "Die Furt der Franken", "Sagenort", 3, ["Sage", "Legende"], ["Mittelalter"],
    "Altstadt", "Mainkai, unterhalb des Doms", "Gründungssage", 50.10870, 8.68600,
    "Eine Hirschkuh soll Karl dem Großen auf der Flucht vor den Sachsen den Weg durch den Main gezeigt haben.",
    ["Der Sage nach wurde Karl der Große mit seinem Heer von den Sachsen bis an den Main gedrängt. Dichter Nebel lag über dem Fluss, eine Brücke gab es nicht.",
     "Da sah man eine Hirschkuh mit ihrem Jungen durch das Wasser waten. Sie zeigte eine seichte Stelle, an der die Franken den Fluss sicher durchqueren konnten. Die Sachsen, die den Weg nicht kannten, blieben zurück.",
     "Zum Dank soll der Ort den Namen „Furt der Franken“ erhalten haben. Der Name Frankfurt geht tatsächlich auf eine Furt zurück, die Geschichte mit der Hirschkuh ist aber eine Sage."])

add("alte-bruecke", "Alte Brücke und Brickegickel", "Brücke", 2, ["Sage", "Geschichte"], ["Mittelalter"],
    "Altstadt", "Alte Brücke", "erstmals 1222 erwähnt", 50.10745, 8.68880,
    "Ein goldener Hahn auf der Brücke erinnert an einen Baumeister, der den Teufel überlistete.",
    ["Die Alte Brücke war über Jahrhunderte der einzige feste Übergang über den Main zwischen Frankfurt und Sachsenhausen. Sie wurde 1222 erstmals urkundlich erwähnt.",
     "Die Sage erzählt von einem Baumeister, der mit dem Bau nicht rechtzeitig fertig wurde und einen Pakt mit dem Teufel schloss: Der Teufel vollendet die Brücke und bekommt dafür die erste Seele, die sie überquert. Der Baumeister trieb am Eröffnungstag einen Hahn über die Brücke. Der betrogene Teufel zerriss das Tier und schleuderte es durch die Brücke, und die zwei Löcher, die dabei entstanden, ließen sich angeblich nie wieder schließen.",
     "Ein vergoldeter Hahn auf einer Stange an der Brücke, auf Frankfurterisch der „Brickegickel“, erinnert bis heute an die Geschichte."])

add("eschenheimer-turm", "Eschenheimer Turm", "Stadtturm", 3, ["Sage", "Geschichte", "Architektur"], ["Mittelalter"],
    "Innenstadt", "Eschenheimer Tor", "1400–1428", 50.11705, 8.68210,
    "Die neun Löcher in der Wetterfahne soll ein Wilderer geschossen haben, um sein Leben zu retten.",
    ["Der Eschenheimer Turm war Teil der spätmittelalterlichen Stadtbefestigung und ist das älteste fast unveränderte Bauwerk der Frankfurter Innenstadt.",
     "Der Sage nach saß hier der Wilderer Hans Winkelsee gefangen und wartete auf seine Hinrichtung. Er bot dem Rat einen Handel an: Wenn er mit neun Schüssen eine Neun in die Wetterfahne auf dem Turm schieße, solle man ihn freilassen. Jeder Schuss saß.",
     "Die Wetterfahne mit den neun Einschusslöchern ist bis heute zu sehen. Ob die Geschichte stimmt, ist nicht belegt, aber kaum ein Frankfurter Bauwerk hat eine bekanntere Sage."])

add("paulskirche", "Paulskirche", "Kirche, Gedenkort", 3, ["Geschichte", "Erinnerung"], ["19. Jahrhundert", "20. Jahrhundert"],
    "Altstadt", "Paulsplatz 11", "1848/49", 50.11140, 8.68075,
    "Hier tagte 1848 das erste frei gewählte gesamtdeutsche Parlament.",
    ["Am 18. Mai 1848 zogen die Abgeordneten der Nationalversammlung in die Paulskirche ein. Sie arbeiteten eine Verfassung mit Grundrechten aus, die Paulskirchenverfassung von 1849, die viele Ideen des späteren Grundgesetzes vorwegnahm.",
     "Das Parlament scheiterte, als der preußische König die angebotene Kaiserkrone ablehnte. Die Paulskirche gilt dennoch als Wiege der deutschen Demokratie.",
     "Nach der Zerstörung 1944 wurde sie als eines der ersten Gebäude der Stadt bis 1948 wieder aufgebaut. Heute wird hier unter anderem der Friedenspreis des Deutschen Buchhandels verliehen."])

add("goethe-haus", "Goethe-Haus", "Wohnhaus, Museum", 3, ["Persönlichkeit", "Kultur"], ["Frühe Neuzeit"],
    "Innenstadt", "Großer Hirschgraben 23", "1749", 50.11100, 8.67765,
    "Geburtshaus von Johann Wolfgang von Goethe, der hier am 28. August 1749 zur Welt kam.",
    ["Goethe wurde in diesem Haus geboren und verbrachte hier seine Kindheit und Jugend. In „Dichtung und Wahrheit“ beschreibt er das Haus, das Puppentheater, das er als Kind geschenkt bekam, und das Treiben der Krönungsfeierlichkeiten von 1764.",
     "Hier schrieb er auch frühe Werke wie den „Götz von Berlichingen“ und „Die Leiden des jungen Werthers“.",
     "Das Haus wurde 1944 zerstört, die Einrichtung war zuvor ausgelagert worden. Nach dem Wiederaufbau 1951 ist es mit dem Deutschen Romantik-Museum nebenan zu besichtigen."])

add("justitia", "Gerechtigkeitsbrunnen", "Brunnen", 2, ["Geschichte", "Kultur"], ["Frühe Neuzeit", "19. Jahrhundert"],
    "Altstadt", "Römerberg", "Krönungsfeste", 50.11040, 8.68235,
    "Bei Kaiserkrönungen soll aus diesem Brunnen Wein statt Wasser geflossen sein.",
    ["Der Brunnen mit der Justitia steht mitten auf dem Römerberg. Die heutige Bronzefigur stammt von 1887 und ersetzte eine ältere Steinfigur.",
     "Bei den Krönungsfesten wurde das Volk auf dem Römerberg bewirtet: Ein ganzer Ochse wurde gebraten, und aus dem Brunnen floss Wein. Bei Feierlichkeiten wurde dieser Brauch später gelegentlich wiederholt.",
     "Auffällig: Die Frankfurter Justitia trägt keine Augenbinde."])

add("nikolai", "Alte Nikolaikirche", "Kirche", 1, ["Religion", "Architektur"], ["Mittelalter"],
    "Altstadt", "Römerberg 11", "13. Jahrhundert", 50.10985, 8.68300,
    "Die kleine Kirche am Römerberg diente einst als Ratskapelle.",
    ["Die Alte Nikolaikirche wurde im 13. Jahrhundert errichtet und war zeitweise die Hofkapelle der Staufer und danach Ratskapelle des Magistrats.",
     "Vom Dach aus ließ sich das Treiben auf dem Römerberg beobachten. Heute ist die Kirche vor allem für ihr Glockenspiel bekannt, das mehrmals am Tag erklingt."])

add("steinernes-haus", "Steinernes Haus", "Bürgerhaus", 1, ["Architektur", "Kultur"], ["Mittelalter"],
    "Altstadt", "Markt 44", "1464", 50.11085, 8.68380,
    "Ein steinernes Patrizierhaus zwischen lauter Fachwerk, heute Sitz des Kunstvereins.",
    ["Das Haus wurde 1464 für den Kaufmann Johann von Melem gebaut. Es war ganz aus Stein gemauert, was in der von Fachwerk geprägten Altstadt auffiel und ihm seinen Namen gab.",
     "Nach der Zerstörung im Zweiten Weltkrieg wurde es wieder aufgebaut und ist heute Sitz des Frankfurter Kunstvereins."])

add("goldene-waage", "Haus zur Goldenen Waage", "Fachwerkhaus", 1, ["Architektur"], ["Frühe Neuzeit", "Gegenwart"],
    "Altstadt", "Markt 5", "1619 / 2018", 50.11075, 8.68440,
    "Das prächtigste Fachwerkhaus der Neuen Altstadt, nach alten Plänen rekonstruiert.",
    ["Der niederländische Kaufmann Abraham van Hamel ließ das Haus 1618/19 errichten. Die Waage im Namen weist auf sein Gewerbe hin.",
     "1944 brannte es aus. Im Zuge des Dom-Römer-Projekts wurde es bis 2018 mit originalen Spolien und nach historischen Fotos und Plänen rekonstruiert."])

add("struwwelpeter", "Struwwelpeter-Museum", "Museum", 2, ["Persönlichkeit", "Kultur"], ["19. Jahrhundert"],
    "Altstadt", "Hinter dem Lämmchen 2–4", "1845", 50.11100, 8.68400,
    "Der Frankfurter Arzt Heinrich Hoffmann erfand den Struwwelpeter als Weihnachtsgeschenk für seinen Sohn.",
    ["1844 suchte Heinrich Hoffmann ein Bilderbuch für seinen dreijährigen Sohn und fand nichts, was ihm gefiel. Also zeichnete und dichtete er selbst: den Struwwelpeter, den Suppen-Kaspar, Paulinchen mit dem Feuerzeug.",
     "Freunde überredeten ihn, das Heft zu veröffentlichen. 1845 erschien es und wurde eines der erfolgreichsten deutschen Kinderbücher.",
     "Hoffmann war im Hauptberuf Arzt und leitete später die städtische Anstalt für Irre und Epileptische. Das Museum zeigt sein Werk seit 2019 in der Neuen Altstadt."])

add("saalhof", "Saalhof und Rententurm", "Burg, Museum", 2, ["Geschichte", "Architektur"], ["Mittelalter"],
    "Altstadt", "Saalhof 1", "um 1200", 50.10960, 8.68180,
    "Die Saalhofkapelle aus der Stauferzeit ist das älteste erhaltene Bauwerk der Altstadt.",
    ["Am Mainufer stand ab dem 12. Jahrhundert ein staufischer Königshof. Seine Kapelle aus der Zeit um 1200 ist erhalten und gilt als ältestes Gebäude der Frankfurter Altstadt.",
     "Der Rententurm daneben wurde um 1456 als Teil der Mainbefestigung gebaut. Hier saß das Rentamt, das Zölle und Abgaben einzog. Heute gehört das Ensemble zum Historischen Museum."])

add("haus-wertheim", "Haus Wertheim", "Fachwerkhaus", 1, ["Architektur", "Geschichte"], ["Frühe Neuzeit"],
    "Altstadt", "Fahrtor 1", "um 1600", 50.10985, 8.68225,
    "Das einzige Fachwerkhaus der Altstadt, das die Bombennächte von 1944 überstand.",
    ["Bei den Luftangriffen im März 1944 brannte die mittelalterliche Altstadt fast vollständig nieder. Haus Wertheim blieb als einziges Fachwerkhaus stehen.",
     "Es wird erzählt, dass Feuerwehrleute es gezielt hielten, um einen Fluchtweg aus der brennenden Altstadt zum Main offen zu halten. Ob es so war, ist nicht gesichert, das Haus ist aber das einzige echte Fachwerk-Original der Altstadt."])

add("judengasse", "Judengasse und Börneplatz", "Gedenkort, Museum", 3, ["Geschichte", "Erinnerung", "Persönlichkeit"], ["Mittelalter", "Frühe Neuzeit", "20. Jahrhundert"],
    "Innenstadt", "Battonnstraße 47", "1462–1811", 50.11180, 8.68960,
    "Über drei Jahrhunderte mussten Frankfurts Juden in einer einzigen engen Gasse leben, darunter die Familie Rothschild.",
    ["1462 zwang der Rat die jüdische Gemeinde, aus der Nähe des Doms in eine Gasse vor der damaligen Stadtmauer zu ziehen. In der Judengasse lebten zeitweise rund 3.000 Menschen auf engstem Raum, nachts und an Feiertagen wurden die Tore verschlossen.",
     "1744 wurde hier Mayer Amschel Rothschild geboren, der Begründer des Bankhauses Rothschild. Erst Anfang des 19. Jahrhunderts fiel der Ghettozwang.",
     "Das Museum Judengasse zeigt Fundamente der Häuser. Am Neuen Börneplatz erinnert eine Gedenkstätte mit über 11.000 Namen an die Frankfurter Juden, die im Holocaust ermordet wurden."])

add("grossmarkthalle", "Großmarkthalle und Erinnerungsstätte", "Gebäude, Gedenkort", 2, ["Erinnerung", "Architektur", "Geschichte"], ["20. Jahrhundert", "Gegenwart"],
    "Ostend", "Sonnemannstraße 20", "1928 / 1941–1945", 50.10970, 8.70250,
    "Aus dem Keller der Großmarkthalle wurden mehr als 10.000 Frankfurter Juden deportiert. Heute steht hier die EZB.",
    ["Die Großmarkthalle von Martin Elsaesser wurde 1928 eröffnet und war ein Hauptwerk des Neuen Frankfurt.",
     "Zwischen 1941 und 1945 nutzte die Gestapo den Keller und die Gleisanlagen der Halle als Sammelstelle. Von hier aus wurden über 10.000 Jüdinnen und Juden in Ghettos und Vernichtungslager deportiert.",
     "Seit 2014 ist die Halle Teil des Sitzes der Europäischen Zentralbank. Eine Erinnerungsstätte am Gelände erinnert an die Deportationen."])

add("auschwitz-prozess", "Haus Gallus und der Auschwitz-Prozess", "Gebäude, Gedenkort", 2, ["Erinnerung", "Persönlichkeit", "Geschichte"], ["20. Jahrhundert"],
    "Gallus", "Frankenallee 111", "1963–1965", 50.10480, 8.64380,
    "Hier verhandelte das Frankfurter Schwurgericht im ersten großen Auschwitz-Prozess.",
    ["Der hessische Generalstaatsanwalt Fritz Bauer brachte gegen große Widerstände den Prozess gegen Angehörige der SS-Wachmannschaft von Auschwitz zustande.",
     "Die Verhandlung begann im Dezember 1963 im Römer und zog wegen des großen Andrangs 1964 in das Bürgerhaus Haus Gallus um. Der Prozess endete im August 1965 und veränderte den Umgang der Bundesrepublik mit den NS-Verbrechen nachhaltig."])

add("hauptwache", "Hauptwache", "Wachgebäude", 2, ["Geschichte", "Architektur"], ["Frühe Neuzeit", "19. Jahrhundert"],
    "Innenstadt", "An der Hauptwache 15", "1730", 50.11395, 8.67880,
    "Das barocke Wachhaus gab dem zentralen Platz der Stadt seinen Namen.",
    ["Die Hauptwache wurde 1729/30 als Sitz der Stadtwehr und als Gefängnis gebaut.",
     "Am 3. April 1833 stürmten Studenten und Bürger die Wache, um eine Revolution in ganz Deutschland auszulösen. Der Frankfurter Wachensturm scheiterte nach kurzer Zeit.",
     "Heute ist das Gebäude ein Café, unter dem Platz liegt einer der wichtigsten Nahverkehrsknoten der Stadt."])

add("gretchen", "Susanna Margaretha Brandt", "Ereignisort", 2, ["Persönlichkeit", "Geschichte", "Kultur"], ["Frühe Neuzeit"],
    "Innenstadt", "Platz an der Hauptwache", "1772", 50.11425, 8.67815,
    "Ihr Schicksal inspirierte Goethe zur Gretchen-Tragödie im „Faust“.",
    ["Die Magd Susanna Margaretha Brandt tötete 1771 ihr neugeborenes Kind. Am 14. Januar 1772 wurde sie vor der Hauptwache mit dem Schwert hingerichtet.",
     "Der junge Goethe, damals Anwalt in Frankfurt, verfolgte den Prozess genau. Ihr Fall gilt als Vorbild für Gretchen, die im „Faust“ ebenfalls ihr Kind tötet und dafür verurteilt wird."])

add("katharinenkirche", "Katharinenkirche", "Kirche", 1, ["Religion", "Persönlichkeit"], ["Mittelalter", "Frühe Neuzeit"],
    "Innenstadt", "An der Hauptwache 1", "1681", 50.11425, 8.67960,
    "Hier begann 1522 die Reformation in Frankfurt, und Goethe wurde hier konfirmiert.",
    ["In der Vorgängerkirche predigte Hartmann Ibach 1522 im Sinne Luthers. Damit hielt die Reformation in Frankfurt Einzug.",
     "Der heutige barocke Bau entstand 1678 bis 1681. Die Familie Goethe gehörte zur Gemeinde, der junge Johann Wolfgang wurde hier konfirmiert."])

add("alte-oper", "Alte Oper", "Konzerthaus", 3, ["Kultur", "Architektur", "Geschichte"], ["19. Jahrhundert", "20. Jahrhundert"],
    "Innenstadt", "Opernplatz 1", "1880", 50.11590, 8.67205,
    "Ein Opernhaus, das die Bürger erst bezahlten, dann als Ruine fast verloren und dann wieder aufbauten.",
    ["Das Opernhaus wurde 1880 eröffnet, finanziert zu einem großen Teil von Frankfurter Bürgern. Über dem Eingang steht „Dem Wahren Schönen Guten“. Kaiser Wilhelm I. soll bei der Eröffnung gesagt haben: „Das könnte ich mir in Berlin nicht leisten.“",
     "Im Zweiten Weltkrieg brannte das Haus aus. Jahrzehntelang stand die Ruine leer und wurde „Deutschlands schönste Ruine“ genannt, sogar ein Abriss war im Gespräch.",
     "Eine Bürgerinitiative sammelte Spenden für den Wiederaufbau. 1981 wurde die Alte Oper als Konzert- und Kongresshaus neu eröffnet."])

add("boerse", "Börse mit Bulle und Bär", "Gebäude, Skulptur", 2, ["Geschichte", "Kultur"], ["19. Jahrhundert", "Gegenwart"],
    "Innenstadt", "Börsenplatz 4", "1879", 50.11530, 8.67625,
    "Frankfurt ist einer der ältesten Börsenplätze der Welt, die Bronzetiere davor sind ein beliebtes Fotomotiv.",
    ["Die Frankfurter Börse geht auf das Jahr 1585 zurück, als Kaufleute auf der Messe einheitliche Wechselkurse festlegten. Das heutige Gebäude am Börsenplatz wurde 1879 eingeweiht.",
     "Vor dem Haus stehen Bulle und Bär, Symbole für steigende und fallende Kurse. Der Bulle stößt seine Hörner nach oben, der Bär schlägt mit der Tatze nach unten."])

add("schopenhauer", "Schopenhauer an der Schönen Aussicht", "Wohnort", 2, ["Persönlichkeit"], ["19. Jahrhundert"],
    "Altstadt", "Schöne Aussicht 16", "1833–1860", 50.10910, 8.68780,
    "Der Philosoph Arthur Schopenhauer lebte fast drei Jahrzehnte in Frankfurt, stets begleitet von einem Pudel.",
    ["Schopenhauer zog 1833 nach Frankfurt und blieb bis zu seinem Tod 1860. Die meisten Jahre wohnte er an der Schönen Aussicht direkt am Main.",
     "Die Frankfurter kannten ihn als Sonderling, der täglich spazieren ging, im Englischen Hof zu Mittag aß und seine Pudel, die alle Atma hießen, über alles schätzte. Sein Grab liegt auf dem Hauptfriedhof."])

add("hauptfriedhof", "Hauptfriedhof", "Friedhof", 1, ["Persönlichkeit", "Natur", "Kultur"], ["19. Jahrhundert"],
    "Nordend-West", "Eckenheimer Landstraße 194", "1828", 50.12870, 8.68760,
    "Auf dem parkartigen Friedhof liegen Schopenhauer, Heinrich Hoffmann und Theodor W. Adorno.",
    ["Der Hauptfriedhof wurde 1828 eröffnet und gehört zu den großen historischen Friedhöfen in Deutschland.",
     "Zwischen alten Bäumen liegen zahlreiche bekannte Frankfurter, darunter Arthur Schopenhauer, Struwwelpeter-Erfinder Heinrich Hoffmann und der Philosoph Theodor W. Adorno."])

add("kuhhirtenturm", "Kuhhirtenturm", "Stadtturm", 1, ["Persönlichkeit", "Architektur"], ["Mittelalter", "20. Jahrhundert"],
    "Sachsenhausen-Nord", "Alt-Sachsenhausen, am Mainufer", "15. Jahrhundert", 50.10570, 8.68980,
    "Im letzten erhaltenen Turm der Sachsenhäuser Befestigung wohnte einst der Komponist Paul Hindemith.",
    ["Der Turm gehörte zur Befestigung von Sachsenhausen und ist als einziger Teil davon erhalten. Seinen Namen hat er vom Kuhhirten, der hier zeitweise wohnte.",
     "Von 1923 bis 1927 lebte der Komponist Paul Hindemith im Turm. Heute erinnert eine Ausstellung an ihn."])

add("frau-rauscher", "Frau-Rauscher-Brunnen", "Brunnen", 2, ["Kultur"], ["20. Jahrhundert"],
    "Sachsenhausen-Nord", "Klappergasse", "Fastnachtslied", 50.10465, 8.68890,
    "Eine Brunnenfigur aus einem Fastnachtslied, die unaufmerksame Passanten nass spritzt.",
    ["„Frau Rauscher aus de Klappergass, die hat e Beul am Ei“: Das Lied über die streitbare Frau aus der Klappergasse ist einer der bekanntesten Frankfurter Fastnachtsschlager.",
     "Der Brunnen zeigt eine füllige Frau mit Beule am Kopf. In unregelmäßigen Abständen spuckt sie einen kräftigen Wasserstrahl auf den Gehweg, zur Freude aller, die nicht getroffen werden."])

add("aeppelwoi", "Apfelwein in Alt-Sachsenhausen", "Kulturort", 2, ["Kultur"], ["19. Jahrhundert", "Gegenwart"],
    "Sachsenhausen-Nord", "Große Rittergasse", "Tradition", 50.10520, 8.68690,
    "Bembel, Geripptes und Handkäs mit Musik: In den Gassen von Sachsenhausen schlägt das Herz der Apfelweinkultur.",
    ["In Sachsenhausen gab es früher viele Weinbauern. Als der Weinbau zurückging, wurde Apfelwein zum Getränk der Stadt. In den Apfelweinwirtschaften wird er bis heute aus dem grauen, blau bemalten Steinzeugkrug, dem Bembel, ins „Gerippte“ eingeschenkt.",
     "Ein grüner Kranz über der Tür zeigt traditionell, dass frischer Apfelwein ausgeschenkt wird. Dazu gibt es Handkäs mit Musik oder Grüne Soße."])

add("eiserner-steg", "Eiserner Steg", "Brücke", 2, ["Geschichte", "Architektur"], ["19. Jahrhundert", "20. Jahrhundert"],
    "Altstadt", "Eiserner Steg", "1869", 50.10805, 8.68370,
    "Eine Fußgängerbrücke, die die Bürger selbst bezahlten und die heute unter tausenden Liebesschlössern ächzt.",
    ["Weil die Alte Brücke dem Verkehr nicht mehr genügte, gründeten Frankfurter Bürger eine Aktiengesellschaft und finanzierten den Steg selbst. 1869 wurde er eröffnet, für die Überquerung wurde anfangs Brückengeld verlangt.",
     "Im März 1945 sprengte die Wehrmacht den Steg, er wurde kurz nach dem Krieg wieder aufgebaut. Heute hängen an seinem Geländer unzählige Liebesschlösser."])

add("staedel", "Städel Museum", "Museum", 2, ["Kultur", "Persönlichkeit"], ["19. Jahrhundert"],
    "Sachsenhausen-Nord", "Schaumainkai 63", "1815", 50.10300, 8.67410,
    "Ein Kaufmann vermachte der Stadt seine Sammlung und sein Vermögen, daraus wurde eines der bedeutendsten Kunstmuseen Deutschlands.",
    ["Der Bankier und Kaufmann Johann Friedrich Städel verfügte in seinem Testament, dass aus seiner Kunstsammlung und seinem Vermögen eine Stiftung entstehen solle. Er starb 1816, das Testament von 1815 ist die Gründungsurkunde des Museums.",
     "Nach einem langen Erbstreit konnte das Städel seine Arbeit aufnehmen. Heute zeigt es Kunst aus sieben Jahrhunderten, darunter Werke von Dürer, Rembrandt und Tischbeins „Goethe in der Campagna“."])

add("gerbermuehle", "Gerbermühle", "Landhaus", 2, ["Persönlichkeit", "Kultur"], ["19. Jahrhundert"],
    "Oberrad", "Gerbermühlstraße 105", "1815", 50.10180, 8.72520,
    "Hier verliebte sich Goethe in Marianne von Willemer, die Suleika seines West-östlichen Divans.",
    ["Die Gerbermühle am Main war der Sommersitz des Bankiers Johann Jakob von Willemer. 1814 und 1815 war Goethe hier zu Gast.",
     "Zwischen ihm und Willemers junger Frau Marianne entstand eine tiefe Zuneigung, die in den „West-östlichen Divan“ einging. Erst lange nach ihrem Tod wurde bekannt, dass einige der schönsten Suleika-Gedichte von Marianne selbst stammen."])

add("palmengarten", "Palmengarten", "Park", 2, ["Natur", "Geschichte"], ["19. Jahrhundert"],
    "Westend-Süd", "Siesmayerstraße 61", "1871", 50.12360, 8.65720,
    "Die Pflanzen des abgesetzten Herzogs von Nassau wurden zum Grundstock eines Bürgergartens.",
    ["Nach der Annexion des Herzogtums Nassau durch Preußen 1866 verkaufte Herzog Adolph seine Pflanzensammlung aus Biebrich. Der Gärtner Heinrich Siesmayer und Frankfurter Bürger kauften sie und gründeten eine Aktiengesellschaft.",
     "1871 öffnete der Palmengarten mit dem großen Palmenhaus. Er ist bis heute einer der größten botanischen Gärten Deutschlands."])

add("senckenberg", "Senckenberg Naturmuseum", "Museum", 2, ["Natur", "Kultur"], ["19. Jahrhundert", "20. Jahrhundert"],
    "Westend-Süd", "Senckenberganlage 25", "1817 / 1907", 50.11750, 8.65190,
    "Dinosaurier vor der Tür und Urpferdchen aus der Grube Messel im Inneren.",
    ["Die Senckenbergische Naturforschende Gesellschaft wurde 1817 von Frankfurter Bürgern gegründet, Goethe hatte die Idee unterstützt. Der Name erinnert an den Arzt Johann Christian Senckenberg.",
     "Das Museum an der Senckenberganlage öffnete 1907. Bekannt ist es für seine Dinosaurierskelette und die Fossilien aus der Grube Messel bei Darmstadt."])

add("bockenheimer-warte", "Bockenheimer Warte", "Wachturm", 1, ["Geschichte", "Kultur"], ["Mittelalter", "20. Jahrhundert"],
    "Bockenheim", "Bockenheimer Landstraße / Senckenberganlage", "1435", 50.11985, 8.65275,
    "Ein mittelalterlicher Wachturm und daneben eine Straßenbahn, die scheinbar aus dem Boden bricht.",
    ["Die Bockenheimer Warte war einer der Türme der Frankfurter Landwehr, eines Rings aus Wall, Graben und Warten weit vor der Stadtmauer. Von hier aus konnten Wächter herannahende Gefahren melden.",
     "Am Eingang der U-Bahn-Station daneben ragt ein alter Straßenbahnwagen schräg aus dem Pflaster. Das Kunstwerk von 1986 sieht aus, als würde die Bahn aus dem Untergrund auftauchen."])

add("ig-farben", "IG-Farben-Haus", "Gebäude", 2, ["Geschichte", "Architektur", "Erinnerung"], ["20. Jahrhundert", "Gegenwart"],
    "Westend-Nord", "Norbert-Wollheim-Platz 1", "1931", 50.12570, 8.66680,
    "Konzernzentrale, US-Hauptquartier, Universität: Ein Gebäude, drei Epochen.",
    ["Hans Poelzig entwarf das riesige Verwaltungsgebäude für die IG Farben, das 1931 fertig wurde. Der Konzern war tief in die Verbrechen des NS-Regimes verstrickt, unter anderem durch das Werk bei Auschwitz-Monowitz.",
     "Nach 1945 war das Haus das Hauptquartier der amerikanischen Militärregierung, Dwight D. Eisenhower hatte hier sein Büro.",
     "Seit 2001 gehört es zur Goethe-Universität. Der Platz davor ist nach Norbert Wollheim benannt, einem Überlebenden, der die IG Farben auf Entschädigung verklagte."])

add("holzhausen", "Holzhausenschlösschen", "Wasserschloss", 1, ["Architektur", "Geschichte"], ["Frühe Neuzeit"],
    "Nordend-West", "Justinianstraße 5", "1729", 50.12575, 8.68080,
    "Ein kleines Wasserschloss im Park, einst Landsitz einer der ältesten Patrizierfamilien.",
    ["Die Familie von Holzhausen gehörte über Jahrhunderte zu den einflussreichsten Geschlechtern der Stadt. An der Stelle einer mittelalterlichen Wasserburg ließ sie 1727 bis 1729 das heutige barocke Schlösschen bauen.",
     "Heute nutzt die Frankfurter Bürgerstiftung das Haus für Konzerte, Lesungen und Ausstellungen."])

add("justinus", "Justinuskirche", "Kirche", 2, ["Religion", "Architektur"], ["Mittelalter"],
    "Höchst", "Justinusplatz", "9. Jahrhundert", 50.09935, 8.54500,
    "Eine der ältesten erhaltenen Kirchen Deutschlands, gebaut im 9. Jahrhundert.",
    ["Die Justinuskirche in Höchst wurde im 9. Jahrhundert gebaut und ist das älteste Gebäude Frankfurts. Teile des karolingischen Langhauses sind bis heute erhalten.",
     "Später kam ein gotischer Chor hinzu, die Antoniter betreuten die Kirche ab dem 15. Jahrhundert."])

add("hoechster-schloss", "Höchster Schloss", "Burg", 1, ["Geschichte", "Architektur"], ["Mittelalter", "Frühe Neuzeit"],
    "Höchst", "Schloßplatz", "14. Jahrhundert", 50.10035, 8.54380,
    "Die Mainzer Erzbischöfe kontrollierten von hier aus den Zoll auf dem Main.",
    ["Höchst gehörte lange zu Kurmainz. Die Erzbischöfe ließen hier eine Burg errichten, um den Main-Handel zu kontrollieren und Zoll zu erheben.",
     "Aus der Burg wurde später ein Renaissanceschloss. Bis 1928 war Höchst eine eigene Stadt, erst dann wurde es nach Frankfurt eingemeindet."])

add("bolongaro", "Bolongaropalast", "Palast", 1, ["Persönlichkeit", "Architektur"], ["Frühe Neuzeit"],
    "Höchst", "Bolongarostraße 109", "1772–1775", 50.10125, 8.54780,
    "Zwei italienische Tabakhändler bauten sich einen Palast, nachdem Frankfurt sie nicht als Bürger aufnehmen wollte.",
    ["Die Brüder Bolongaro handelten mit Schnupftabak und wurden damit reich. In Frankfurt wurden ihnen als Katholiken die vollen Bürgerrechte verweigert.",
     "Sie zogen ins kurmainzische Höchst und ließen dort ab 1772 einen Palast mit Garten zum Main bauen, der prächtiger ausfiel als vieles in Frankfurt selbst."])

add("nida", "Römerstadt NIDA", "Archäologische Stätte", 2, ["Geschichte"], ["Antike"],
    "Heddernheim", "Zwischen Heddernheim und Praunheim", "1.–3. Jahrhundert", 50.16420, 8.62900,
    "Lange vor Frankfurt gab es hier eine römische Stadt mit Thermen, Tempeln und Theater.",
    ["Im heutigen Heddernheim lag die römische Siedlung NIDA, Hauptort der Civitas Taunensium. Sie entstand im 1. Jahrhundert nach Christus und erlebte ihre Blüte im 2. Jahrhundert.",
     "Mit dem Rückzug der Römer hinter den Rhein um 260 wurde die Stadt aufgegeben. Funde aus NIDA, darunter Heiligtümer des Mithras-Kults, sind im Archäologischen Museum Frankfurt zu sehen."])

add("roemerstadt-may", "Siedlung Römerstadt", "Siedlung", 2, ["Architektur", "Geschichte", "Persönlichkeit"], ["20. Jahrhundert"],
    "Heddernheim", "Hadrianstraße", "1927–1928", 50.16600, 8.63450,
    "Ernst Mays Siedlung des Neuen Frankfurt, mit der Frankfurter Küche in jeder Wohnung.",
    ["Stadtbaurat Ernst May ließ in den 1920er Jahren zahlreiche Siedlungen bauen, um die Wohnungsnot zu lindern: das Neue Frankfurt. Die Römerstadt über dem Niddatal ist eine der bekanntesten.",
     "Die Wohnungen hatten fast alle die Frankfurter Küche der Architektin Margarete Schütte-Lihotzky, die als Urform der modernen Einbauküche gilt."])

add("anne-frank", "Geburtsort von Anne Frank", "Wohnhaus", 2, ["Persönlichkeit", "Erinnerung"], ["20. Jahrhundert"],
    "Dornbusch", "Marbachweg 307", "1929", 50.13880, 8.68420,
    "Anne Frank wurde 1929 in Frankfurt geboren und verbrachte hier ihre ersten Lebensjahre.",
    ["Anne Frank kam am 12. Juni 1929 in Frankfurt zur Welt. Die Familie wohnte zunächst im Marbachweg, später in der Ganghoferstraße.",
     "Nach der Machtübernahme der Nationalsozialisten emigrierte die Familie 1933/34 nach Amsterdam. Dort schrieb Anne im Versteck ihr Tagebuch. Eine Gedenktafel am Haus erinnert an sie."])

add("goetheturm", "Goetheturm", "Aussichtsturm", 1, ["Natur"], ["20. Jahrhundert", "Gegenwart"],
    "Sachsenhausen-Süd", "Am Goetheturm", "1931 / 2020", 50.09180, 8.70040,
    "Ein Holzturm am Rand des Stadtwalds, 2017 abgebrannt und von den Frankfurtern zurückgeholt.",
    ["Der Goetheturm wurde 1931 aus Holz gebaut und war mit 43 Metern einer der höchsten Holztürme Deutschlands. Von oben sieht man über den Stadtwald auf die Skyline.",
     "Im Oktober 2017 brannte der Turm durch Brandstiftung vollständig ab. Nach Spenden und viel Engagement aus der Stadt wurde er bis 2020 originalgetreu neu errichtet."])

add("lohrberg", "Lohrberg", "Berg, Weinberg", 1, ["Natur", "Kultur"], ["Gegenwart"],
    "Seckbach", "Lohrberg", "Weinlage", 50.15020, 8.73450,
    "Frankfurts einziger Weinberg, mit Blick über die ganze Stadt.",
    ["Früher wurde rund um Frankfurt viel Wein angebaut. Übrig geblieben ist der Lohrberger Hang in Seckbach, die einzige Weinlage innerhalb der Stadtgrenze.",
     "Der Lohrberg-Park auf der Kuppe ist ein beliebtes Ausflugsziel, von hier aus liegt die Skyline wie ein Modell vor einem."])

add("skyline", "Commerzbank-Tower", "Hochhaus", 2, ["Architektur", "Geschichte"], ["Gegenwart"],
    "Innenstadt", "Kaiserplatz", "1997", 50.11040, 8.67430,
    "Mit 259 Metern war der Turm von Norman Foster lange das höchste Gebäude der EU.",
    ["Frankfurt ist die einzige deutsche Stadt mit einer echten Hochhaus-Skyline, was ihr den Spitznamen „Mainhattan“ eingebracht hat.",
     "Der Commerzbank-Tower von Norman Foster wurde 1997 fertig. Er gilt als eines der ersten ökologischen Hochhäuser, mit Gärten, die sich spiralförmig über mehrere Etagen nach oben ziehen."])

add("rothschild-palais", "Rothschild-Palais", "Palais, Museum", 1, ["Persönlichkeit", "Erinnerung", "Kultur"], ["19. Jahrhundert", "Gegenwart"],
    "Innenstadt", "Untermainkai 14–15", "seit 1846", 50.10750, 8.67350,
    "Das ehemalige Wohnhaus der Rothschilds am Main beherbergt heute das Jüdische Museum.",
    ["Nach dem Ende des Ghettozwangs konnten jüdische Familien auch außerhalb der Judengasse wohnen. Die Familie Rothschild kaufte 1846 das klassizistische Palais am Untermainkai.",
     "Seit 1988 ist hier das Jüdische Museum Frankfurt untergebracht, das 2020 um einen Neubau erweitert wurde."])

add("leonhard", "Leonhardskirche", "Kirche", 1, ["Religion", "Architektur"], ["Mittelalter"],
    "Altstadt", "Am Leonhardstor 25", "ab 1219", 50.10925, 8.68060,
    "Kaiser Friedrich II. schenkte das Grundstück, die romanischen Portale sind bis heute erhalten.",
    ["1219 überließ der Staufer Friedrich II. den Frankfurter Bürgern ein Grundstück am Main für den Bau einer Kirche. Aus dieser Zeit stammen die beiden romanischen Portale.",
     "Die Leonhardskirche gehört zu den wenigen Kirchen der Altstadt, die den Zweiten Weltkrieg weitgehend unbeschadet überstanden."])

add("hessendenkmal", "Hessendenkmal", "Denkmal", 1, ["Geschichte", "Erinnerung"], ["Frühe Neuzeit"],
    "Innenstadt", "Friedberger Anlage", "1792", 50.11700, 8.68940,
    "Ein Denkmal für hessische Soldaten, die 1792 beim Sturm auf das französisch besetzte Frankfurt fielen.",
    ["Im Oktober 1792 besetzten französische Revolutionstruppen Frankfurt. Am 2. Dezember stürmten preußische und hessische Truppen das Friedberger Tor und eroberten die Stadt zurück.",
     "Der preußische König Friedrich Wilhelm II. stiftete das Denkmal für die gefallenen Hessen. Es steht bis heute an der Friedberger Anlage."])

feats = []
for (id_, title, kind, imp, themes, epochs, st, addr, year, lat, lon, teaser, story) in I:
    feats.append({
        "type": "Feature",
        "id": id_,
        "geometry": {"type": "Point", "coordinates": [lon, lat]},
        "properties": {
            "id": id_, "title": title, "kind": kind, "importance": imp,
            "themes": themes, "epochs": epochs,
            "place": {"stadtteil": st, "stadt": "Frankfurt am Main", "kreis": "Kreisfreie Stadt Frankfurt am Main", "bundesland": "Hessen"},
            "address": addr, "period": year, "teaser": teaser, "story": story,
            "sources": [{"label": "Wikipedia", "url": "https://de.wikipedia.org/w/index.php?search=" + title.replace(" ", "+") + "+Frankfurt"}],
            "status": "published", "author": "redaktion", "updated": "2026-10-20",
        }})

out = {"type": "FeatureCollection",
       "meta": {"schemaVersion": 1, "region": "Frankfurt am Main", "license": "Texte: eigene Zusammenfassung, Prototyp", "importanceScale": {"3": "Wahrzeichen", "2": "Bedeutend", "1": "Lokal"}},
       "features": feats}
json.dump(out, open(sys.argv[1], "w"), ensure_ascii=False, indent=2)
print(len(feats))
