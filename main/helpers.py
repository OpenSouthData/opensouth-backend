import random 
from .models import VerificationPin





def generate_organisation_pin(organisation):

    """
    Generates a random 6 digit pin
    """
    
    pin = random.randint(100000, 999999)

    VerificationPin.objects.create(
        organisation=organisation,
        pin=pin
    )


    return pin





