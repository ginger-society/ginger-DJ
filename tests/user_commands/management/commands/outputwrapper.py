from ginger.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, **options):
        self.stdout.write("Working...")
        self.stdout.flush()
        self.stdout.write("OK")
