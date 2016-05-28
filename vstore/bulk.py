from itertools import islice

from rdflib import ConjunctiveGraph, URIRef, Graph

import logging
logger = logging.getLogger(__name__)

# Size of graphs to post by default.
DEFAULT_CHUNK_SIZE = 8000


class BulkUpdateGraph(ConjunctiveGraph):

    @staticmethod
    def make_batch(size, graph):
        """
        Split graphs into n sized chunks.
        See: http://stackoverflow.com/a/1915307/758157
        
        :param size: int
        :param graph: graph
        :return: graph
        """
        i = iter(graph)
        chunk = list(islice(i, size))
        while chunk:
            yield chunk
            chunk = list(islice(i, size))

    def nt_yielder(self, graph, size):
        """
        Yield n sized ntriples for a given graph.
        Used in sending chunks of data to the VIVO
        SPARQL API.
        """
        for grp in self.make_batch(size, graph):
            tmpg = Graph()
            # Add statements as list to tmp graph
            tmpg += grp
            yield (len(tmpg), tmpg.serialize(format='nt'))

    def bulk_update(self, named_graph, graph, size, is_add=True):
        """
        Bulk adds or deletes. Triples are chunked into n size groups before
        sending to API. This prevents the API endpoint from timing out.
        """
        context = URIRef(named_graph)
        total = len(graph)
        if total > 0:
            for set_size, nt in self.nt_yielder(graph, size):
                if is_add is True:
                    logger.info("Adding {} statements to <{}>.".format(set_size, named_graph))
                    self.update(u'INSERT DATA { GRAPH %s { %s } }' % (context.n3(), nt))
                else:
                    logger.info("Removing {} statements from <{}>.".format(set_size, named_graph))
                    self.update(u'DELETE DATA { GRAPH %s { %s } }' % (context.n3(), nt))
        return total

    def bulk_add(self, named_graph, add, size=DEFAULT_CHUNK_SIZE):
        """
        Add batches of statements in n-sized chunks.
        """
        return self.bulk_update(named_graph, add, size)

    def bulk_remove(self, named_graph, add, size=DEFAULT_CHUNK_SIZE):
        """
        Remove batches of statements in n-sized chunks.
        """
        return self.bulk_update(named_graph, add, size, is_add=False)
