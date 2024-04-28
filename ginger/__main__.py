"""
Invokes ginger-admin when the ginger module is run as a script.

Example: python -m ginger check
"""

from ginger.core import management

if __name__ == "__main__":
    management.execute_from_command_line()
