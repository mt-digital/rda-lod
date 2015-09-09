"""API"""
import json
import dateutil.parser as dup

from flask import request, jsonify, Response
from flask import current_app as app
from flask_cors import cross_origin

from . import api
from ..models import NormalizedMetadata


@api.route('/api/metadata', methods=['GET'])
@cross_origin(origin='*', methods=['GET'],
              headers=['X-Requested-With', 'Content-Type', 'Origin'])
def metadata():
    """Handle get and push requests coming to metadata server"""

    docs = NormalizedMetadata.objects()[8000:8100]

    formatted_docs = [

        _format_normal_metadata(document)

        for document in docs
    ]

    return jsonify(dict(results=formatted_docs, count=len(docs)))


def _text_search_jsonified(search_args):

    search_results = []
    for key in search_args:
        search_results += \
            NormalizedMetadata.objects.search_text(search_args[key])

    formatted_search_results = [

        _format_normal_metadata(document)

        for document in search_results
    ]

    results_dict = dict(results=formatted_search_results)

    return jsonify(results_dict)


def _format_normal_metadata(document):
    append = ''
    if app.config['PRODUCTION']:
        append = '/lidd'

    return {
        'id': str(document.id),
        'title': document.title,
        'native_identifier': document.identifier,
        'raw':
            'http://{}{}/api/metadata/{}/raw'.format(request.host,
                                                     append, document.id),
        'permalink':
            'http://{}{}/api/metadata/{}'.format(request.host,
                                                 append, document.id),
        'start_datetime': document.start_datetime.isoformat(),
        'end_datetime': document.end_datetime.isoformat(),
        'metadata_standards': document.metadata_standard
    }

BAD_DATETIME_RESPONSE = lambda datetime_query_key: Response(
    '<p><pre><code>{}</code></pre> format is not recognized. Try '
    '<a href="https://en.wikipedia.org/wiki/ISO_8601">ISO 8601</a>'
    '. Example: 1985-01-01T10:00:00-007</p>'.format(datetime_query_key),

    400
)


@api.route('/api/metadata/search', methods=['GET', 'PUT'])
@cross_origin(origin='*', methods=['GET', 'PUT'],
              headers=['X-Requested-With', 'Content-Type', 'Origin'])
def metadata_search():
    """Get the JSON representation of the metadata record with given id.
    """
    _known_keys = ('title', 'min_start_datetime', 'max_start_datetime',
                   'min_end_datetime', 'max_end_datetime', 'eml', 'ddi')

    search_args = request.args

    unknown_keys = []

    search_all_standards = (
        (('eml' in search_args and search_args['eml'] == 'true')
         and ('ddi' in search_args and search_args['ddi'] == 'true'))
        or ('eml' not in search_args and 'ddi' not in search_args)
        )

    # create base search object list by filtering standards
    md_objs = None
    if search_all_standards:
        md_objs = NormalizedMetadata.objects()

    elif 'eml' in search_args and search_args['eml'] == 'true':
        md_objs = NormalizedMetadata.objects(
            metadata_standard__name='EML'
        )

    elif 'ddi' in search_args and search_args['ddi'] == 'true':
        md_objs = NormalizedMetadata.objects(
            metadata_standard__name='DDI'
        )

    for k in search_args.keys():

        if k in _known_keys:
            if k == 'title':
                md_objs = md_objs.search_text(search_args[k])

            elif k == 'min_start_datetime':

                val = search_args[k]
                try:
                    parsed_date = dup.parse(val)
                    md_objs = md_objs.filter(end_datetime__gt=parsed_date)

                except Exception:
                    return BAD_DATETIME_RESPONSE(k)

            elif k == 'max_start_datetime':

                val = search_args[k]
                try:
                    parsed_date = dup.parse(val)
                    md_objs = md_objs.filter(start_datetime__lt=parsed_date)

                except:

                    return BAD_DATETIME_RESPONSE(k)

            elif k == 'min_end_datetime':

                val = search_args[k]
                try:
                    parsed_date = dup.parse(val)
                    md_objs = md_objs.filter(end_datetime__gt=parsed_date)

                except:

                    return BAD_DATETIME_RESPONSE(k)

            elif k == 'max_end_datetime':

                val = search_args[k]
                try:
                    parsed_date = dup.parse(val)
                    md_objs = md_objs.filter(end_datetime__lt=parsed_date)

                except:

                    return BAD_DATETIME_RESPONSE(k)

        else:
            unknown_keys.append(k)

    if unknown_keys:

        return "<h1>Unknown Key(s): {}</h1>".format(', '.join(unknown_keys))

    else:

        return _jsonified_search_results(md_objs)

def _jsonified_search_results(search_results):
    """
    helper for formatting a list of search results into the jsonified
    version that is ready to return from a view function
    """
    return jsonify(dict(count=len(search_results),
                        results=[
        _format_normal_metadata(document)
        for document in search_results
        ])
    )


@api.route('/api/metadata/<string:_oid>')
@cross_origin(origin='*', methods=['GET'])
def get_single_metadata(_oid):
    """Get the common XML representation of the metadata record with
       given id.
    """
    record = NormalizedMetadata.objects.get_or_404(pk=_oid)

    formatted_record = _format_normal_metadata(record)

    return jsonify(formatted_record)


@api.route('/api/metadata/<string:_oid>/raw')
@cross_origin(origin='*', methods=['GET'])
def get_single_xml_metadata(_oid):
    """Get the common XML representation of the metadata record with
       given id.
    """
    record = NormalizedMetadata.objects.get_or_404(pk=_oid)

    raw_xml_string = json.loads(record.to_json())['raw']

    return Response(raw_xml_string, 200, mimetype='application/xml')
