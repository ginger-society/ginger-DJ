from ginger.core.checks import Tags
from ginger.core.management.base import BaseCommand


class Command(BaseCommand):
    requires_system_checks = [Tags.staticfiles, Tags.models]

    def handle(self, *args, **options):
        pass
