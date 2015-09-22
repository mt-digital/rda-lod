"""
Normalized metadata model for the app. Over time the NormalizedMetadata class
will be a MongoEngine representation of a valid JSON-LD document.

Author: Matthew Turner <maturner@uidaho.edu>
Date: 9/17/2015
"""
from pyld import jsonld

from . import db


# TODO the next two models could inherit from the same class which could be
# widely used everywhere we want a display name and a URL to link to.
class MetadataStandard(db.EmbeddedDocument):
    """
    Which standard the metadata follows: no explicit restrictions, but at this
    point will be either DDI or EML. The URL will point to a linkable code
    book. Again, no explicit restrictions, but it would be great if it were a
    URL that linked to basic documentation plus could be hashed for a
    namespace, e.g. http://example.com/api/doc/field_definitions# so that
    we may link to the 'start_date' definition:
    http://example.com/api/doc/field_definitions#start_date
    """
    name = db.StringField(max_length=20, required=True)
    # reference to be used for non-specification documentation
    reference = db.URLField()


class NormalizedMetadata(db.Document):
    """
    Model served by the API to consumers. It has been normalized: parsed from
    whatever the metadata's native format and extracted to the currently
    supported terms. Imported to ../parsers for creating app-ready normalized
    metadata.
    """
    raw = db.StringField(required=True)

    title = db.StringField(required=True)
    start_datetime = db.DateTimeField(required=True)
    end_datetime = db.DateTimeField(required=True)
    abstract = db.StringField()
    geo_center = db.PointField()

    identifier = db.StringField(max_length=100)

    # allow a list of standards in case they do indeed meet multiple standards
    metadata_standard = db.EmbeddedDocumentField('MetadataStandard')

    meta = {
        'indexes': [
            'title',
            '$title',
            ('start_datetime', 'end_datetime'),
        ],
        'allow_inheritance': True
    }

    def to_jsonld(self):
        """
        Use metadata_standard.specification_root to build an expanded jsonld
        metadata record
        """


        non_ld = json.loads(self.to_json())

        return jsonld.expand(non_ld, {'expandContext': context})


HCLS_NORMALIZED_MAPPABLE = {
    'title': 'dct:title',
    'start_datetime': 'dbpedia:StartDateTime',
    'end_datetime': 'dbpedia:EndDateTime',
    'geo_center': 'lidd:geo_center'
}


# not all used, but these are all from
HCLS_PLUS_CONTEXT = {
    'cito': 'http://purl.org/spar/cito/',
    'dcat': 'http://www.w3.org/ns/dcat#',
    'dctypes': 'http://purl.org/dc/dcmitype/',
    'dct': 'http://purl.org/dc/terms/',
    'foaf': 'http://xmlns.com/foaf/0.1/',
    'freq': 'http://purl.org/cld/freq/',
    'idot': 'http://identifiers.org/terms#',
    'lexvo': 'http://lexvo.org/ontology#',
    'pav': 'http://purl.org/pav/',
    'prov': 'http://www.w3.org/ns/prov#',
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
    'sd': 'http://www.w3.org/ns/sparql-service-description#',
    'xsd': 'http://www.w3.org/2001/XMLSchema#',
    'vann': 'http://purl.org/vocab/vann/',

    # non-hcls
    'lidd': 'https://mt.northwestknowledge.net/lidd/terms#',
    'dbpedia': 'http://mappings.dbpedia.org/index.php/OntologyProperty:',
    'dbpedia:StartDateTime': {
        'rdfs:label@en': 'start date and time',
        'rdfs:comment@en': 'ISO 8601 formatted start date and time',
        '@type': 'xsd:dateTime'
    },
    'dbpedia:EndDateTime': {
        'rdfs:label@en': 'start date and time',
        'rdfs:comment@en': 'ISO 8601 formatted start date and time',
        '@type': 'xsd:dateTime'
    }
}
