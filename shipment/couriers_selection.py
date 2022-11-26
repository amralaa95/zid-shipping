import random
from .models import Shipment


def selectCourier() -> str:
    # a native way to choose a courier for creating a shipment for this instead of building a criteria layer
    return random.choice(Shipment.COURIER_CHOICES)[0]
