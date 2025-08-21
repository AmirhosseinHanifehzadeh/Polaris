import logging
import os
from apps.measurements.services import MeasurementService
from apps.measurements import interfaces as measurement_interfaces

logger = logging.getLogger(__name__)


class Bootstrapper:
    def __new__(cls, *args, **kwargs):
        logger.info("new method of bootstrap")
        if not hasattr(cls, 'instance') or kwargs.get('force_recreate', False):
            logger.info("create a new bootstrap")
            cls.instance = super(Bootstrapper, cls).__new__(cls)
        return cls.instance

    def __init__(self, **kwargs) -> None:
        self._measurements_service = MeasurementService()

    def get_measurements_service(self) -> measurement_interfaces.AbstractMeasurementService:
        """Get measurements service instance"""
        # For now, return a simple instance without dependencies
        # In a real implementation, you would inject dependencies like cache service
        return self._measurements_service


def get_bootstrapper(**kwargs) -> Bootstrapper:
        bootstrapper = Bootstrapper(**kwargs)
        return bootstrapper
