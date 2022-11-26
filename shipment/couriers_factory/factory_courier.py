from ..couriers_factory.aramex_courier import AramexCourier
from ..couriers_factory.smsa_courier import SmsaCourier
from ..couriers_factory.base_courier_methods import CourierFactory


class FactoryCourier():

    @classmethod
    def create_courier_class(cls, courier_type: str) -> CourierFactory:
        Couriers = {'ARAMEX': AramexCourier, 'SMSA': SmsaCourier}
        return Couriers[courier_type]()