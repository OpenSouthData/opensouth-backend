from django.core.management.base import BaseCommand, CommandError
from public.models import ClientIP

class Command(BaseCommand):
    help = 'db update'


    def handle(self, *args, **options):

        orgs = ClientIP.objects.filter()

        orgs.delete()

        self.stdout.write(self.style.SUCCESS("Successfully updated"))



        