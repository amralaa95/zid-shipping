import json
import io
from django.test import TestCase
from shipment.fixtures_factory import ShipmentFactory


class ShipmentTests(TestCase):

    def test_create_shipment(self):
        response = self.client.post('/api/v1/shipments/',
                                    data=json.dumps({
                                        "title": "test shipping",
                                        "weight": 4.4,
                                        "shipper_name": "shipper name",
                                        "shipper_country": "Egypt",
                                        "shipper_city": "Cairo",
                                        "shipper_address": "Giza, 6th October",
                                        "shipper_phone": "+201121287693",
                                        "receiver_name": "receiver name",
                                        "receiver_country": "Egypt",
                                        "receiver_city": "Cairo",
                                        "receiver_address": "Giza, Faisel",
                                        "receiver_phone": "+201121287684",
                                        "number_of_pieces": "1",
                                        "total_amount": "12"
                                    }),
                                    content_type='application/json')
        self.assertEquals(201, response.status_code)
        response = response.json()
        del response['tracking_id']
        self.assertEquals(
            {
                "title": "test shipping",
                "weight": 4.4,
                "status": "PENDING",
                "number_of_pieces": 1,
                "total_amount": 12,
                "scheduled_at": None,
                "estimated_shipping_date": None,
                "shipper_name": "shipper name",
                "shipper_country": "Egypt",
                "shipper_city": "Cairo",
                "shipper_address": "Giza, 6th October",
                "shipper_phone": "+201121287693",
                "receiver_name": "receiver name",
                "receiver_country": "Egypt",
                "receiver_city": "Cairo",
                "receiver_address": "Giza, Faisel",
                "receiver_phone": "+201121287684"
            }, response)

    def test_failed_create_shipment(self):

        response = self.client.post('/api/v1/shipments/',
                                    data=json.dumps({
                                        "title": "test shipping",
                                        "weight": 4.4,
                                        "shipper_name": "shipper name",
                                        "shipper_country": "Egypt",
                                        "shipper_city": "Cairo",
                                        "shipper_address": "Giza, 6th October",
                                        "shipper_phone": "+201121287693"
                                    }),
                                    content_type='application/json')
        self.assertEquals(400, response.status_code)
        self.assertEquals(
            {
                "number_of_pieces": ["This field is required."],
                "total_amount": ["This field is required."],
                "receiver_name": ["This field is required."],
                "receiver_country": ["This field is required."],
                "receiver_city": ["This field is required."],
                "receiver_address": ["This field is required."],
                "receiver_phone": ["This field is required."]
            }, response.json())

    def test_print_waybill(self):
        tracking_id = "5f964902797d45fd9fce17813415468f"
        ShipmentFactory(tracking_id=tracking_id)

        response = self.client.get(f'/api/v1/shipments/{tracking_id}/print/', content_type='application/json')

        self.assertEquals(200, response.status_code)
        file = io.BytesIO(response.content)
        self.assertTrue(file)

    def test_failed_print_waybill_tracking_not_found(self):
        tracking_id = "5f964902797d45fd9fce17813415468f"

        response = self.client.get(f'/api/v1/shipments/{tracking_id}/print/', content_type='application/json')

        self.assertEquals(404, response.status_code)
        self.assertEqual("Can't find tracking id", response.json())

    def test_tracking_status(self):
        tracking_id = "5f964902797d45fd9fce17813415468f"
        ShipmentFactory(tracking_id=tracking_id)

        response = self.client.get(f'/api/v1/shipments/{tracking_id}/status/',
                                   content_type='application/json')

        self.assertEquals(200, response.status_code)
        self.assertEquals('Shipping status is SCHEDULED', response.json())

    def test_failed_tracking_status_tracking_not_found(self):
        tracking_id = "5f964902797d45fd9fce17813415468f"

        response = self.client.get(f'/api/v1/shipments/{tracking_id}/status/',
                                   content_type='application/json')

        self.assertEquals(404, response.status_code)
        self.assertEqual("Can't find tracking id", response.json())

    def test_cancel_tracking(self):
        tracking_id = "5f964902797d45fd9fce17813415468f"
        ShipmentFactory(tracking_id=tracking_id)

        response = self.client.put(f'/api/v1/shipments/{tracking_id}/cancel/',
                                   content_type='application/json')

        self.assertEquals(200, response.status_code)
        self.assertEquals('Shipping is cancelled', response.json())

    def test_failed_cancel_tracking_tracking_not_found(self):
        tracking_id = "5f964902797d45fd9fce17813415468f"

        response = self.client.put(f'/api/v1/shipments/{tracking_id}/cancel/',
                                   content_type='application/json')

        self.assertEquals(404, response.status_code)
        self.assertEqual("Can't find tracking id", response.json())

    def test_failed_cancel_tracking_tracking_is_cancelled(self):
        tracking_id = "5f964902797d45fd9fce17813415468f"
        ShipmentFactory(tracking_id=tracking_id, status='CANCELLED')

        response = self.client.put(f'/api/v1/shipments/{tracking_id}/cancel/',
                                   content_type='application/json')

        self.assertEquals(400, response.status_code)
        self.assertEqual({"error": "Shipping is already cancelled"}, response.json())

    def test_update_status(self):
        tracking_id = "5f964902797d45fd9fce17813415468f"
        ShipmentFactory(tracking_id=tracking_id)

        response = self.client.post(f'/api/v1/shipments/update_status/',
                                    data=json.dumps({
                                        'tracking_id': tracking_id,
                                        'status': 'Approved'
                                    }),
                                    content_type='application/json')

        self.assertEquals(200, response.status_code)
        self.assertEquals('Shipping is updated', response.json())

    def test_failed_cancel_tracking_tracking_not_found(self):
        tracking_id = "5f964902797d45fd9fce17813415468f"

        response = self.client.post(f'/api/v1/shipments/update_status/',
                                    data=json.dumps({
                                        'tracking_id': tracking_id,
                                        'status': 'Approved'
                                    }),
                                    content_type='application/json')

        self.assertEquals(404, response.status_code)
        self.assertEqual("Can't find tracking id", response.json())
