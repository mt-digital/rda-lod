"""
This is special for DataONE which contains three different metadata standards:
Dublin Core (DC), Ecological Markup Language (EML), and ISO 19139, the XML
implementation of ISO 19115.

This parser module will contain logic to parse each of these, even though these
might not be the only place, for example, a DC parser or EML parser will be
used. When needed by another Repository parser, the standard-specific logic
can be extracted and put into parsers/util.py or something like that.
"""
