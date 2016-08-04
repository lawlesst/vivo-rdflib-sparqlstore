"""
Extension to RDFLib SPARQLStore and SPARQLUpdateStore for use with VIVO/Vitro's built
in SPARQL query and update API. The VIVO implementation requires all SPARQL requests to
contain a "email" and "password" HTTP parameters to authenticate the request.
"""


from rdflib.plugins.stores.sparqlstore import (
    SPARQLStore,
    SPARQLUpdateStore,
    NSSPARQLWrapper,
)

from graph_utils import VIVOUtilsGraph

class VIVOWrapper(NSSPARQLWrapper):
    def setQuery(self, query):
        """
        Set the SPARQL query text and set the VIVO custom
        authentication parameters.

        Set here because this is called immediately before
        any query is sent to the triple store.
        """
        self.queryType = self._parseQueryType(query)
        self.queryString = self.injectPrefixes(query)
        self.addParameter('email', self.email)
        self.addParameter('password', self.password)


class VIVOStore(VIVOWrapper, SPARQLStore):
    def __init__(self, **kwargs):
        super(VIVOWrapper, self).__init__(**kwargs)
        super(SPARQLStore, self).__init__(**kwargs)


class VIVOUpdateStore(VIVOStore, SPARQLUpdateStore, VIVOUtilsGraph):
    def __init__(self, email, password, **kwargs):
        self.email = email
        self.password = password
        super(VIVOStore, self).__init__(**kwargs)
        super(SPARQLUpdateStore, self).__init__(**kwargs)
