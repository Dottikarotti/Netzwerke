# -*- coding: utf-8 -*-
"""
Created on Sat May 19 13:01:58 2018

@author: BlackEmperor
"""

#Außer "re" müssen alle Module auf dem Server Terminal mit "pip install MODUL --user" installiert werden (z.B. pip3 install rdflib --user)
import rdflib
import networkx as nx
import re
import pandas as pd
import matplotlib.pyplot as plt

dbtropes_rdf = rdflib.Graph()
dbtropes_rdf.parse("/home/heckelenme/tvtropes_projektseminar/dbtropes_snapshot.nt", format = "nt")

#Anlegen leerer Listen
featureliste = []
werkliste = []
filter_werkliste = []
comedytrope_liste = []
bipartite_kantenliste = []
knotenliste = []
typeliste = []

#1. Query: "Features"
#ERKLÄRUNG:
#Das Ergebnis des Queries wird in eine Variable "query_output" geschrieben.
#Die """ am Anfang und Ende braucht das rdf-Modul; wir schreiben eine Art "Query-Text", den das
#Modul in einen richtigen Query umwandelt.
#Wir SELECTen eine Variable "feature".
#Was ist "feature"? "feature" ist jedes Element, das einen "type" mit dem Namen "Rated M for Manly"
#besitzt. Wollen wir ein anderes Genre, müssen wir "RatedMForManly" im RDF-"Objekt" (Erinnerung:
#Subject-Prädikat-OBJEKT) durch ein anderes Genre ersetzen.
query_output = dbtropes_rdf.query(
        """
        SELECT ?feature
        WHERE {
                ?feature <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbtropes.org/resource/Main/RatedMForManly>
            }
        """
    )

#Hier wird der Query ausgeführt. Jedes "feature" Element wird in eine Liste "featureliste" geschrieben.
for row in query_output:
    featureliste.extend(row)

#Test zum Anzeigen der Featureliste.
print(featureliste)

#2. Query: Werke
#Wir führen den Query in einer for-Schleife aus, und zwar für jedes Element in unserer Featureliste.
#Wir SELECTen eine Variable "work". Diese Variable ist jedes "Subjekt", das ein "Prädikat" "hasFeature"
#besitzt, das als "Objekt" den String des Features in der Liste hat, für das der Query ausgeführt wird.
#Da der String in einer Python-Variable "feature" gespeichert ist, wird der "Query-Text" nach dem < mit
#den """ unterbrochen, der String wird mit nach dem ersten + eingefügt und nach dem zweiten + geht der
#Query-Text weiter.
for feature in featureliste:
    query_output = dbtropes_rdf.query(
        """
        SELECT ?work
        WHERE {
            ?work <http://skipforward.net/skipforward/resource/seeder/skipinions/hasFeature> <""" + str(feature) +"""> .
        }
        """
    )
#Hier wird der Query wieder ausgeführt. Jedes Werk wird in eine Werkliste geschrieben. Dieser Schritt
#ist wegen der Übereck-Feature-Verbindung der Werke mit dem "Genre-Trope" notwendig.
    for work in query_output:
        werkliste.extend(work)

#Test zum Anzeigen der Werkliste.
print(werkliste)

#Wir nutzen eine Regular Expression, um nach Filmen zu filtern.
regex = re.compile(r'/Film/')

#In die Variable "filter_werkliste" wird eine Liste geschrieben, in der die Filme mithilfe der
#Regular Expression aus der ursprünglichen Werkliste durch den regex.search Befehl gefiltert wurden.
filter_werkliste = list(filter(regex.search, werkliste))
#Dann erstellen wir eine Typliste, wo der Knotentyp (in diesem Fall "work") für jedes Werk abgelegt
#wird. Die werden später für die Attribute des jeweiligen Knoten gebraucht.
for filterwerk in filter_werkliste:
    typeliste.extend([{"type": "work"}])
    
#Test zum Anzeigen der gefilterten Werkliste.
print(filter_werkliste)

#Jetzt haben wir zumindest mal eine Liste von Filmen aus dem "Rated M for Manly" Genre.

#3. Query: Tropes der Filme
#Der Query läuft per for-Schleife über die gefilterte Werkliste.
#Hier wird wieder eine Variable "trope" definiert. Hier wird die "Auflösung" der komplizierten
#Feature-Verbindung komplett in den Query gepackt. Heißt:
#"String des Films" - hasFeature - beliebige FeatureID
#beliebige FeatureID - type - beliebiges Trope
#Dieses beliebige Trope brauchen wir. Das ganze wird pro Werk so oft gemacht, wie das Werk Tropes
#besitzt.
for filterwerk in filter_werkliste:
    query_output = dbtropes_rdf.query(
        """
        SELECT ?trope
        WHERE {
            <""" + str(filterwerk) + """> <http://skipforward.net/skipforward/resource/seeder/skipinions/hasFeature> ?feature .
            ?feature <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> ?trope
            }
        """
    )
#Zuerst packen wir die Strings der gefilterten Werke (ohne diesen rdf URI Rotz vor der URI) in eine Liste.
    knotenliste.extend([str(filterwerk)])
#Hier wird der Query dann erst wirklich ausgeführt. Für jedes gefundene Trope wird ein Tuple Eintrag
#in der bipartiten Kantenliste angelegt, dann werden die einzelnen Tropes der Knotenliste hinzugefügt
#und zu guter Letzt wird die Typliste mit dem Knotentyp "Trope" für jedes Trope erweitert.
    for trope in query_output:
        bipartite_kantenliste.append((str(filterwerk), str(trope[0])))
        knotenliste.extend([str(trope[0])])
        typeliste.extend([{"type": "trope"}])
    
#Hier kann man sich die einzelnen Listen anzeigen lassen.
print(knotenliste)
print(typeliste)
print(bipartite_kantenliste)

##### TROPE LISTEN ERSTELLEN #####
#4. Query: Comedy Tropes
#Der Query holt alle Tropes aus dem Datensatz, die über "processingCategory2" mit der ComedyTropes
#Ressource verbunden sind (sprich, alle Comedy Tropes).
query_output = dbtropes_rdf.query(
        """
        SELECT ?trope
        WHERE {
            ?trope <http://dbtropes.org/ont/processingCategory2> <http://dbtropes.org/resource/Main/ComedyTropes>
        }
        """
    )

#Ausführung und Füllen der Liste.
for row in query_output:
    comedytrope_liste.extend(row)

#Test zum Anzeigen der Comedy Trope Liste.
print(comedytrope_liste)

##### LISTEN IN NETZWERKFORM BRINGEN #####
##### ACHTUNG! WORK IN PROGRESS #####
#Typliste und Knotenliste werden zusammengeführt. Jedes Element in der Liste wird nun zu
#einem Tupel, (Werk/Trope, type: work/trope).
knoten = list(zip(knotenliste, typeliste))

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

#Datei wird in Gephi-Format exportiert; Usernamen im Pfad durch euren ersetzen
nx.write_gexf(trope_network, "/home/schwarzersn/trope_network.gexf")

#Diese Datei sollte man per scp (pscp) Befehl vom Server runterladen können. Den genauen
#Befehl weiß ich noch nicht.

#Nutzlosen roten Farbkleks malen. Dauert lange.
nx.draw(trope_network)