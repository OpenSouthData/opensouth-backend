from django.core.management.base import BaseCommand, CommandError
from main.models import LocationAnalysis


class Command(BaseCommand):
    help = 'db update'


    def handle(self, *args, **options):

        orgs = LocationAnalysis.objects.filter()

        orgs.delete()

        self.stdout.write(self.style.SUCCESS("Successfully updated"))



        