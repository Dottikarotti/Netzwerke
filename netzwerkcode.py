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

#Gebt hier jeweils den Pfad und Namen der Knoten bzw. Kantendatei an, die ihr aus der .zip
#von GitHub entpackt habt.
#Wichtig ist nur, dass ihr wirklich immer "\\" benutzt, zum Escapen des "\" Symbols im Pfad.
#Außerdem solltet ihr immer nur ein Genre gleichzeitig bearbeiten (also eine _knoten und eine
#_kanten Datei reinladen).
df1 = pd.read_pickle("C:\\Users\\BlackEmperor\\Desktop\\Projektarbeit\\ratedmformanly_knoten")
df2 = pd.read_pickle("C:\\Users\\BlackEmperor\\Desktop\\Projektarbeit\\ratedmformanly_kanten")

#Hier könnt ihr Tropelisten importieren.
df3 = pd.read_pickle("C:\\Users\\BlackEmperor\\Desktop\\Projektarbeit\\comedytropes")

#Hier werden die einzelnen Werte aus den DataFrames in Listen gepackt.
knotenliste = df1[0].values.tolist()
typeliste = df1[1].values.tolist()
bipartite_kantenliste = df2.values.tolist()
tropeliste = df3.values.tolist()

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

#???
trope_network_tropes_only = bipartite.projected_graph(trope_network, trope_nodes, multigraph=False)

#Datei wird in Gephi-Format exportiert; Gebt hier einen Pfad auf eurem PC an.
nx.write_gexf(trope_network, "C:\\Users\\BlackEmperor\\Desktop\\Projektarbeit\\trope_network.gexf")