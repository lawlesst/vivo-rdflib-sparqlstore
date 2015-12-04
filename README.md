## vivo-rdflib-sparqlstore

A RDFLib [SPARQLStore implementation](http://rdflib.readthedocs.org/en/latest/apidocs/rdflib.plugins.stores.html#rdflib.plugins.stores.sparqlstore.SPARQLUpdateStore) for the [VIVO](http://vivoweb.org/) [SPARQL query](https://wiki.duraspace.org/display/VIVO/The+SPARQL+Query+API) and [update](https://wiki.duraspace.org/display/VIVO/The+SPARQL+Update+API) APIs.

The VIVO SPARQL APIs require a user email and password for authentication.

See [RDFLib's docs](http://rdflib.readthedocs.org/en/latest/apidocs/rdflib.plugins.stores.html?highlight=sparqlstore#module-rdflib.plugins.stores.sparqlstore) for detailed documentation on the SPARQLStore implementation.

## Install

```
pip install git+https://github.com/lawlesst/rdflib-vivo-sparqlstore.git
```


## Usage

See [example.py](./example.py) for example usage.

### basic usage
```
from vstore import VIVOUpdateStore, VIVOStore
from rdflib.namespace import SKOS, RDF
from rdflib.graph import Dataset

#Define the VIVO store
query_endpoint = 'http://localhost:8983/vivo/api/sparqlQuery'
update_endpoint = 'http://localhost:8983/vivo/api/sparqlUpdate'

#Setup the VIVO store
store = VIVOUpdateStore('vivo_root@school.edu', 'passwd')
store.open((query_endpoint, update_endpoint))

ds = Dataset(store=store)

#All skos:Concepts in the store.
for subj in ds.subjects(predicate=RDF.type, object=SKOS.Concept):
    print 'Concept: ', subj
```

With a default VIVO installation, several URIS for skos:Concepts should be included, e.g.:

```
Concept:  http://vivoweb.org/ontology/core#yearMonthPrecision
Concept:  http://vivoweb.org/ontology/core#yearPrecision
Concept:  http://vivoweb.org/ontology/core#yearMonthDayTimePrecision
Concept:  http://vivoweb.org/ontology/core#yearMonthDayPrecision
```
