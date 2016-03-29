from setuptools import setup, find_packages

description = 'RDFLib SPARQLStore and SPARQLUpdateStore implementation for VIVO.'

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name = 'vivo-rdflib-sparqlstore',
    version = '0.0.1',
    url = 'https://github.com/lawlesst/rdflib-vivo-sparqlstore',
    author = 'Ted Lawless',
    author_email = 'lawlesst@gmail.com',
    packages=find_packages(),
    install_requires=required,
    include_package_data=True,
    description = description,
    entry_points='''
        [console_scripts]
        vivoUpdate=command:process
    '''
)

