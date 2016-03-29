from setuptools import setup

description = 'RDFLib SPARQLStore and SPARQLUpdateStore implementation for VIVO.'

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name = 'vivo-rdflib-sparqlstore',
    version = '0.0.1',
    url = 'https://github.com/lawlesst/rdflib-vivo-sparqlstore',
    author = 'Ted Lawless',
    author_email = 'lawlesst@gmail.com',
    py_modules = ['vstore', 'vivoUpdate'],
    scripts = ['vstore.py'],
    description = description,
    install_requires=required,
    entry_points='''
        [console_scripts]
        vivoUpdate=vivoUpdate:process
    '''
)

