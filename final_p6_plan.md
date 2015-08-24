<!DOCTYPE html>
<html>
<head>
<!-- Latest compiled and minified CSS -->
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">

<!-- Optional theme -->
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap-theme.min.css">

<!-- Latest compiled and minified JavaScript -->
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
<title>Plan for Plenary</title>
</head>


<body>
<div class="container">
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

### Why another search interface? ICPSR and DataONE have their own.

<div class="row">
<img align="left" id="stallman" src="Richard_Stallman_-_Fete_de_lHumanite_2014_-_010.jpg" alt="Richard
Stallman, founder of the Free Software Foundation"/>
\begin{figure}
\begin{center}
\includegraphics[width=2in]{Richard_Stallman_-_Fete_de_lHumanite_2014_-_010.jpg}
\caption{Richard Stallman, founder of the Free Software Foundation}
\end{center}
\end{figure}
<p>
Because I didn't like using either. And to adapt a famous quote from the founder
of the Free Software Foundation Richard Stallman, 
I wanted to freely explore the metadata records in both ICPSR and DataONE
Repositories: "free like freedom, not free like free beer". 
</p>

Another reason is that a generic or pre-existing search interface won't
be able to serve my needs exactly as I move forward. 
I want the interface to be a publication like
a paper. We talk about software and data publications--why not have a software
publication version of some work someone did, even if a lot of the basics might
_might_ be covered in another work. Reading a paper on software sometimes
feels useless: why not just write the software well and present it on the web? 
Make web interfaces for data products as ubiquitous as latex. 


<p id="stallman-citation">
<em>
"Richard Stallman -
Fête de l'Humanité 2014 - 010" by Thesupermat - Own work. Licensed under CC
BY-SA 3.0 via Commons -
<a
href="https://commons.wikimedia.org/wiki/File:Richard_Stallman_-_F%C3%AAte_de_l%27Humanit%C3%A9_2014_-_010.jpg#/media/File:Richard_Stallman_-_F%C3%AAte_de_l%27Humanit%C3%A9_2014_-_010.jpg">https://commons.wikimedia.org/wiki/File:Richard_Stallman_-_F%C3%AAte_de_l%27Humanit%C3%A9_2014_-_010.jpg#/media/File:Richard_Stallman_-_F%C3%AAte_de_l%27Humanit%C3%A9_2014_-_010.jpg</a>
</em>
</p>
</div>

I'll briefly explore the limitations of both [ICPSR Data
Search](https://www.icpsr.umich.edu/icpsrweb/ICPSR/) and DataONE's
[ONEMercury search](https://cn.dataone.org/onemercury/). Below is a screenshot
 my search for the Endangered Species Act, which I
thought would be a fruitful intersection of social and ecological data.

![ESA Search Results on ICPSR](icpsr_esa_search_results.png) 

Clicking through the search results, then using the browser to search the page for
"endangered species" or even just "endangered" shows nothing. So if we even just
improved the search interface for ICPSR, we'd have a win.

The Whooping Crane happens to be the first species I think of when I think of
the ESA. I spent time in Houston. I helped administer surveys during the annual 
CraneFest at Port Aransas, Texas, near the cranes' main winter home. As the 
saying goes, "go with what you know". So that's what I'm doing. 
Here's a detailed view of a DataONE SOLR-indexed search result of 
"whooping crane". 

![DataONE detailed view of a search result](data_one_search_result_unlinked_detail.png)

Not bad at all, but it's not linked. Easily those could have been hyperlinks,
thus making that metadata instantly _linked_ to an outside source.

As for an external source, it'd be nice to have one with an obvious API. 
Wolfram Alpha's API couldn't be simpler for search. 
We can easily link an identical search for further information, like so: 

Have a look, Wolfram|Alpha works pretty well for ["Whooping
Crane"](http://www.wolframalpha.com/input/?i=whooping+crane#). Not as well for 
"endangered speices act":

![Wolfram|Alpha search results for "endangered species act"](wolfram_alpha_endangered_species_act.png)

Wolfram|Alpha is one of the often-cited sources for semantic searching even
though they claim to be a _Computational_ Knowledge Engine.  Plus their API was
instantly recognizable. Compare that to DBPedia which requires a SPARQL query.
Why SPARQL? Look at the Wikipedia API. Wikipedia provides an 
[API sandbox](https://en.wikipedia.org/wiki/Special:ApiSandbox#action=query&list=search&srsearch=Albert%20Einstein&utf8=) 
and [documentation](https://www.mediawiki.org/wiki/API:Main_page) 
all through straightforward HTTP requests. If our goal is to make linked data
widely useful to humanity I think we should avoid SPARQL. The tools to create
SPARQL endpoints are few and poorly documented. The tools for creating HTTP APIs
are many and well documented. Fielding's famed [thesis Chapter 5 on
Representational State
Transfer](https://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm)
is popular for a reason: "the REST architectural style from other network-based
styles is its emphasis on a uniform interface between components." Furthermore,
it presents a clear split between "verbs" and "nouns", and their identification
in the existing HTTP scheme: verbs are built in and the main ones we need are
GET, POST, PUT, and DELETE. No need to introduce any more verbs. The nouns of
REST are _resources_. In the API I've built so far there are four resources:

1. `/api/metadata`
1. `/api/metadata/<string:_oid>`
1. `/api/metadata/<string:_oid>/raw`
1. `/api/metadata/search`


In my _innovation-decision_ process, I recognize an anxiety to adopt SPARQL
because the community that wants that is so much smaller and there are less
resources for me or other developers to learn from. Alternatively, REST 
provides an answer to the same problem, but designed to fit the web.

The first of the final two sections describe some technical details of what 
I've done so far. The second of the final two sections describes where I plan to
take this, maybe answering a question you might have at this point, namely,
"Where's the linked data?"


## Technical Details

I've set up a REST API backend that can be used 
independently and web app frontend that uses the API to query the metadata.

My general framework for implementing this is illustrated in the figure below.
Each new metadata standard or repository is ingested into a normalized metadata
model. This model is shown in its current, minimal form below.  This is the
actual model used in the _Model-View-Controller_ architecture of the REST API. I
also use it during the ingestion step: each metadata source gets its own
_parser_, contained in the 
[rda-lod/parsers](https://github.com/mtpain/rda-lod/tree/master/parsers)
directory.

![](lidd-hierarchy.png)


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

Since each normalized field sits in a Mongo collection and we can do full-text
indexes on arbitrary fields. In the current iteration of the
`NormalizedMetadata` model, `$index` denotes one of those fields flagged 
for full-text search. For the P6 meeting, I'll add abstracts to the model
and index those for full-text search as well. I'll experiment with a full-text
search on the full native metadata records themselves, stored in the `raw` 
field of `NormalizedMetadata`.


## Linked Data

### Clustering/Linking via Computed Metadata Relationships

You probably noticed the "Linking" box in the section above and gotten an idea
of one of the ways I'd like to use linked data. I want to use the right
ontologies to describe inherent linkages between (meta)data. 
I want to do clustering be it via geographic clustering of metadata records 
based on their geospatial locations, temporal clustering based on 
the timespans the data cover, or text-based clustering and topic modeling 
based on the titles and abstracts. Why not try to use keywords, you might ask? 
Because of my principle of rapid prototyping: I think we can get to better 
linking faster by using full-text instead of keywords coming from diverse
standards which may or may not overlap. Scientists or the people who created the
metadata might not have known the full vocabulary anyway, or the vocabulary may
actually not be well-designed for the domain scientists who are forced to use
it. Put more scientifically, my hypothesis is that keywords are relatively poor
indicators of the actual content contained in the data. A corollary to that is
that this inherent poorness of representation compounds itself when trying to
link datasets together based on the content of their metadata.


### 3rd Party Web Linking

More traditionally, I will ensure that both my API and web app deliver
hyperlinks wherever a URL is found. Each normalized metadata record will link
back to its native metadata standard, which is what I'm trying to do in the 
`metadata_standard`.  It will also link to the native definition of each
`NormalizedMetadata` field, for example 
[DDI's time period
covered](http://www.ddialliance.org/Specification/DDI-Codebook/2.5/XMLSchema/field_level_documentation_files/schemas/codebook_xsd/elements/timePrd.html#a4).

Furthermore, I'll include searches to other sources like Wikipedia and
Wolfram|Alpha. As I said before, I'm hesitant to link to DBPedia because of the
time investment to learn its API. Plus, one search I did for "Whooping Crane"
took way too long.


## Long term

</div>
</body>
</html>