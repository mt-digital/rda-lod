"""
Normalized metadata model for the app. Over time the NormalizedMetadata class
will be a MongoEngine representation of a valid JSON-LD document.
"""
from . import db


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

    # allow a list of standards in case they do indeed meet multiple standards
    metadata_standard = db.ListField(db.EmbeddedDocumentField('MetadataStandard'))

    meta = {
        'indexes': [
            'title',
            '$title',
            ('start_datetime', 'end_datetime')
        ],
        'allow_inheritance': True
    }

    def format_dates(self):
        """
        Our web form needs the date to be in YYYY-MM-DD (ISO 8601)
        """
        for el in [self.start_date, self.end_date, self.first_pub_date]:
            el = el.isoformat()
