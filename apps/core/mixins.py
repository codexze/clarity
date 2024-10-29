from dateutil import parser
from django.utils.dateparse import parse_date
import logging

logger = logging.getLogger(__name__)

class TwoDigitYearParserInfo(parser.parserinfo):
    def convertyear(self, year, century_specified=False):
        """
        Converts two-digit years to year
        range of self._year (current local time)
        """

        # Function contract is that the year is always positive
        assert year >= 0
        if year < 100 and not century_specified:
            # assume current century to start
            year += self._century
            if year > self._year:  # if too far in future
                year -= 100

        return year

def parse_queried_date(date):
    value = date.replace('-', '')  # remove dashes if any

    try:
        if len(value) == 6:
            date = '%s-%s-%s' % (value[0:2], value[2:4], value[4:6])
            date_parse = parser.parse(date, dayfirst=True, parserinfo=TwoDigitYearParserInfo())

            return date_parse.date()

        if len(value) == 8:
            date = '%s-%s-%s' % (value[0:2], value[2:4], value[4:8])
            date_parse = parser.parse(date, dayfirst=True)

            return date_parse.date()

        elif parse_date(value):
            date = parse_date(value)
            date_parse = date if date else None

            return date_parse.date()

    except Exception as e:
        logger.info(f"Can't parse date: {str(e)}")
        return date