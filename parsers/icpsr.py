"""
ICPSR Parser for ingestion into normalized-for-discovery (nfd) metadata store.
<<<<<<< HEAD
=======


>>>>>>> 1572cc58a6dfc6ad1a6224d32770e2ec9c808d0f
"""
import re
import warnings

import calendar
<<<<<<< HEAD
import json

=======
>>>>>>> 1572cc58a6dfc6ad1a6224d32770e2ec9c808d0f
from datetime import datetime
import dateutil.parser as dup
import xmltodict as x2d

<<<<<<< HEAD
from app.models import NormalizedMetadata


DDI_DOC_URL = 'http://www.ddialliance.org/Specification/DDI-Codebook/2.5/XMLSchema/field_level_documentation.html'


def make_normalized_icpsr(icpsr_file=None):

        raw = RawICPSR(icpsr_file)
        date_range = NormalizedDateEntry(raw)
        start_date = date_range.start_time
        end_date = date_range.end_time

        title = _extract_title(raw)

        document_str = json.dumps(
            dict(raw=raw.text,
                 title=title,
                 start_datetime=start_date.isoformat(),
                 end_datetime=end_date.isoformat(),
                 metadata_standard=[{'name': 'DDI', 'reference': DDI_DOC_URL}]
                 )
        )

        return NormalizedMetadata.from_json(document_str)


def _extract_title(raw_icpsr):
    md = raw_icpsr.metadata_dict
    return md['codeBook']['docDscr']['citation']['titlStmt']['titl']
=======

class ICPSR:

    def __init__(self, icpsr_file=None):
        self.raw = RawICPSR(icpsr_file)
        self.date_range = NormalizedDateEntry(self.raw)
        self.start_date = self.date_range.start_time
        self.end_date = self.date_range.end_time
>>>>>>> 1572cc58a6dfc6ad1a6224d32770e2ec9c808d0f


class NormalizedDateEntry:

    def __init__(self, raw_icpsr):
        self.start_time, self.end_time = _get_time_periods(raw_icpsr)
        self.valid = self.start_time <= self.end_time
        if not self.valid:
            warnings.warn("Start time is greater than end time")


class RawICPSR:

    def __init__(self, icpsr_file=None):
        if icpsr_file:
<<<<<<< HEAD
            self.text = open(icpsr_file).read()
=======
            self.text = open(icpsr_file)
>>>>>>> 1572cc58a6dfc6ad1a6224d32770e2ec9c808d0f
            self.metadata_dict = x2d.parse(self.text)

        else:
            self.text = None
            self.dict = None


def _get_time_periods(raw_icpsr):
    """
    Extracts the time periods to transform

    <timePrd event="start" date="1862" cycle="P1">
    </timePrd>
    <timePrd event="end"   date="1865" cycle="P1">
    </timePrd>

    to a list of dates to be used to build a NormalizedDateEntry.
    """
    md_dict = raw_icpsr.metadata_dict

    # a list
<<<<<<< HEAD
    try:
        time_prds = \
            md_dict['codeBook']['stdyDscr']['stdyInfo']['sumDscr']['timePrd']
    except:
        start_time = datetime(1000, 1, 1)
        end_time = datetime(3000, 1, 1)
        return start_time, end_time
=======
    time_prds = \
        md_dict['codeBook']['stdyDscr']['stdyInfo']['sumDscr']['timePrd']
>>>>>>> 1572cc58a6dfc6ad1a6224d32770e2ec9c808d0f

    # on brief inspection these seem to be the dominant date patterns in
    # ICPSR DDI metadata. Unfortunately the standard provides no date format
    # requirements, only suggest ISO 8601
    year_pattern = re.compile('^[0-9]{4}$')
    year_mo_pattern = re.compile('^[0-9]{4}-[0-9][1-2]$')

    if not type(time_prds) is list:

        time_prd = time_prds

        assert time_prd['@event'] == 'single', \
            "Bad Metadata: A single time step must have event type single"

        single_time_period = time_prd['@date']

        if year_pattern.match(single_time_period.strip()):
            year = int(single_time_period)
            start_time = datetime(year, 1, 1)
            end_time = datetime(year, 12, 31)

        elif year_mo_pattern.match(single_time_period.strip()):
            year, mo = (int(el) for el in single_time_period.split('-'))
            start_time = datetime(year, mo, 1)
            end_time = datetime(year, mo, calendar.monthrange(year, mo)[1])

        else:
            try:
                start_time = dup.parse(single_time_period)
                end_time = dup.parse(single_time_period)
            except:
<<<<<<< HEAD
                start_time = datetime(1000, 1, 1)
                end_time = datetime(3000, 12, 31)

    elif len(time_prds) == 2:

        try:
            start_time_period = filter(lambda p: p['@event'] == 'start',
                                       time_prds).pop()['@date']

            end_time_period = filter(lambda p: p['@event'] == 'end',
                                     time_prds).pop()['@date']
        except:
            start_time_period = '1000-01-01'
            end_time_period = '3000-12-31'
=======
                start_time = None
                end_time = None

    elif len(time_prds) == 2:

        start_time_period = filter(lambda p: p['@event'] == 'start',
                                   time_prds).pop()['@date']

        end_time_period = filter(lambda p: p['@event'] == 'end',
                                 time_prds).pop()['@date']
>>>>>>> 1572cc58a6dfc6ad1a6224d32770e2ec9c808d0f

        if (year_pattern.match(start_time_period) and
                year_pattern.match(end_time_period)):

            start_time = datetime(int(start_time_period.strip()), 1, 1)
            end_time = datetime(int(end_time_period.strip()), 12, 31)

        elif (year_mo_pattern.match(start_time_period) and
              year_mo_pattern.match(end_time_period)):

<<<<<<< HEAD
            year, mo = (int(el) for el in start_time_period.split('-'))
=======
            year, mo = (int(el) for el in single_time_period.split('-'))
>>>>>>> 1572cc58a6dfc6ad1a6224d32770e2ec9c808d0f
            # start at beginning of month, day not given
            start_time = datetime(year, mo, 1)
            # end at the end of the month given
            end_time = datetime(year, mo, calendar.monthrange(year, mo)[1])

        else:  # if things are weird, just try dateutil.parse.parse
            start_time = dup.parse(start_time_period)
            end_time = dup.parse(end_time_period)

<<<<<<< HEAD
    else:

        start_time = datetime(1000, 1, 1)
        end_time = datetime(3000, 1, 1)

=======
>>>>>>> 1572cc58a6dfc6ad1a6224d32770e2ec9c808d0f
    return start_time, end_time
