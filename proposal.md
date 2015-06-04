# RDA Metadata IG Fellow Proposal

## Matthew Turner

### June 4, 2015

One goal in the process of creating linked data is translation of the
metadata into an HCLS-compliant RDF representation. However if we simply
translate exactly what is currently present in the DDI and DataONE repositories,
we won't have linked data. 

We will therefore need to annotate the given information with linkages.
For example, in this [example DataONE EML metadata
record](https://cn.dataone.org/cn/v1/object/doi:10.5063%2FAA%2Fnrs.692.1), there
is a section for geography

```xml
<boundingCoordinates>
    <westBoundingCoordinate>-120.2367</westBoundingCoordinate>
    <eastBoundingCoordinate>-120.2367</eastBoundingCoordinate>
    <northBoundingCoordinate>39.4317</northBoundingCoordinate>
    <southBoundingCoordinate>39.4317</southBoundingCoordinate>
</boundingCoordinates>
```

We could use the GeoNames API to look up the closest known entity
to the center of that bounding box by the following query

```
http://api.geonames.org/findNearby?lat=39.4317&lng=-120.2367&&username=mtpain
```

From this we can get a unique identifier for the nearest Geonamed thing and use
it in our linked (meta)data record. We could then use the `nearbyFeatures`
attribute in the Geonames linked data, specifically, using the result of the
query above,
[`<gn:nearbyFeatures
rdf:resource="http://sws.geonames.org/5404896/nearby.rdf"/>`](
http://sws.geonames.org/5404896/nearby.rdf).

By following the guidelines on the W3C's [Dataset Descriptions: HCLS Community
Profile](http://www.w3.org/2001/sw/hcls/notes/hcls-dataset/), we can further
make our link-annotated RDF metadata web friendly and conform to this powerful
standard.

Here is a rough outline of the project goals in the order they should be
accomplished:

1. Identify a couple specific ways to annotate the existing XML metadata with
linkages to other LOD resources on the web. 
2. As a proof of concept, build a program to generate the annotated RDF/HCLS
metadata automatically.
3. On a set of 5 - 10 records, some related, some not, do an experiment to see
if the chosen linkages for the metadata can actually result in user "discovery"
that the known related ones actually are related.
    - A prerequisite of this of course is to invent a scheme for such discovery
4. At this point either pursue a user interface for doing more experiments on
more datasets or see if we should instead try to identify alternative/better
metrics for discovering related metadata records
