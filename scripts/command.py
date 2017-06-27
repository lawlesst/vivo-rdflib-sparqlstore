
import os

import click

# Default VIVO graph
from rdflib import URIRef, Graph
from rdflib.util import guess_format
from vstore import VIVOUpdateStore

KB2 = URIRef("http://vitro.mannlib.cornell.edu/default/vitro-kb-2")


def console(msg):
    click.echo(msg, err=True)


def do_update(email, password, base, graph, named_graph, action):
    # Define the VIVO store
    query_endpoint = base.rstrip('/') + '/api/sparqlQuery'
    update_endpoint = base.rstrip('/') + '/api/sparqlUpdate'

    # Setup the VIVO store
    store = VIVOUpdateStore(email, password)
    store.open((query_endpoint, update_endpoint))

    if action == "add":
        added = store.bulk_add(named_graph, graph)
        console("{} triples added to {}.".format(added, named_graph.n3()))
    else:
        removed = store.bulk_remove(named_graph, graph)
        console("{} triples removed from {}.".format(removed, named_graph.n3()))


@click.command(help="Pass in the file to add or remove and the action 'add' or 'remove'.")
@click.argument('triple_file')
@click.argument('action', required=True, type=click.Choice(["add", "remove"]))
@click.option('--email', required=True, default=lambda: os.environ.get('VIVO_EMAIL', None))
@click.option('--password', required=True, default=lambda: os.environ.get('VIVO_PASSWORD', None))
@click.option('--url', required=True, default=lambda: os.environ.get('VIVO_URL', None))
@click.option('--named_graph', default=KB2)
def process(triple_file, action, email, password, url, named_graph):
    console("\n{}\n".format('-' * 25))
    console("VIVO url: {}".format(url))

    # Handle named graph
    if named_graph != KB2:
        named_graph = URIRef(named_graph)

    fmt = guess_format(triple_file)
    graph = Graph()
    graph.parse(source=triple_file, format=fmt)

    console("Read {} triples and will {} to <{}>".format(len(graph), action, named_graph))
    # Do the update.
    do_update(email, password, url, graph, named_graph, action)
    # Finish
    console("\n{}\n".format('-' * 25))


if __name__ == '__main__':
    process()
