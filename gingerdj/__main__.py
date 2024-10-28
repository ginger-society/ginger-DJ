"""
Invokes gingerdj-admin when the gingerdj module is run as a script.

Example: python -m gingerdj check
"""

from gingerdj.core import management

if __name__ == "__main__":
    management.execute_from_command_line()
