# from __future__ import annotations
from abc import ABC, abstractmethod
import uuid


class CourierFactory(ABC):

    @abstractmethod
    def create_order(self, **kwargs):
        pass

    @abstractmethod
    def retrive_status(self, tracking_id):
        pass

    def generate_tracking_id(self):
        return str(uuid.uuid4()).replace('-', '')


class Cancallable(ABC):  # this class for the couriers that wants to cancel thier orders so they use it

    def cancel_order(self, tracking_id):
        pass
