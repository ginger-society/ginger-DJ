# This file is distributed under the same license as the GingerDJ package.
#
# The *_FORMAT strings use the GingerDJ date format syntax,
# see https://docs.gingerdj.gloportal.dev/en/dev/ref/templates/builtins/#date
DATE_FORMAT = "j. F Y."
TIME_FORMAT = "H:i"
DATETIME_FORMAT = "j. F Y. H:i"
YEAR_MONTH_FORMAT = "F Y."
MONTH_DAY_FORMAT = "j. F"
SHORT_DATE_FORMAT = "j.m.Y."
SHORT_DATETIME_FORMAT = "j.m.Y. H:i"
FIRST_DAY_OF_WEEK = 1

# The *_INPUT_FORMATS strings use the Python strftime format syntax,
# see https://docs.python.org/library/datetime.html#strftime-strptime-behavior
DATE_INPUT_FORMATS = [
    "%d.%m.%Y.",  # '25.10.2006.'
    "%d.%m.%y.",  # '25.10.06.'
    "%d. %m. %Y.",  # '25. 10. 2006.'
    "%d. %m. %y.",  # '25. 10. 06.'
    # "%d. %b %y.",  # '25. Oct 06.'
    # "%d. %B %y.",  # '25. October 06.'
    # "%d. %b '%y.",  # '25. Oct '06.'
    # "%d. %B '%y.",  #'25. October '06.'
    # "%d. %b %Y.",  # '25. Oct 2006.'
    # "%d. %B %Y.",  # '25. October 2006.'
]
DATETIME_INPUT_FORMATS = [
    "%d.%m.%Y. %H:%M:%S",  # '25.10.2006. 14:30:59'
    "%d.%m.%Y. %H:%M:%S.%f",  # '25.10.2006. 14:30:59.000200'
    "%d.%m.%Y. %H:%M",  # '25.10.2006. 14:30'
    "%d.%m.%y. %H:%M:%S",  # '25.10.06. 14:30:59'
    "%d.%m.%y. %H:%M:%S.%f",  # '25.10.06. 14:30:59.000200'
    "%d.%m.%y. %H:%M",  # '25.10.06. 14:30'
    "%d. %m. %Y. %H:%M:%S",  # '25. 10. 2006. 14:30:59'
    "%d. %m. %Y. %H:%M:%S.%f",  # '25. 10. 2006. 14:30:59.000200'
    "%d. %m. %Y. %H:%M",  # '25. 10. 2006. 14:30'
    "%d. %m. %y. %H:%M:%S",  # '25. 10. 06. 14:30:59'
    "%d. %m. %y. %H:%M:%S.%f",  # '25. 10. 06. 14:30:59.000200'
    "%d. %m. %y. %H:%M",  # '25. 10. 06. 14:30'
]
DECIMAL_SEPARATOR = ","
THOUSAND_SEPARATOR = "."
NUMBER_GROUPING = 3
