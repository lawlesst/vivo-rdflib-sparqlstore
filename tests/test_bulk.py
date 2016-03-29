from unittest import TestCase

from vstore.bulk import BulkUpdateGraph
from rdflib import Graph, URIRef


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


class TestBulkUpdate(TestCase):

    g = Graph().parse(data=sample, format="turtle")

    def test_yielder(self):
        """
        Test yielder returns proper number of triple sets.
        """
        g = Graph().parse(data=sample, format="turtle")
        bu = BulkUpdateGraph()
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
        bu = BulkUpdateGraph()
        added = bu.bulk_add(named_graph, g, size=4)
        self.assertEqual(added, 12)

    def test_bulk_remove(self):
        named_graph = URIRef("http://localhost/test/data")
        bu = BulkUpdateGraph()
        added = bu.bulk_add(named_graph, self.g, size=4)
        # Remove 4 triples.
        rg = Graph().parse(data=sample2, format="turtle")
        removed = bu.bulk_remove(named_graph, rg, size=2)
        self.assertEqual(removed, 4)
        # Total triples left should be 8
        self.assertEqual(len(bu), 8)

