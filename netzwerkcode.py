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

#Gebt hier jeweils den Pfad und Namen der Knoten bzw. Kantendatei an, die ihr aus der .zip
#von GitHub entpackt habt.
#Wichtig ist nur, dass ihr wirklich immer "\\" benutzt, zum Escapen des "\" Symbols im Pfad.
#Außerdem solltet ihr immer nur ein Genre gleichzeitig bearbeiten (also eine _knoten und eine
#_kanten Datei reinladen).
df1 = pd.read_pickle("C:\\Users\\BlackEmperor\\Desktop\\Projektarbeit\\chickflick_knoten")
df2 = pd.read_pickle("C:\\Users\\BlackEmperor\\Desktop\\Projektarbeit\\chickflick_kanten")

#Hier könnt ihr Tropelisten importieren.
df3 = pd.read_pickle("C:\\Users\\BlackEmperor\\Desktop\\Projektarbeit\\comedytropes")

#Hier werden die einzelnen Werte aus den DataFrames in Listen gepackt.
knotenliste = df1[0].values.tolist()
typeliste = df1[1].values.tolist()
bipartite_kantenliste = df2.values.tolist()
tropeliste = df3[0].values.tolist()

#Der Inhalt der Kantenliste wurde beim Export in das DataFrame von Tupeln in Listen umgewandelt.
#Diese Zeile macht das im Prinzip wieder rückgängig.
bipartite_kantenliste = list(tuple(x) for x in bipartite_kantenliste)

#Knotenliste und Typeliste werden wieder zusammengefügt.
knoten = list(zip(knotenliste, typeliste))

#Nun haben wir die gleichen Listen wie auf dem Server.

#Hier wird ein leerer Graph angelegt, in den erst die Knoten aus der zusammengelegten
#Knotenliste (Variable "knoten") und dann die Kanten aus der bipartiten Kantenliste eingefügt werden
trope_network = nx.Graph()
trope_network.add_nodes_from(knoten)
trope_network.add_edges_from(bipartite_kantenliste)

#Hier wird irgendwas namens "bipartite" importiert. Braucht man wohl für den nachfolgenden Code.
from networkx.algorithms import bipartite

#Hier wird der Inhalt aus der zusammengeführten Knotenliste in Werkknoten und Tropeknoten
#aufgespalten. Dafür haben wir zuvor die Typliste gebraucht.
trope_nodes = [k for k, v in dict(knoten).items() if v["type"] ==  "trope" ]
work_nodes = [k for k, v in dict(knoten).items() if v["type"] == "work" ]

#Hier scheint ein Netzwerk erstellt zu werden, in dem nur Tropes vorkommen. Wofür das ganze ist,
#weiß ich nicht. Wenn man das Netzwerk mit Gephi öffnet, kann man damit nicht so viel anfangen,
#da irgendwie jedes Trope miteinander verbunden ist.
trope_network_tropes_only = bipartite.projected_graph(trope_network, trope_nodes, multigraph=False)

#Datei wird in Gephi-Format exportiert; Gebt hier einen Pfad auf eurem PC an.
nx.write_gexf(trope_network, "C:\\Users\\BlackEmperor\\Desktop\\Projektarbeit\\trope_network.gexf")
#Diese Zeile exportiert das Trope-Netzwerk. Momentan auskommentiert, siehe oben (trope_network_tropes_only)
#nx.write_gexf(trope_network_tropes_only, "C:\\Users\\BlackEmperor\\Desktop\\Projektarbeit\\trope_network_tropes_only.gexf")

###### NETZWERKANALYSE MIT PYTHON ######

#Leider besitzen alle Listen viele Duplikate von Tropes. Bei der Erstellung des Netzwerks werden
#diese Duplikate automatisch entfernt, aber sie bleiben in den Python Listen. Mit diesen Befehlen
#kann man neue Listen erstellen, in denen die Duplikate entfernt wurden. Diese kann man dann
#eher für quantitative Analysen verwenden.
knotenliste_nwa = list(set(knotenliste))
bipartite_kantenliste_nwa = list(set(bipartite_kantenliste))

### Trope Vergleich ###
#Hier könnt ihr die Knotenliste mit einer der Tropelisten vergleichen.
#Beide Listen werden als "sets" gespeichert, dann wird nach Überschneidungen gesucht und die
#Ergebnisse in das Überschneidungsset gespeichert.
#Dann wird über dieses Set in einer for-Schleife iteriert und die Matches in eine Matchliste
#gepackt. Das Ergebnis sind alle Tropes, die in der Knoten - und Tropeliste auftauchen.
vergleichsliste1 = set(knotenliste_nwa)
vergleichsliste2 = set(tropeliste)
ueberschneidungsset = vergleichsliste1.intersection(vergleichsliste2)
matchliste_nwa  = []
for match in ueberschneidungsset:
    matchliste_nwa.append(match)

#Anzahl der Elemente in der Matchliste.
len(matchliste_nwa)
#Anzahl der Elemente in der Tropeliste.
len(tropeliste)

#Grad der einzelnen Knoten im Netzwerk berechnen. Leider nicht sehr übersichtlich; lieber
#Gephi dafür verwenden, wenn man eine Übersicht haben möchte.
grade = trope_network.degree()
print(grade)

#Anzahl der Werke in der Knotenliste:
regex = re.compile(r'/Film/')
werkknotenliste_nwa = list(filter(regex.search, knotenliste_nwa))
len(werkknotenliste_nwa)
#Anzahl der Tropes in der Knotenliste (WICHTIG: MOMENTAN "FEATURES", ES SIND ALSO NICHT NUR TROPES! FILTERN NÖTIG):
regex = re.compile(r'/Main/')
tropeknotenliste_nwa = list(filter(regex.search, knotenliste_nwa))
len(tropeknotenliste_nwa)

#Histogramm für Betweenness Centrality
plt.hist(list(nx.betweenness_centrality(trope_network).values()), bins=100)
plt.ylabel("Häufigkeit")
plt.xlabel("Betweenness Centrality")
plt.show()

#Histogramm für Degree Centrality
plt.hist(list(nx.degree_centrality(trope_network).values()), bins=100)
plt.ylabel("Häufigkeit")
plt.xlabel("Degree Centrality")
plt.show()

#Netzwerk zeichnen. Auskommentiert, da Python zum Erstellen von Netzwerkgrafiken scheiße ist.
#nx.draw(trope_network)