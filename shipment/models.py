import pdfkit
from jinja2 import Environment, FileSystemLoader
from django.db import models
from django.core.validators import MinValueValidator


class Shipment(models.Model):
    PENDING = 'PENDING'
    SCHEDULED = "SCHEDULED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"

    SMSA = "SMSA"
    ARAMEX = "ARAMEX"

    STATUS_CHOCIES = (
        (PENDING, PENDING),
        (SCHEDULED, SCHEDULED),
        (CANCELLED, CANCELLED),
        (DELIVERED, DELIVERED),
    )

    COURIER_CHOICES = (
        (SMSA, SMSA),
        (ARAMEX, ARAMEX)
    )

    courier = models.CharField(max_length=50, choices=COURIER_CHOICES)
    title = models.CharField(max_length=250)
    estimated_shipping_date = models.DateField(null=True)
    scheduled_at = models.DateField(null=True)
    weight = models.FloatField(validators=[MinValueValidator(1)])
    total_amount = models.FloatField(validators=[MinValueValidator(0.5)])
    number_of_pieces = models.IntegerField(validators=[MinValueValidator(1)])
    tracking_id = models.CharField(max_length=35, unique=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOCIES, default=PENDING)

    shipper_name = models.CharField(max_length=250)
    shipper_city = models.CharField(max_length=50)
    shipper_country = models.CharField(max_length=50)
    shipper_address = models.CharField(max_length=250)
    shipper_phone = models.CharField(max_length=15)

    receiver_name = models.CharField(max_length=250)
    receiver_city = models.CharField(max_length=50)
    receiver_country = models.CharField(max_length=50)
    receiver_address = models.CharField(max_length=300)
    receiver_phone = models.CharField(max_length=15)

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_waybill(self):
        """
        Return the pdf representation of this shipment

        Args:
            self: The shipment object

        Returns:
            Byte: the Byte representation of the shipment label in pdf format.
        """

        file_loader = FileSystemLoader('shipment/templates')
        env = Environment(loader=file_loader)
        template = env.get_template('waybill.html')
        str_temp = template.render(**self.to_dict())
        return pdfkit.from_string(str_temp, False)

    def to_dict(self):
        """
        Return te Dict representation of the shipment object

        Args:
            self: The shipment object

        Returns:
            DICT: a doctionary representation of the shipment object.
        """

        return {
            "title": self.title,
            "shipper_name": self.shipper_name,
            "shipper_country": self.shipper_country,
            "shipper_city": self.shipper_city,
            "shipper_address": self.shipper_address,
            "shipper_phone": self.shipper_phone,
            "receiver_name": self.receiver_name,
            "receiver_country": self.receiver_country,
            "receiver_city": self.receiver_city,
            "receiver_address": self.receiver_address,
            "receiver_phone": self.receiver_phone,
            "weight": self.weight,
            "status": self.status,
            "tracking_id": self.tracking_id,
            "estimated_shipping_date": self.estimated_shipping_date,
            "scheduled_at": self.scheduled_at,
            "number_of_pieces": self.number_of_pieces,
            "total_amount": self.total_amount
        }
