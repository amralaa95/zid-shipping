# from __future__ import annotations
from abc import ABC, abstractmethod
import uuid


class CourierFactory(ABC):

    @abstractmethod
    def create_order(self, **kwargs):
        pass

    @abstractmethod
    def retrive_status(self, tracking_id: str):
        pass

    def generate_tracking_id(self) -> str:
        return str(uuid.uuid4()).replace('-', '')

    def cancel_order(self, tracking_id: str):
        raise NotImplementedError('Cancel order not exist for this Courier')
