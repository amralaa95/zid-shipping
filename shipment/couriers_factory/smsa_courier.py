from shipment.couriers_factory.base_courier_methods import CourierFactory
import logging
from shipment.models import Shipment

logger = logging.getLogger(__name__)


class SmsaCourier(CourierFactory):
    def __init__(self):
        self.status = {
            'Pending': Shipment.PENDING,
            'Approved': Shipment.SCHEDULED,
            'Delivered': Shipment.DELIVERED,
            'Stopped': Shipment.CANCELLED
        }

    def create_order(self, **kwargs) -> str:
        tracking_id = self.generate_tracking_id()
        logger.info(f'Shipping is created for courier SMSA with tracking id {tracking_id}')
        return tracking_id

    def retrive_status(self, tracking_id: str) -> str:
        logger.info(f"Status for courier SMSA with tracking id {tracking_id} is {self.status['Approved']}")
        return self.status['Approved']

    def cancel_order(self, tracking_id: str):
        logger.info(f'Shipping is cancelled for courier SMSA with tracking id {tracking_id}')
