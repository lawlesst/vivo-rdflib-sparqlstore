from setuptools import setup, find_packages

description = 'RDFLib SPARQLStore and SPARQLUpdateStore implementation for VIVO.'

setup(
    name='vivo-rdflib-sparqlstore',
    version='0.3',
    url='https://github.com/lawlesst/rdflib-vivo-sparqlstore',
    author='Ted Lawless',
    author_email='lawlesst@gmail.com',
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

