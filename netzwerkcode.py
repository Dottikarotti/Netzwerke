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

#Knotenliste und Typeliste werden wieder zusammengefügt.
knoten_cf = list(zip(knotenliste_cf, typeliste_cf))
knoten_rmfm = list(zip(knotenliste_rmfm, typeliste_rmfm))

#Nun haben wir die gleichen Listen wie auf dem Server.

##### LISTEN VERFEINERN #####

#Wir können einzelne Tropes aus den Listen werfen.
#Mit dieser Regular Expression wird der String in der URI spezifiziert, nach dem gesucht werden
#soll. ChickFlick ist kein Trope, taucht aber trotzdem als Trope in den Listen auf. Das wollen
#wir ändern.
regex_cf = re.compile(r'/Main/ChickFlick')
regex_rmfm = re.compile(r'/Main/RatedMForManly')
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
trope_network_rmfm = nx.Graph()
trope_network_rmfm.add_nodes_from(knoten_rmfm)
trope_network_rmfm.add_edges_from(bipartite_kantenliste_rmfm)

#Datei wird in Gephi-Format exportiert; Gebt hier einen Pfad auf eurem PC an.
nx.write_gexf(trope_network_cf, "C:\\Users\\BlackEmperor\\Desktop\\Projektarbeit\\trope_network_cf.gexf")
nx.write_gexf(trope_network_rmfm, "C:\\Users\\BlackEmperor\\Desktop\\Projektarbeit\\trope_network_rmfm.gexf")

##### Tropes als Knoten, Werke als Kanten #####
from networkx.algorithms import bipartite

#Hier wird der Inhalt aus der zusammengeführten Knotenliste in Werkknoten und Tropeknoten
#aufgespalten.
trope_nodes_cf = [k for k, v in dict(knoten_cf).items() if v["type"] ==  "trope" ]
work_nodes_cf = [k for k, v in dict(knoten_cf).items() if v["type"] == "work" ]
trope_nodes_rmfm = [k for k, v in dict(knoten_rmfm).items() if v["type"] ==  "trope" ]
work_nodes_rmfm = [k for k, v in dict(knoten_rmfm).items() if v["type"] == "work" ]

#Hier wird das Netzwerk erstellt.
trope_network_tropes_only_cf = bipartite.projected_graph(trope_network_cf, trope_nodes_cf, multigraph=False)
trope_network_tropes_only_rmfm = bipartite.projected_graph(trope_network_rmfm, trope_nodes_rmfm, multigraph=False)

#Export (ACHTUNG: Sehr viele Kanten)
nx.write_gexf(trope_network_tropes_only_cf, "C:\\Users\\BlackEmperor\\Desktop\\Projektarbeit\\trope_network_tropes_only_cf.gexf")
nx.write_gexf(trope_network_tropes_only_rmfm, "C:\\Users\\BlackEmperor\\Desktop\\Projektarbeit\\trope_network_tropes_only_rmfm.gexf")

######~~ NETZWERKANALYSE MIT PYTHON ~~######

##### TROPE VERGLEICH #####
#Hier könnt ihr die Knotenliste mit einer der Tropelisten vergleichen.
#Beide Listen werden als "sets" gespeichert, dann wird nach Überschneidungen gesucht und die
#Ergebnisse in das Überschneidungsset gespeichert.
#Dann wird über dieses Set in einer for-Schleife iteriert und die Matches in eine Matchliste
#gepackt. Das Ergebnis sind alle Tropes, die in der Knoten - und Tropeliste auftauchen.

#Ihr könnt als Vergleichslisten folgende Variablen verwenden: knotenliste_cf, knotenliste_rmfm, tropeliste.
#Einfach ersetzen.
vergleichsliste1 = set(knotenliste_cf)
vergleichsliste2 = set(tropeliste)
ueberschneidungsset = vergleichsliste1.intersection(vergleichsliste2)
matchliste  = []
for match in ueberschneidungsset:
    matchliste.append(match)

#Anzahl der Elemente in der Matchliste.
len(matchliste)
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
grade_rmfm = trope_network_rmfm.degree()

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

#Histogramm für Betweenness Centrality (trope_network oder trope_network_neu)
plt.hist(list(nx.betweenness_centrality(trope_network_cf).values()), bins=100)
plt.hist(list(nx.betweenness_centrality(trope_network_neu).values()), bins=100)
plt.ylabel("Häufigkeit")
plt.xlabel("Betweenness Centrality")
plt.show()

#Histogramm für Degree Centrality
plt.hist(list(nx.degree_centrality(trope_network_cf).values()), bins=100)
plt.hist(list(nx.degree_centrality(trope_network_neu).values()), bins=100)
plt.ylabel("Häufigkeit")
plt.xlabel("Degree Centrality")
plt.show()

#Histogramm für Closeness Centrality
plt.hist(list(nx.closeness_centrality(trope_network_cf).values()), bins=100)
plt.hist(list(nx.closeness_centrality(trope_network_neu).values()), bins=100)
plt.ylabel("Häufigkeit")
plt.xlabel("Closeness Centrality")
plt.show()

#Histogramm für Eigenvector Centrality
plt.hist(list(nx.eigenvector_centrality(trope_network_cf).values()), bins=100)
plt.hist(list(nx.eigenvector_centrality(trope_network_neu).values()), bins=100)
plt.ylabel("Häufigkeit")
plt.xlabel("Eigenvector Centrality")
plt.show()

#Netzwerk zeichnen. Auskommentiert, da Python zum Erstellen von Netzwerkgrafiken scheiße ist.
#nx.draw(trope_network)