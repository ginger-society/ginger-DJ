# This file is distributed under the same license as the GingerDJ package.
#
# The *_FORMAT strings use the GingerDJ date format syntax,
# see https://docs.gingerdj.gloportal.dev/en/dev/ref/templates/builtins/#date
DATE_FORMAT = r"j E \d\e Y"
TIME_FORMAT = "G:i"
DATETIME_FORMAT = r"j E \d\e Y \a \l\e\s G:i"
YEAR_MONTH_FORMAT = r"F \d\e\l Y"
MONTH_DAY_FORMAT = r"j E"
SHORT_DATE_FORMAT = "d/m/Y"
SHORT_DATETIME_FORMAT = "d/m/Y G:i"
FIRST_DAY_OF_WEEK = 1  # Monday

# The *_INPUT_FORMATS strings use the Python strftime format syntax,
# see https://docs.python.org/library/datetime.html#strftime-strptime-behavior
DATE_INPUT_FORMATS = [
    "%d/%m/%Y",  # '31/12/2009'
    "%d/%m/%y",  # '31/12/09'
]
DATETIME_INPUT_FORMATS = [
    "%d/%m/%Y %H:%M:%S",
    "%d/%m/%Y %H:%M:%S.%f",
    "%d/%m/%Y %H:%M",
    "%d/%m/%y %H:%M:%S",
    "%d/%m/%y %H:%M:%S.%f",
    "%d/%m/%y %H:%M",
]
DECIMAL_SEPARATOR = ","
THOUSAND_SEPARATOR = "."
NUMBER_GROUPING = 3
