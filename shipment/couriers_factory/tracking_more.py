from http.client import BAD_REQUEST
import json
from shipment.couriers_factory.base_courier_methods import CourierFactory, Cancallable
import logging
import requests

logger = logging.getLogger(__name__)


class TrackingMoreCourier(CourierFactory, Cancallable):

    def __init__(self):
        self.URL = 'https://api.trackingmore.com/v3/trackings'
        self.API_KEY = 'v7cg2v6a-t85h-u6yi-jp9a-3swotvstdpuh'

    def create_order(self, **kwargs):
        tracking_id = self.generate_tracking_id()

        # querystring = {"tracking_numbers": "UB209300714LV"}

        payload = [{
            "title": kwargs['title'],
            "tracking_number": tracking_id,
            "courier_code": "cainiao",
            "order_number": tracking_id,
            "destination_code": kwargs['receiver_country'],
            "customer_name": kwargs['receiver_name'],
            "customer_phone": kwargs['receiver_phone'],
        }]
        headers = {'tracking-api-key': self.API_KEY, 'content-type': "application/json"}

        response = requests.request("POST", f"{self.URL}/create", data=json.dumps(payload), headers=headers)

        if len(response.error) > 0:
            raise BAD_REQUEST(response.error)

        logger.info(f"Shipping is created for courier TrackingMore with tracking id {tracking_id}")
        return tracking_id

    def retrive_status(self, tracking_id):
        pass

    def cancel_order(self, tracking_id):
        logger.info(f"Shipping is cancelled for courier TrackingMore with tracking id {tracking_id}")
