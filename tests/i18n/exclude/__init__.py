# This package is used to test the --exclude option of
# the makemessages and compilemessages management commands.
# The locale directory for this app is generated automatically
# by the test cases.

from ginger.utils.translation import gettext as _

# Translators: This comment should be extracted
dummy1 = _("This is a translatable string.")

# This comment should not be extracted
dummy2 = _("This is another translatable string.")
