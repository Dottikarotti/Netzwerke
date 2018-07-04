# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 13:38:24 2018

@author: BlackEmperor
"""

#!!!!WICHTIG!!!!
#Diesen Code könnt ihr einfach auf eurem Rechner ausführen. Ihr müsst also keine Verbindung
#zur iPython Konsole auf dem Server herstellen, sondern könnt den Code an eure eigene Konsole
#auf dem PC schicken (Console 1/A Fenster rechts unten).

import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import re

#######~~ SETUP ~~#######

###### LISTEN IMPORTIEREN ######

#Gebt hier jeweils den Pfad und Namen der Knoten bzw. Kantendatei an, die ihr aus der .zip
#von GitHub entpackt habt.
#Wichtig ist nur, dass ihr wirklich immer "\\" benutzt, zum Escapen des "\" Symbols im Pfad.
#Außerdem solltet ihr immer nur ein Genre gleichzeitig bearbeiten (also eine _knoten und eine
#_kanten Datei reinladen).
df1 = pd.read_pickle("C:\\Users\\BlackEmperor\\Desktop\\Projektarbeit\\chickflick_knoten")
df2 = pd.read_pickle("C:\\Users\\BlackEmperor\\Desktop\\Projektarbeit\\chickflick_kanten")
df4 = pd.read_pickle("C:\\Users\\BlackEmperor\\Desktop\\Projektarbeit\\ratedmformanly_knoten")
df5 = pd.read_pickle("C:\\Users\\BlackEmperor\\Desktop\\Projektarbeit\\ratedmformanly_kanten")

#Hier könnt ihr Tropelisten importieren.
df3 = pd.read_pickle("C:\\Users\\BlackEmperor\\Desktop\\Projektarbeit\\comedytropes")

#Duplikate im Knoten-Dataframe löschen.
df1 = df1.drop_duplicates(subset=0)
df4 = df4.drop_duplicates(subset=0)

#Hier werden die einzelnen Werte aus den DataFrames in Listen gepackt.
knotenliste_cf = df1[0].values.tolist()
knotenliste_rmfm = df4[0].values.tolist()
typeliste_cf = df1[1].values.tolist()
typeliste_rmfm = df4[1].values.tolist()
bipartite_kantenliste_cf = df2.values.tolist()
bipartite_kantenliste_rmfm = df5.values.tolist()
tropeliste = df3[0].values.tolist()

#Der Inhalt der Kantenliste wurde beim Export in das DataFrame von Tupeln in Listen umgewandelt.
#Diese Zeile macht das im Prinzip wieder rückgängig.
bipartite_kantenliste_cf = list(tuple(x) for x in bipartite_kantenliste_cf)
bipartite_kantenliste_rmfm = list(tuple(x) for x in bipartite_kantenliste_rmfm)
#Duplikate in der Kantenliste löschen.
bipartite_kantenliste_cf = list(set(bipartite_kantenliste_cf))
bipartite_kantenliste_rmfm = list(set(bipartite_kantenliste_rmfm))

#### COMEDYATTRIBUT & GENREATTRIBUT HINZUFÜGEN ####

#Hier setzen wir drei Sets von Vergleichslisten auf, einmal die (Comedy)-Tropeliste, dann die Knotenliste aus
#ChickFlicks und zuletzt die Knotenliste von Rated M For Manly. Dazu werden drei leere Matchlisten angelegt.
vergleichsliste_tropes = set(tropeliste)
vergleichsliste_g1 = set(knotenliste_cf)
vergleichsliste_g2 = set(knotenliste_rmfm)
matchliste_tropes_c_cf = []
matchliste_tropes_c_rmfm = []
matchliste_genre = []

#Hier schauen wir, welche Einträge (im Prinzip nur Tropes) sowohl in den ChickFlick Knoten als auch in der Trope-
#liste vorkommen. Diese Tropes werden in die Matchliste für Comedytropes (c) und ChickFlick (cf) eingetragen.
ueberschneidungsset_tropes_cf = vergleichsliste_tropes.intersection(vergleichsliste_g1)
for match in ueberschneidungsset_tropes_cf:
    matchliste_tropes_c_cf.append(match)
    
#Das ganze wiederholen wir jetzt für die Rated M For Manly Knoten (rmfm).
ueberschneidungsset_tropes_rmfm = vergleichsliste_tropes.intersection(vergleichsliste_g2)
for match in ueberschneidungsset_tropes_rmfm:
    matchliste_tropes_c_rmfm.append(match)
    
#Jetzt vergleichen wir die beiden Knotenlisten und schreiben alle Tropes in die Matchliste, die in beiden vorkommen.
ueberschneidungsset_genre = vergleichsliste_g1.intersection(vergleichsliste_g2)
for match in ueberschneidungsset_genre:
    matchliste_genre.append(match)
    
#Wir legen nun für jedes der beiden Genres eine neue Typeliste an.
typeliste_cf_neu = []
typeliste_rmfm_neu = []

#Wir erstellen nun eine Indexvariabel und setzen die auf 0. Die brauchen wir für die nächste Schleife.
index = 0
#Diese Schleife dient dazu, die Dictionaryeinträge in der Typeliste zu erweitern. Momentan sind dort die "types"
#der Knoten ("work" oder "trope") gespeichert. Wir wollen für jedes Element ein Attribut "comedytrope" hinzufügen, 
#das entweder mit "ja" oder "nein" belegt ist.
#Wir untersuchen jedes Element der Knotenliste.
for element in knotenliste_cf:
    #Zunächst speichern wir das Element an der Stelle "index" in der alten Typeliste als Variable "dict_element" ab.
    dict_element = typeliste_cf[index]
    #Wenn das Element in der Matchliste für Comedytropes und ChickFlick auftaucht...
    if element in matchliste_tropes_c_cf:
        #...wird das Dictionary in der Variable "dict_element" um den Dictionaryeintrag mit dem Key "comedytrope"
        #und dem Value "ja" erweitert.
        dict_element.update({"comedytrope": "ja"})
    #Wenn das Element dagegen nicht in der Matchliste auftaucht...
    else:
        #...wird der Eintrag stattdessen mit dem gleichen Key, aber dem Value "nein" erweitert.
        dict_element.update({"comedytrope": "nein"})
    #Als nächsten checken wir, ob das Element in der Genre-Matchliste auftaucht. Wenn ja...
    if element in matchliste_genre:
        #...erweitern wir den Eintrag mit einem Key "genre" und dem Wert "beide".
        dict_element.update({"genre": "beide"})
    #Wenn nicht...
    else:
        #...erhält der Key "genre" den Wert "Chick Flick".
        dict_element.update({"genre": "Chick Flick"})
    #Dieser neue, erweiterte Dictionaryeintrag wird nun der neuen Typeliste hinzugefügt.
    typeliste_cf_neu.append(dict_element)
    #Zuletzt erhöhen wir die Indexvariable um 1. Damit wird in der alten Typeliste das nächste Element ausgewählt,
    #damit alles synchron zur Schleife hier abläuft, die ja über die Knotenliste läuft (sonst würde immer der
    #Type-Eintrag des ersten Elements benutzt werden, also immer nur "type: work").
    index += 1
    #Die Schleife läuft solange weiter, bis alle Knoten in der Knotenliste abgearbeitet wurden.
    
#Das ganze wiederholen wir wieder für die Knotenliste von Rated M For Manly.
index = 0
for element in knotenliste_rmfm:
    dict_element = typeliste_rmfm[index]
    if element in matchliste_tropes_c_rmfm:
        dict_element.update({"comedy": "ja"})
        typeliste_rmfm_neu.extend([dict_element])
    else:
        dict_element.update({"comedy": "nein"})
        typeliste_rmfm_neu.extend([dict_element])
    if element in matchliste_genre:
        dict_element.update({"genre": "beide"})
    else:
        dict_element.update({"genre": "Rated M For Manly"})
    typeliste_rmfm_neu.extend([dict_element])
    index += 1

#Jetzt können wir die alten Knotenlisten mit den neuen Typelisten zusammenführen. Damit haben wir im Gephi-Datenlabor
#neben der Spalte "type" zwei weitere Spalten, "comedy" und "genre".
knoten_cf = list(zip(knotenliste_cf, typeliste_cf_neu))
knoten_rmfm = list(zip(knotenliste_rmfm, typeliste_rmfm_neu))

#Nun haben wir die gleichen Listen wie auf dem Server.

##### LISTEN VERFEINERN #####

#Wir können einzelne Tropes aus den Listen werfen.
#Mit dieser Regular Expression wird der String in der URI spezifiziert, nach dem gesucht werden
#soll. ChickFlick ist kein Trope, taucht aber trotzdem als Trope in den Listen auf. Das wollen
#wir ändern.
regex_cf = re.compile(r'/Main/ChickFlick')
#Erst suchen wir in den Knoten und erstellen eine neue Liste mit allen Knoten, die den String
#"ChickFlick" nicht enthalten.
knotenliste_cf_gefiltert = [i for i in knotenliste_cf if not regex_cf.search(i)]
knoten_cf_gefiltert = [i for i in knoten_cf if not regex_cf.search(i[0])]
#Dann das gleiche mit der Kantenliste.
bipartite_kantenliste_cf_gefiltert = [i for i in bipartite_kantenliste_cf if not regex_cf.search(i[1])]
#Die alten Listen werden mit dem Inhalt der neuen gefilterten Listen ersetzt.
knoten_cf = knoten_cf_gefiltert
knotenliste_cf = knotenliste_cf_gefiltert
bipartite_kantenliste_cf = bipartite_kantenliste_cf_gefiltert

#Das ganze nochmal für Rated M For Manly
regex_rmfm = re.compile(r'/Main/RatedMForManly')
knotenliste_rmfm_gefiltert = [i for i in knotenliste_rmfm if not regex_rmfm.search(i)]
knoten_rmfm_gefiltert = [i for i in knoten_rmfm if not regex_rmfm.search(i[0])]
bipartite_kantenliste_rmfm_gefiltert = [i for i in bipartite_kantenliste_rmfm if not regex_rmfm.search(i[1])]
knoten_rmfm = knoten_rmfm_gefiltert
knotenliste_rmfm = knotenliste_rmfm_gefiltert
bipartite_kantenliste_rmfm = bipartite_kantenliste_rmfm_gefiltert

###### NETZWERK ERSTELLEN: Werke & Tropes als Knoten ######

#Hier wird ein leerer Graph angelegt, in den erst die Knoten aus der zusammengelegten
#Knotenliste (Variable "knoten") und dann die Kanten aus der bipartiten Kantenliste eingefügt werden
trope_network_cf = nx.Graph()
trope_network_cf.add_nodes_from(knoten_cf)
trope_network_cf.add_edges_from(bipartite_kantenliste_cf)

#Datei wird in Gephi-Format exportiert; Gebt hier einen Pfad auf eurem PC an.
nx.write_gexf(trope_network_cf, "C:\\Users\\BlackEmperor\\Desktop\\Projektarbeit\\trope_network_cf.gexf")

#Der Einfachheit halber hier nochmal für Rated M For Manly:
trope_network_rmfm = nx.Graph()
trope_network_rmfm.add_nodes_from(knoten_rmfm)
trope_network_rmfm.add_edges_from(bipartite_kantenliste_rmfm)
nx.write_gexf(trope_network_rmfm, "C:\\Users\\BlackEmperor\\Desktop\\Projektarbeit\\trope_network_rmfm.gexf")

##### TROPES ALS KNOTEN, WERKE ALS KANTEN #####
from networkx.algorithms import bipartite

#Hier wird der Inhalt aus der zusammengeführten Knotenliste in Werkknoten und Tropeknoten
#aufgespalten.
trope_nodes_cf = [k for k, v in dict(knoten_cf).items() if v["type"] ==  "trope" ]
work_nodes_cf = [k for k, v in dict(knoten_cf).items() if v["type"] == "work" ]

#Hier wird das Netzwerk erstellt.
trope_network_tropes_only_cf = bipartite.projected_graph(trope_network_cf, trope_nodes_cf, multigraph=False)

#Gewichteten Graf erstellen (Kanten (Werke) mit vielen Verbindungen haben ein höheres Gewicht)
trope_network_tropes_only_cf_gewichtet = bipartite.weighted_projected_graph(trope_network_cf, trope_nodes_cf)

#Export (ACHTUNG: Sehr viele Kanten)
nx.write_gexf(trope_network_tropes_only_cf, "C:\\Users\\BlackEmperor\\Desktop\\Projektarbeit\\trope_network_tropes_only_cf.gexf")
nx.write_gexf(trope_network_tropes_only_cf_gewichtet, "C:\\Users\\BlackEmperor\\Desktop\\Projektarbeit\\trope_network_tropes_only_cf_gewichtet.gexf")

#Und nochmal für Rated M For Manly.
trope_nodes_rmfm = [k for k, v in dict(knoten_rmfm).items() if v["type"] ==  "trope" ]
work_nodes_rmfm = [k for k, v in dict(knoten_rmfm).items() if v["type"] == "work" ]
trope_network_tropes_only_rmfm = bipartite.projected_graph(trope_network_rmfm, trope_nodes_rmfm, multigraph=False)
nx.write_gexf(trope_network_tropes_only_rmfm, "C:\\Users\\BlackEmperor\\Desktop\\Projektarbeit\\trope_network_tropes_only_rmfm.gexf")

#Gewichteter Graph
trope_network_tropes_only_rmfm_gewichtet = bipartite.weighted_projected_graph(trope_network_rmfm, trope_nodes_rmfm)
nx.write_gexf(trope_network_tropes_only_rmfm_gewichtet, "C:\\Users\\BlackEmperor\\Desktop\\Projektarbeit\\trope_network_tropes_only_rmfm_gewichtet_gewichtet.gexf")

######~~ NETZWERKANALYSE MIT PYTHON ~~######

#Anzahl der Elemente in der Comedytrope-ChickFlick Matchliste.
len(matchliste_tropes_c_cf)
#Anzahl der Elemente in der Comedytrope-Rated M For Manly Matchliste.
len(matchliste_tropes_c_rmfm)
#Anzahl der Elemente in der Genre-Matchliste.
len(matchliste_genre)
#Anzahl der Elemente in der Tropeliste.
len(tropeliste)

#Anzahl der Werke in der Knotenliste:
regex = re.compile(r'/Film/')
werkknotenliste_cf = list(filter(regex.search, knotenliste_cf))
len(werkknotenliste_cf)
regex = re.compile(r'/Film/')
werkknotenliste_rmfm = list(filter(regex.search, knotenliste_rmfm))
len(werkknotenliste_rmfm)
#Anzahl der Tropes in der Knotenliste (am besten vorher filtern, siehe oben (LISTEN VERFEINERN):
regex = re.compile(r'/Main/')
tropeknotenliste_cf = list(filter(regex.search, knotenliste_cf))
len(tropeknotenliste_cf)
regex = re.compile(r'/Main/')
tropeknotenliste_rmfm = list(filter(regex.search, knotenliste_rmfm))
len(tropeknotenliste_rmfm)

#Grad der einzelnen Knoten im Netzwerk berechnen. Leider nicht sehr übersichtlich; lieber
#Gephi dafür verwenden, wenn man eine Übersicht haben möchte.
grade_cf = trope_network_cf.degree()

##### KLEINERE NETZWERKE ERSTELLEN #####
#Mit den berechneten Graden können wir in Python neue Listen erstellen, aus denen wir ein
#kompakteres Netzwerk bekommen.

#1) Liste mit allen Elementen erstellen, deren Grad größer ist als x. Nützlich, um zum Beispiel
#"unwichtigere" Tropes auszuschließen. Als Standardwert habe ich mal 2 ausgewählt, könnt ihr
#aber auch ändern.
gradliste = list(grade_cf)
gefilterte_gradliste = []
for i in gradliste:
    if i[1] > 2:
        gefilterte_gradliste.append(i[0])
#2) Neue Werkliste erstellen:
regex = re.compile(r'/Film/')
knotenliste_neu = list(filter(regex.search, gefilterte_gradliste))
typeliste_neu = []
for i in knotenliste_neu:
    typeliste_neu.extend([{"type": "work"}])
#3) Neue Tropeliste erstellen:
regex = re.compile(r'/Main/')
tropeliste_neu = list(filter(regex.search, gefilterte_gradliste))
for i in tropeliste_neu:
    knotenliste_neu.extend([i])
    typeliste_neu.extend([{"type": "trope"}])
#4) Neue Knoten - und Typelisten zusammenführen:
knoten_neu = list(zip(knotenliste_neu, typeliste_neu))
#5) Neue Kantenliste erstellen:
bipartite_kantenliste_neu = []
#Wenn das Trope im aktuellen Tuple-Element in der neuen Knotenliste auftaucht, wird das Tuple
#in die neue Kantenliste geschrieben.
bipartite_kantenliste_neu = [i for i in bipartite_kantenliste_cf if i[1] in knotenliste_neu and i[0] in knotenliste_neu]
        
#6) Neues Netzwerk erstellen:
trope_network_neu = nx.Graph()
trope_network_neu.add_nodes_from(knoten_neu)
trope_network_neu.add_edges_from(bipartite_kantenliste_neu)
#7) Neues Netzwerk für Gephi ausgeben (optional):
nx.write_gexf(trope_network_neu, "C:\\Users\\BlackEmperor\\Desktop\\Projektarbeit\\trope_network_neu.gexf")

##### HISTOGRAMME ERSTELLEN #####

#Hier könnt ihr Histogramme zeichnen lassen. Wenn ihr das verkleinerte Netzwerk verwenden wollt, löscht das "#"
#vor der jeweils zweiten "plt.hist(....)" Zeile raus und fügt es vor die erste Zeile ein, damit das richtige
#Netzwerk ausgewählt ist.

#Histogramm für Betweenness Centrality
plt.hist(list(nx.betweenness_centrality(trope_network_cf).values()), bins=100)
#plt.hist(list(nx.betweenness_centrality(trope_network_neu).values()), bins=100)
plt.ylabel("Häufigkeit")
plt.xlabel("Betweenness Centrality")
plt.show()

#Histogramm für Degree Centrality
plt.hist(list(nx.degree_centrality(trope_network_cf).values()), bins=100)
#plt.hist(list(nx.degree_centrality(trope_network_neu).values()), bins=100)
plt.ylabel("Häufigkeit")
plt.xlabel("Degree Centrality")
plt.show()

#Histogramm für Closeness Centrality
plt.hist(list(nx.closeness_centrality(trope_network_cf).values()), bins=100)
#plt.hist(list(nx.closeness_centrality(trope_network_neu).values()), bins=100)
plt.ylabel("Häufigkeit")
plt.xlabel("Closeness Centrality")
plt.show()

#Histogramm für Eigenvector Centrality
plt.hist(list(nx.eigenvector_centrality(trope_network_cf).values()), bins=100)
#plt.hist(list(nx.eigenvector_centrality(trope_network_neu).values()), bins=100)
plt.ylabel("Häufigkeit")
plt.xlabel("Eigenvector Centrality")
plt.show()

##### SUBGRAPHEN #####
from networkx.algorithms import community
communities_chickflick = community.girvan_newman(trope_network_cf)
communities_chickflick = next(communities_chickflick)
communities_chickflick_list = [list(comm) for comm in communities_chickflick]