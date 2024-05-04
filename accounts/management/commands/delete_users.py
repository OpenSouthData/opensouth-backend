from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create Dummy Box locations'


    def handle(self, *args, **options):

        email = input(">>>>")

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.ERROR("User aexists"))

            user = User.objects.get(email=email)
            user.delete_permanently()

            self.stdout.write(self.style.SUCCESS("Successfully deleted user"))
    
        
        else:
            self.stdout.write(self.style.ERROR("User does not exist"))