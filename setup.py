from setuptools import setup

description = 'RDFLib SPARQLStore and SPARQLUpdateStore implementation for VIVO.'

setup(
    name = 'rdflib-vivo-sparqlstore',
    version = '0.0.1',
    url = 'https://github.com/lawlesst/rdflib-vivo-sparqlstore',
    author = 'Ted Lawless',
    author_email = 'lawlesst@gmail.com',
    py_modules = ['vstore',],
    scripts = ['vstore.py'],
    description = description,
    install_requires=[
        'rdflib>=4.2',
    ],
)
