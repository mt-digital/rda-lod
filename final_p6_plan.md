#  Final plan for P6 with an eye on the future

I've done a lot of reading and reflecting on the possibilities and
usefulness of a tool so described, a "mechanism to search across the pool of 
records for data sets that have the potential to be used together" by
"express(ing) metadata element correspondences at the schema level
between DDI-RDF and DataONE properties, harmonizing
geographic/temporal ranges and units.
There is also some guidance in the project proposal to translate
metadata from XML to RDF, as well as to select a small subset of the
records from ICPSR and DataONE to use as an example.  

I've found part of this to be a real challenge, namely finding a
subset of related records. I was not too pleased with either ICPSR's
or DataONE's search capability, and I ran into immediate challenges
identifying related datasets between the two. 


## Serving Users through a web app

I don't want to use RDF because it seems esotheric and doesn't
necessarily integrate well with more familiar tools to me and, in my
opinion, with the standard developer. Lately I've been concerned about
software sustainability, and if we use RDF and a Fuseki server we're
likely to be limited in finding experts to work with these
technologies, let alone experts in metadata formats. So I want to
lower the learning curve by using MongoDB as a datastore and JSON-LD
as a format. This has the added benefit of keeping all our (meta)data
in a consistent format from server to client. However I want to keep
the full-text XML in with each MongoDB document for full-text search.
I extract the most relevant fields from each new metadata format into
the Mongo translation document, much like DataONE uses a Solr index of
select fields as well as a full-text index. In the future, a Solr
index like that could augment or even replace this Mongo architecture.
But for this initial prototype I'd like to go with what I believe is a
more common tool among developers, and one where the data model is
tightly integrated with the server code, which is the Python Flask web
framework. We can incrementally support more common fields between
data formats in a straightforward way with this scheme by just adding
another field to our NormalizedDataMore details on all this are below in the technical details
section.

## Technical Details

I will write a parser for each metadata type. Currently I've written
one to extract time and title from ICPSR, with spatial information on
the way soon. I'll also 

```python
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
```

## Linked Data

There are two main ways I'd like to use linked data: 

1. Use semantic analysis and statistics to discover clusters of
related data across datasets. This could be considered "machine
learning" since we let the machine learn what records are related.
Eventually identify an appropriate ontology for describing such
relationships.
2. Use existing APIs and their accompanying ontologies and
vocabularies like 
3. Links to the "native" (DDI, Dublin Core, EML, etc.) descriptions of
the fields (for example [DDI's time period
covered](http://www.ddialliance.org/Specification/DDI-Codebook/2.5/XMLSchema/field_level_documentation_files/schemas/codebook_xsd/elements/timePrd.html#a4))


## Long term

In software development, the products that last are products that
address specific user stories: what type of person would want to do
what specific thing? In thinking about why someone would want to be
able to 
