import factory
from factory.django import DjangoModelFactory

from shipment.models import Shipment


class ShipmentFactory(DjangoModelFactory):
    class Meta:
        model = Shipment

    title = factory.Faker('word')
    shipper_name = factory.Faker('first_name')
    shipper_address = factory.Faker('word')
    shipper_country = factory.Faker('word')
    shipper_city = factory.Faker('word')
    shipper_phone = factory.Faker('word')
    receiver_name = factory.Faker('first_name')
    receiver_address = factory.Faker('word')
    receiver_country = factory.Faker('word')
    receiver_city = factory.Faker('word')
    receiver_phone = factory.Faker('word')
    weight = 5.2
    tracking_id = factory.Faker('word')
    total_amount = 2
    number_of_pieces = 1
    courier = 'SMSA'
    status = 'PENDING'