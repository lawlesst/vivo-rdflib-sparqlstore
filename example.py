"""
Example of using the RDFLib store API with the VIVO
SPARQL endpoint.
"""

from rdflib import Graph, URIRef, RDF
from rdflib.namespace import SKOS

from vstore import VIVOUpdateStore, VIVOStore

VIVO_EMAIL = 'user@school.edu'
VIVO_PASSWORD = 'xxx'

#Define the VIVO store
query_endpoint = 'http://localhost:8080/vivo/api/sparqlQuery'
update_endpoint = 'http://localhost:8080/vivo/api/sparqlUpdate'

#Setup the VIVO store
store = VIVOUpdateStore(VIVO_EMAIL, VIVO_PASSWORD)
store.open((query_endpoint, update_endpoint))

#Identify a named graph where we will be adding our instances.
default_graph = URIRef('http://example.org/vstore-test-graph')
named_graph = Graph(store, identifier=default_graph)

g = Graph()
g.parse(data=
"""
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<http://example.org/n1234> a skos:Concept ;
    skos:broader <http://example.org/n5678> ;
    rdfs:label "Baseball" .

<http://example.org/n5678> a skos:Concept ;
    rdfs:label "Sports" .

<http://example.org/n1000> a skos:Concept ;
    rdfs:label "Soccer" .
"""
, format="turtle")

print g.serialize(format='n3')

# Issue a SPARQL INSERT update query to add the assertions
# to VIVO.
named_graph.update(
    u'INSERT DATA { %s }' % g.serialize(format='nt')
)

#All concepts in the named graph.
for subj in named_graph.subjects(predicate=RDF.type, object=SKOS.Concept):
    print 'Concept: ', subj
