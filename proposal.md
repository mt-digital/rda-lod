# RDA Metadata IG Fellow Proposal

## Matthew Turner

### June 10, 2015

Put simply, the goal of this project is to enable discovery of interdisciplinary
data that is related. Specifically, we will explore linking DDI metadata records
with DataONE metadata records as a test case. 

This project will procede by the following steps:

1. Create RDF translations, including geographic and temporal information, of 
an initially small set of DDI and DataONE metadata records

2. Demonstrate geospatially-enabled SPARQL queries
    a. Stand up a geospatially-enabled SPARQL endpoint. 
    b. Generate appropriate SPARQL queries for finding spatially- and
        temorally-related datasets via their metadata

3. Create user interface for 1 and 2

4. Make the translations conform to [W3C Health Care and Life Sciences
(HCLS)](http://www.w3.org/2001/sw/hcls/notes/hcls-dataset/) standard


Here is an [example DataONE EML metadata
record](https://cn.dataone.org/cn/v1/object/doi:10.5063%2FAA%2Fnrs.692.1)'s
bounding box section

```xml
<boundingCoordinates>
    <westBoundingCoordinate>-120.2367</westBoundingCoordinate>
    <eastBoundingCoordinate>-120.2367</eastBoundingCoordinate>
    <northBoundingCoordinate>39.4317</northBoundingCoordinate>
    <southBoundingCoordinate>39.4317</southBoundingCoordinate>
</boundingCoordinates>
```

We can trivially extract the centroid from this bounding box. Then we can 
get nearby features as shown by this 
[query to get cities within 20 miles of the centroid](http://geosparql.appspot.com/search?q=SELECT++%3Fname+%3Fcountry+%3Fpopulation%0D%0AWHERE%0D%0A++{+%0D%0A+++++%3Fcity+gs%3Anearby%2842.705387+-120+10%29+.%0D%0A+++++%3Fcity+gn%3Aname+%3Fname+.%0D%0A+++++%3Fcity+gn%3AinCountry+%3Fcountry+.%0D%0A+++++%3Fcity+gn%3Apopulation+%3Fpopulation%0D%0A++}%0D%0A
), which is the result of the following query run through http://geosparql.org: 

```sparql
SELECT ?name ?population
WHERE
{ 
     ?city gs:nearby(39.4317 -120.2367 20) .
     ?city gn:name ?name .
     ?city gn:population ?population 
}
```

The DDI metadata does not seem to necessarily contain geospatial coordinates or
an explicit field for a geoname, so generating one will take some thought.

We can extend our Fuseki server we set up by building spatial indices and adding
ontologies as needed, as explained in the [Apache Jena
documentation](https://jena.apache.org/index.html), ["Spatial Searches with
SPARQL"](https://jena.apache.org/documentation/query/spatial-query.html). 

For an example of selecting RDF records within a particular temporal range,
see this example from the [W3C SPARQL
Recommendation](http://www.w3.org/TR/sparql11-query/#expressions) on 
how to query with [xsd:dateTime](http://www.w3.org/TR/xmlschema-2/#dateTime) 
filters: www.w3.org/TR/sparql11-query/#expressions
