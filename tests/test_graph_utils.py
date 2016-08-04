from unittest import TestCase

from vstore.graph_utils import VIVOUtilsGraph, DEFAULT_GRAPH
from rdflib import Graph, URIRef, Dataset, Namespace

SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")


sample = """
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix vivo: <http://vivoweb.org/ontology/core#> .

<http://vivo.school.edu/individual/fac1089> a vivo:FacultyMember ;
    rdfs:label "Payne, Ladonna" .

<http://vivo.school.edu/individual/fac1307> a vivo:FacultyMember ;
    rdfs:label "Pate, Andrea" .

<http://vivo.school.edu/individual/fac1538> a vivo:FacultyMember ;
    rdfs:label "Moises, Edgar Estes" .

<http://vivo.school.edu/individual/fac1567> a vivo:FacultyMember ;
    rdfs:label "Banks, Shannon" .

<http://vivo.school.edu/individual/fac1625> a vivo:FacultyMember ;
    rdfs:label "Hawkins, Callie" .

<http://vivo.school.edu/individual/fac1699> a vivo:FacultyMember ;
    rdfs:label "Stanton, Kathie" .
"""

sample2 = """
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix vivo: <http://vivoweb.org/ontology/core#> .

<http://vivo.school.edu/individual/fac1625> a vivo:FacultyMember ;
    rdfs:label "Hawkins, Callie" .

<http://vivo.school.edu/individual/fac1699> a vivo:FacultyMember ;
    rdfs:label "Stanton, Kathie" .
"""

sample3 = """
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .

<http://vivo.school.edu/individual/topic1> a skos:Concept ;
    rdfs:label "Baseball" .

<http://vivo.school.edu/individual/topic2> a skos:Concept ;
    rdfs:label "Baseball" ;
    skos:altLabel "Hardball" .

<http://vivo.school.edu/individual/sports> skos:narrower <http://vivo.school.edu/individual/topic2> .
"""


class TestBulkUpdate(TestCase):
    g = Graph().parse(data=sample, format="turtle")

    def test_yielder(self):
        """
        Test yielder returns proper number of triple sets.
        """
        g = Graph().parse(data=sample, format="turtle")
        bu = VIVOUtilsGraph()
        chunks = 0
        for num, nt in bu.nt_yielder(g, 4):
            chunks += 1
        self.assertEqual(chunks, 3)

        chunks = 0
        for _, _ in bu.nt_yielder(g, 20):
            chunks += 1
        self.assertEqual(chunks, 1)

    def test_bulk_add(self):
        g = Graph().parse(data=sample, format="turtle")
        named_graph = URIRef("http://localhost/test/data")
        bu = VIVOUtilsGraph()
        added = bu.bulk_add(named_graph, g, size=4)
        self.assertEqual(added, 12)

    def test_bulk_remove(self):
        named_graph = URIRef("http://localhost/test/data")
        bu = VIVOUtilsGraph()
        added = bu.bulk_add(named_graph, self.g, size=4)
        # Remove 4 triples.
        rg = Graph().parse(data=sample2, format="turtle")
        removed = bu.bulk_remove(named_graph, rg, size=2)
        self.assertEqual(removed, 4)
        # Total triples left should be 8
        self.assertEqual(len(bu), 8)

    def test_merge(self):
        # Load test data into named graph
        related = URIRef("http://vivo.school.edu/individual/sports")
        uri1 = URIRef("http://vivo.school.edu/individual/topic1")
        uri2 = URIRef("http://vivo.school.edu/individual/topic2")
        my_vstore = VIVOUtilsGraph()
        named_graph = URIRef("http://localhost/test/data")
        g = Graph()
        g.parse(data=sample3, format="turtle")
        my_vstore.bulk_add(named_graph, g)
        add, remove = my_vstore.merge_uris(uri1, uri2, named_graph)

        # make sure statements have been moved to new uri
        self.assertTrue(related in [u for u in add.subjects(predicate=SKOS.narrower, object=uri1)])
        self.assertEqual(u"Hardball", add.value(subject=uri1, predicate=SKOS.altLabel).toPython())

        # make sure statements are retracted
        self.assertTrue(related in [u for u in remove.subjects(predicate=SKOS.narrower, object=uri2)])
        self.assertEqual(u"Hardball", remove.value(subject=uri2, predicate=SKOS.altLabel).toPython())

        # do the update
        rm_stmts = my_vstore.bulk_remove(named_graph, remove)
        add_stmts = my_vstore.bulk_add(named_graph, add)

        # test merge sizes
        self.assertEqual(rm_stmts, 4)
        self.assertEqual(add_stmts, 4)
        self.assertEqual(rm_stmts, add_stmts)

        # retrieve a merged statement from store
        self.assertEqual(u"Hardball", my_vstore.value(subject=uri1, predicate=SKOS.altLabel).toPython())
        self.assertEqual(None, my_vstore.value(subject=uri2, predicate=SKOS.altLabel))
