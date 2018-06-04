# -*- coding: utf-8 -*-
"""
Created on Sat May 19 13:01:58 2018

@author: BlackEmperor
"""

import rdflib
import re

dbtropes_rdf = rdflib.Graph()
dbtropes_rdf.parse("/home/heckelenme/tvtropes_projektseminar/dbtropes_snapshot.nt", format = "nt")

#Anlegen leerer Listen
featureliste = []
werkliste = []
filter_werkliste = []
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

#Test zum Anzeigen der gefilterten Werkliste.
print(filter_werkliste)

#Jetzt haben wir zumindest mal eine Liste von Filmen aus dem "Rated M for Manly" Genre.


#BEISPIELCODE FÜR TROPES VON HERR HECKELEN - FUNKTIONIERT EVENTUELL NOCH NICHT
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
    knotenliste.extend([str(filterwerk)])
    typeliste.extend({"type": "work"})
    for trope in query_output:
        bipartite_kantenliste.append((str(filterwerk), str(trope[0])))
        knotenliste.extend([str(trope[0])])
        typeliste.extend([{"type": "trope"}])