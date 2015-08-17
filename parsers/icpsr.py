"""
ICPSR Parser for ingestion into normalized-for-discovery (nfd) metadata store.
"""
import re
import warnings

import calendar
from datetime import datetime
import dateutil.parser as dup
import xmltodict as x2d

from ..app.models import NormalizedMetadata, MetadataStandard


DDI_DOC_URL = 'http://www.ddialliance.org/Specification/DDI-Codebook/2.5/XMLSchema/field_level_documentation.html'


def make_normalized_icpsr(self, icpsr_file=None):

        raw = RawICPSR(icpsr_file)
        date_range = NormalizedDateEntry(self.raw)
        start_date = self.date_range.start_time
        end_date = self.date_range.end_time

        metadata_standard = MetadataStandard('DDI', DDI_DOC_URL)

        return NormalizedMetadata(raw, date_range, start_date,
                                  end_date, metadata_standard)


class NormalizedDateEntry:

    def __init__(self, raw_icpsr):
        self.start_time, self.end_time = _get_time_periods(raw_icpsr)
        self.valid = self.start_time <= self.end_time
        if not self.valid:
            warnings.warn("Start time is greater than end time")


class RawICPSR:

    def __init__(self, icpsr_file=None):
        if icpsr_file:
            self.text = open(icpsr_file)
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
    time_prds = \
        md_dict['codeBook']['stdyDscr']['stdyInfo']['sumDscr']['timePrd']

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
                start_time = None
                end_time = None

    elif len(time_prds) == 2:

        start_time_period = filter(lambda p: p['@event'] == 'start',
                                   time_prds).pop()['@date']

        end_time_period = filter(lambda p: p['@event'] == 'end',
                                 time_prds).pop()['@date']

        if (year_pattern.match(start_time_period) and
                year_pattern.match(end_time_period)):

            start_time = datetime(int(start_time_period.strip()), 1, 1)
            end_time = datetime(int(end_time_period.strip()), 12, 31)

        elif (year_mo_pattern.match(start_time_period) and
              year_mo_pattern.match(end_time_period)):

            year, mo = (int(el) for el in single_time_period.split('-'))
            # start at beginning of month, day not given
            start_time = datetime(year, mo, 1)
            # end at the end of the month given
            end_time = datetime(year, mo, calendar.monthrange(year, mo)[1])

        else:  # if things are weird, just try dateutil.parse.parse
            start_time = dup.parse(start_time_period)
            end_time = dup.parse(end_time_period)

    return start_time, end_time
