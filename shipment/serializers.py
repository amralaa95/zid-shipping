from rest_framework import serializers
from shipment.models import Shipment


class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = ('title', 'weight', 'status', 'tracking_id', 'number_of_pieces', 'total_amount',
                  'scheduled_at', 'estimated_shipping_date', 'shipper_name', 'shipper_country',
                  'shipper_city', 'shipper_address', 'shipper_phone', 'receiver_name', 'receiver_country',
                  'receiver_city', 'receiver_address', 'receiver_phone',
                  )

        extra_kwargs = {
            'status': {
                'read_only': True
            },
            'tracking_id': {
                'read_only': True
            },
            'estimated_shipping_date': {
                'read_only': True
            },
            'scheduled_at': {
                'read_only': True
            }
        }

    def create(self, validated_data):
        '''
        Create a Shipment object.

        Args:
            validated_data: a DICT contains Shipment data after the validation step.

        Returns:
            The created Shipment object.
        '''

        shipment = Shipment(**validated_data)
        shipment.save()
        return shipment
