import requests
from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS

class MetadataParser:
    def __init__(self):
        self.ldf_endpoint = 'https://data.linkeddatafragments.org/dbpedia'

    def parse_metadata(self, resource_url):
        graph = Graph()
        graph.parse(resource_url)

        metadata = {}

        for s, p, o in graph:
            if p == RDF.type:
                metadata['type'] = str(o)
            elif p == RDFS.label:
                metadata['label'] = str(o)
            elif p == RDFS.comment:
                metadata['description'] = str(o)

        return metadata

    def fetch_linked_data_fragments(self, resource_url):
        params = {
            'subject': resource_url,
            'predicate': '*',
            'object': '*',
            'force': 'true'
        }
        response = requests.get(self.ldf_endpoint, params=params)
        response.raise_for_status()

        graph = Graph()
        graph.parse(data=response.text, format='turtle')

        metadata = {}
        for s, p, o in graph:
            if p == RDF.type:
                metadata['type'] = str(o)
            elif p == RDFS.label:
                metadata['label'] = str(o)
            elif p == RDFS.comment:
                metadata['description'] = str(o)

        return metadata
