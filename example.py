"""
Example of using the RDFLib store API with the VIVO
SPARQL endpoint.
"""
import os

from rdflib import Graph, URIRef, RDF, Literal
from rdflib.graph import Resource
from rdflib.namespace import SKOS, RDFS

from vstore import VIVOUpdateStore, VIVOStore

VIVO_EMAIL = os.environ['VIVO_EMAIL']
VIVO_PASSWORD = os.environ['VIVO_PASSWORD']
VIVO_BASE = os.environ['VIVO_BASE']

# Define the VIVO store
query_endpoint = VIVO_BASE + '/api/sparqlQuery'
update_endpoint = VIVO_BASE + '/api/sparqlUpdate'

# Setup the VIVO store
store = VIVOUpdateStore(VIVO_EMAIL, VIVO_PASSWORD)
store.open((query_endpoint, update_endpoint))

# Identify a named graph where we will be adding our instances.
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


# Add the data using the RDFLib API
named_graph += g

# List all concepts in the named graph.
for subj in named_graph.subjects(predicate=RDF.type, object=SKOS.Concept):
    print 'Concept: ', subj

# Remove the graph
named_graph -= g

# Attempt to retrieve a deleted URI
baseball_uri = URIRef('http://example.org/n1234')
assert named_graph.value(subject=baseball_uri) == None

# Re-add the concept using the RDFLib API rather than SPARQL
bball = Resource(named_graph, baseball_uri)
bball.set(RDF.type, SKOS.Concept)
bball.set(RDFS.label, Literal("Baseball"))

# Fetch the label for the resource from the VIVO store using the RDFLib API.
assert named_graph.value(subject=baseball_uri, predicate=RDFS.label).toPython() == u"Baseball"

# Remove
named_graph.remove((baseball_uri, RDFS.label, Literal("Baseball")))
named_graph.remove((baseball_uri, RDF.type, SKOS.Concept))

assert named_graph.value(subject=baseball_uri) == None
