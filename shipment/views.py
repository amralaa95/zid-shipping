import logging

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
import random
from .serializers import ShipmentSerializer
from .models import Shipment
from .couriers_factory.factory_courier import FactoryCourier

logger = logging.getLogger(__name__)


class ShipmentResource(viewsets.ModelViewSet):

    serializer_class = ShipmentSerializer
    queryset = Shipment.objects.all()
    lookup_field = 'tracking_id'
   
    def create(self, request):
        """Create a Shipment"""

        try:
            data = request.data
            serializer = self.serializer_class(data=data, context={'request': request})
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            courier = random.choice(Shipment.COURIER_CHOICES)[0]
            courier_type_obj = FactoryCourier().create_courier_class(courier)
            tracking_id = courier_type_obj.create_order(**data)

            serializer.save(courier=courier, tracking_id=tracking_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.exception(f"Error {e} while creating a new shipment")
            return Response({"error": "error happened please try again later"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, tracking_id=None):
        """Retrieve a Shipment"""
        instance = self.get_object()
        return Response(self.serializer_class(instance).data,
                        status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='update_status')
    def update_status(self, request):
        """Webhook for third party to update status for given tracking id"""

        try:
            tracking_id = request.data['tracking_id']
            shipment = Shipment.objects.get(tracking_id=tracking_id)

            courier_type_obj = FactoryCourier().create_courier_class(shipment.courier)
            courier_status = request.data['status']

            shipment.status = courier_type_obj.status[courier_status]
            shipment.save()

            return Response("Shipping is updated", status=status.HTTP_200_OK)
        except Shipment.DoesNotExist:
            return Response("Can't find tracking id", status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.exception(f"Error {e} while get shipping status")
            return Response({"error": "error happened please try again later"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], url_path='(?P<tracking_id>[^/.]+)/status')
    def tracking_status(self, request, tracking_id):
        """Get status for given tracking id"""

        try:
            shipment = Shipment.objects.get(tracking_id=tracking_id)
            courier_type_obj = FactoryCourier().create_courier_class(shipment.courier)
            shipment_status = courier_type_obj.retrive_status(tracking_id)

            return Response(f"Shipping status is {shipment_status}", status=status.HTTP_200_OK)
        except Shipment.DoesNotExist:
            return Response("Can't find tracking id", status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.exception(f"Error {e} while get shipping status")
            return Response({"error": "error happened please try again later"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], url_path='(?P<tracking_id>[^/.]+)/print')
    def print(self, request, tracking_id):
        """Print waybill for given tracking id"""

        try:
            shipment = Shipment.objects.get(tracking_id=tracking_id)
            label = shipment.get_waybill()

            res = HttpResponse(label, content_type='application/pdf')
            res['Content-Disposition'] = f'attachment; filename={shipment.tracking_id}.pdf'

            return res
        except Shipment.DoesNotExist:
            return Response("Can't find tracking id", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception(f"Error {e} while printing labels")
            return Response({"error": "error happened please try again later"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['put'], url_path='(?P<tracking_id>[^/.]+)/cancel')
    def cancel(self, request, tracking_id):
        """Cancel shipping for given tracking id"""
        try:
            shipment = Shipment.objects.get(tracking_id=tracking_id)
            if shipment.status == Shipment.CANCELLED:
                return Response({"error": "Shipping is already cancelled"},
                                status=status.HTTP_400_BAD_REQUEST)

            courier_type_obj = FactoryCourier().create_courier_class(shipment.courier)
            courier_type_obj.cancel_order(tracking_id)

            shipment.status = Shipment.CANCELLED
            shipment.save()

            return Response("Shipping is cancelled", status=status.HTTP_200_OK)
        except Shipment.DoesNotExist:
            return Response({"error": "Can't find tracking id"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.exception(f"Error {e} while cancelling shipping")
            return Response({"error": "error happened please try again later"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
