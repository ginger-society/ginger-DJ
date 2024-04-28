#!/usr/bin/env python
import sys

from ginger.conf import settings
from ginger.core.management import execute_from_command_line

if __name__ == "__main__":
    settings.configure(DEBUG=True, CUSTOM=1)
    execute_from_command_line(sys.argv)
