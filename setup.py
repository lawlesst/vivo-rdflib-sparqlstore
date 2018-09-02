from setuptools import setup, find_packages

description = 'RDFLib SPARQLStore and SPARQLUpdateStore implementation for VIVO.'

long_description = """
=======================
rdflib-vivo-sparqlstore
=======================

A `RDFLib SPARQLStore implementation <http://rdflib.readthedocs.org/en/latest/apidocs/rdflib.plugins.stores.html#rdflib.plugins.stores.sparqlstore.SPARQLUpdateStore>`_ for the
`VIVO <http://vivoweb.org/>`_ `SPARQL query and update <https://wiki.duraspace.org/display/VIVODOC110x/VIVO+APIs>`_ APIs.

This library supports Python 2.7 and 3.5+.

See `Github <https://github.com/lawlesst/rdflib-vivo-sparqlstore>`_ for more details.

"""

setup(
    name='vivo-rdflib-sparqlstore',
    version='0.4',
    url='https://github.com/lawlesst/rdflib-vivo-sparqlstore',
    author='Ted Lawless',
    author_email='lawlesst@gmail.com',
    long_description=long_description,
    python_requires='>=2.7',
    packages=find_packages(),
    install_requires=[
        'rdflib>=4.2',
        'SPARQLWrapper>=1.8',
        'click>=5.0'
    ],
    include_package_data=True,
    description=description,
    entry_points='''
        [console_scripts]
        vivoUpdate=scripts.command:process
    '''
)

