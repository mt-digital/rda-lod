"""
This is special for DataONE which contains three different metadata standards:
Dublin Core (DC), Ecological Markup Language (EML), and ISO 19139, the XML
implementation of ISO 19115.

This parser module will contain logic to parse each of these, even though these
might not be the only place, for example, a DC parser or EML parser will be
used. When needed by another Repository parser, the standard-specific logic
can be extracted and put into parsers/util.py or something like that.
"""
import dateutil
import json
import re
import warnings
import xml.etree.ElementTree as ET

from datetime import datetime, timedelta
from StringIO import StringIO as strio

from app.models import NormalizedMetadata

EML_SPECIFICATION_URL = \
    "https://knb.ecoinformatics.org/#external//emlparser/docs/eml-2.1.1"

DEFAULT_DATETIMES = (datetime(1000, 1, 1), datetime(3000, 1, 1))

CARD_DIR_LIST = ['west', 'east', 'north', 'south']

def make_normalized_dataone(dataone_file=None):
    """
    The super function for dataone normalization. Will check if the record is
    Dublin Core, ISO, or EML and parse accordingly.
    """
    # parse
    raw_dataone = RawDataone(dataone_file)
    tree = raw_dataone.etree

    root_tag = tree.getroot().tag

    nmd = None

    # if EML
    if 'eml' in root_tag:
        nmd = _make_normalized_eml(raw_dataone)

    # if DC

    # if ISO

    else:
        warnings.warn("No valid DataONE metadata standard detected for file" +
                      dataone_file)

    return nmd


def _make_normalized_dublin_core(xml):
    pass


def _make_normalized_eml(raw_dataone):
    """
    See https://knb.ecoinformatics.org/#external//emlparser/docs/eml-2.1.1
    """
    root = raw_dataone.etree.getroot()

    dataset = root.find('dataset')
    if not dataset:
        return None

    # TEMPORAL & GEOGRAPHIC COVERAGE
    coverage = dataset.find('coverage')

    if not coverage:
        return None

    # temporal
    temporal_coverage = coverage.find('temporalCoverage')

    if temporal_coverage:

        children_tags = [a.tag for a in temporal_coverage.getchildren()]
        if len(children_tags) > 1:
            warnings.warn(
                "Invalid EML temporalCoverage children in file: " +
                raw_dataone.file_path
            )

        child_tag = children_tags.pop()

        # if the child is a singleDateTime, make the time range the datetime
        # given plus 24 hours
        if child_tag == 'singleDateTime':

            try:
                start_date = dateutil.parser.parse(
                    temporal_coverage.find('singleDateTime').text,
                    parserinfo=dateutil.parser.parserinfo(smart_defaults=True)
                )
                start_date.hours = 0

                end_date = start_date + timedelta(days=1)

            except:
                warnings.warn(
                    'failed parsing EML '
                    '"dataset/coverage/temporalCoverage/singleDateTime" for ' +
                    raw_dataone.file_path
                )

                start_date, end_date = DEFAULT_DATETIMES

        elif child_tag == 'rangeOfDates':

            try:
                start_date = dateutil.parser.parse(
                    temporal_coverage.find(
                        'rangeOfDates/beginDate/calendarDate').text,
                    default=datetime(2014, 1, 1)
                )

                end_date = dateutil.parser.parse(
                    temporal_coverage.find(
                        'rangeOfDates/endDate/calendarDate').text,
                    default=datetime(2014, 12, 31)
                )

            except Exception as e:
                warnings.warn(
                    'failed parsing EML '
                    '"dataset/coverage/temporalCoverage/rangeOfDates" for ' +
                    raw_dataone.file_path + '\n' + e.message
                )

                start_date, end_date = DEFAULT_DATETIMES

        else:
            start_date, end_date = DEFAULT_DATETIMES

    else:

        start_date, end_date = DEFAULT_DATETIMES

    # geographic
    geo_coverage = coverage.find('geographicCoverage/boundingCoordinates')

    bbox = None
    if geo_coverage:
        try:
            bbox = {
                card_dir:
                    float(geo_coverage.find(card_dir + 'BoundingCoordinate').text)
                for card_dir in CARD_DIR_LIST
            }
        except TypeError:
            bbox = {card_dir: None for card_dir in CARD_DIR_LIST}

    # TITLE AND ABSTRACT
    # get title
    title = dataset.find('title').text

    # get abstract
    abstract_element = dataset.find('abstract/para')
    abstract = ""
    if abstract_element:
        abs_children = abstract_element.getchildren()
        if abs_children:
            try:
                abstract = abstract_element.find('literalLayout').text
            except AttributeError:
                warnings.warn('Abstract in unknown format for file ' +
                              raw_dataone.file_path)

        else:
            try:
                abstract = abstract_element.text
            except AttributeError:
                warnings.warn('Abstract in unknown format for file ' +
                              raw_dataone.file_path)

    # build and return normalized metadata
    return NormalizedMetadata.from_json(json.dumps(
        dict(raw=raw_dataone.text,
             title=title,
             # abstract=abstract,
             start_datetime=start_date.isoformat(),
             end_datetime=end_date.isoformat(),
             metadata_standard=[{'name': 'EML',
                                 'reference': EML_SPECIFICATION_URL
                                 }
                                ]
             )
        )
    )


def _make_normalized_fgdc(xml):
    pass


def _get_d1_type(xml_etree):
    """
    Determines a non-normalized metadata record's standard, either "dc" for
    Dublin Core, "eml" for Ecological Markup Language, or "fgdc" for ISO 19139.

    Arguments:
        xml_etree (xml.etree.ElementTree) Element tree representation of a
        non-normalized metadata record.
    Returns:
        (str) Metadata standard of the metadata record;
            one of "dc", "eml", or "fgdc"
    """
    pass


def el_str(xml_element):
    """
    Returns a string representation of an XML element.
    Seems like it should exist somewhere but it doesn't. See
    https://docs.python.org/2/library/xml.etree.elementtree.html
    """
    import re
    from StringIO import StringIO as strio

    io = strio()

    ET.ElementTree(xml_element).write(io)

    # clean up weird spacing I'm seeing
    exp = re.compile('\n\s+')

    return re.sub(exp, ' ', io.getvalue())


def _eltree_str(xml_element_tree):

    io = strio()

    xml_element_tree.write(io)

    # clean up weird spacing I'm seeing
    exp = re.compile('\n\s+')

    return re.sub(exp, ' ', io.getvalue())


class RawDataone:

    def __init__(self, dataone_file=None):
        if dataone_file:
            self.file_path = dataone_file
            self.text = open(dataone_file, 'r').read()
            self.etree = ET.ElementTree(ET.fromstring(self.text))

        else:
            self.text = None
            self.etree = None
