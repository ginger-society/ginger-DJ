"""
A series of tests to establish that the command-line bash completion works.
"""

import os
import sys
import unittest

from ginger.apps import apps
from ginger.core.management import ManagementUtility
from ginger.test.utils import captured_stdout


class BashCompletionTests(unittest.TestCase):
    """
    Testing the Python level bash completion code.
    This requires setting up the environment as if we got passed data
    from bash.
    """

    def setUp(self):
        self.old_GINGER_AUTO_COMPLETE = os.environ.get("GINGER_AUTO_COMPLETE")
        os.environ["GINGER_AUTO_COMPLETE"] = "1"

    def tearDown(self):
        if self.old_GINGER_AUTO_COMPLETE:
            os.environ["GINGER_AUTO_COMPLETE"] = self.old_GINGER_AUTO_COMPLETE
        else:
            del os.environ["GINGER_AUTO_COMPLETE"]

    def _user_input(self, input_str):
        """
        Set the environment and the list of command line arguments.

        This sets the bash variables $COMP_WORDS and $COMP_CWORD. The former is
        an array consisting of the individual words in the current command
        line, the latter is the index of the current cursor position, so in
        case a word is completed and the cursor is placed after a whitespace,
        $COMP_CWORD must be incremented by 1:

          * 'ginger-admin start' -> COMP_CWORD=1
          * 'ginger-admin startproject' -> COMP_CWORD=1
          * 'ginger-admin startproject ' -> COMP_CWORD=2
        """
        os.environ["COMP_WORDS"] = input_str
        idx = len(input_str.split(" ")) - 1  # Index of the last word
        comp_cword = idx + 1 if input_str.endswith(" ") else idx
        os.environ["COMP_CWORD"] = str(comp_cword)
        sys.argv = input_str.split()

    def _run_autocomplete(self):
        util = ManagementUtility(argv=sys.argv)
        with captured_stdout() as stdout:
            try:
                util.autocomplete()
            except SystemExit:
                pass
        return stdout.getvalue().strip().split("\n")

    def test_ginger_admin_py(self):
        "ginger_admin.py will autocomplete option flags"
        self._user_input("ginger-admin sqlmigrate --verb")
        output = self._run_autocomplete()
        self.assertEqual(output, ["--verbosity="])

    def test_manage_py(self):
        "manage.py will autocomplete option flags"
        self._user_input("manage.py sqlmigrate --verb")
        output = self._run_autocomplete()
        self.assertEqual(output, ["--verbosity="])

    def test_custom_command(self):
        "A custom command can autocomplete option flags"
        self._user_input("ginger-admin test_command --l")
        output = self._run_autocomplete()
        self.assertEqual(output, ["--list"])

    def test_subcommands(self):
        "Subcommands can be autocompleted"
        self._user_input("ginger-admin sql")
        output = self._run_autocomplete()
        self.assertEqual(output, ["sqlflush sqlmigrate sqlsequencereset"])

    def test_completed_subcommand(self):
        "Show option flags in case a subcommand is completed"
        self._user_input("ginger-admin startproject ")  # Trailing whitespace
        output = self._run_autocomplete()
        for item in output:
            self.assertTrue(item.startswith("--"))

    def test_help(self):
        "No errors, just an empty list if there are no autocomplete options"
        self._user_input("ginger-admin help --")
        output = self._run_autocomplete()
        self.assertEqual(output, [""])

    def test_app_completion(self):
        "Application names will be autocompleted for an AppCommand"
        self._user_input("ginger-admin sqlmigrate a")
        output = self._run_autocomplete()
        a_labels = sorted(
            app_config.label
            for app_config in apps.get_app_configs()
            if app_config.label.startswith("a")
        )
        self.assertEqual(output, a_labels)
