from .dataclasses import *
from abc import ABC, abstractmethod
from typing import List


class AbstractMeasurementService(ABC):
    @abstractmethod
    def create_measurement(self, request: CreateMeasurementReq) -> MeasurementDTO:
        """
        Create a new measurement record.
        """
        raise NotImplementedError

    @abstractmethod
    def get_measurement(self, measurement_id: int) -> MeasurementDTO:
        """
        Get measurement data by ID.
        """
        raise NotImplementedError

    @abstractmethod
    def list_measurements(self, request: MeasurementListReq) -> MeasurementListResponse:
        """
        List measurements with optional filtering and pagination.
        """
        raise NotImplementedError

    @abstractmethod
    def bulk_create_measurements(self, request: BulkCreateMeasurementReq) -> BulkCreateMeasurementResponse:
        """
        Create multiple measurements in a single transaction.
        """
        raise NotImplementedError

    @abstractmethod
    def delete_measurement(self, measurement_id: int) -> bool:
        """
        Delete a measurement by ID.
        """
        raise NotImplementedError 