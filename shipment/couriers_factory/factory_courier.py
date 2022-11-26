from ..couriers_factory.aramex_courier import AramexCourier
from ..couriers_factory.smsa_courier import SmasCourier


class FactoryCourier():
    @classmethod
    def create_courier_class(cls, courier_type):
        if courier_type == 'ARAMEX':
            return AramexCourier()
        elif courier_type == 'SMSA':
            return SmasCourier()
