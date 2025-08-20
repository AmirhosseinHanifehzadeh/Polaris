import logging
from typing import List, Dict
from django.db import transaction
from .models import Measurement
from . import interfaces
from apps.accounts import interfaces as accounts_interfaces
from libs.redis_client import interfaces as cache_interfaces

logger = logging.getLogger(__name__)


class MeasurementService(interfaces.AbstractMeasurementService):
    def __init__(
            self,
            claim: accounts_interfaces.Session,
    ):
        self.claim = claim

    def create_measurement(self, request: interfaces.CreateMeasurementReq) -> interfaces.MeasurementDTO:
        logger.info(f"Creating measurement: {request}")
        
        try:
            measurement = Measurement.objects.create(
                timestamp=request.timestamp,
                latitude=request.latitude,
                longitude=request.longitude,
                technology=request.technology,
                plmn_id=request.plmn_id,
                lac=request.lac,
                rac=request.rac,
                tac=request.tac,
                cell_id=request.cell_id,
                frequency_band=request.frequency_band,
                arfcn=request.arfcn,
                rsrp=request.rsrp,
                rsrq=request.rsrq,
                rscp=request.rscp,
                ec_no=request.ec_no,
                rxlev=request.rxlev,
                download_rate=request.download_rate,
                upload_rate=request.upload_rate,
                ping_response_time=request.ping_response_time,
                dns_response_time=request.dns_response_time,
                web_response_time=request.web_response_time,
                sms_delivery_time=request.sms_delivery_time
            )
            
            result = self._convert_measurement_to_dataclass(measurement)
            logger.info(f"Created measurement with ID: {result.id}")
            return result
            
        except Exception as e:
            logger.error(f"Error creating measurement: {e}")
            raise interfaces.BadRequestRoot()

    def get_measurement(self, measurement_id: int) -> interfaces.MeasurementDTO:
        logger.info(f"Getting measurement with ID: {measurement_id}")
        
        try:
            measurement = Measurement.objects.get(id=measurement_id)
            result = self._convert_measurement_to_dataclass(measurement)
            logger.info(f"Retrieved measurement: {result}")
            return result
        except Measurement.DoesNotExist:
            logger.debug(f"Measurement with ID {measurement_id} doesn't exist")
            raise interfaces.MeasurementNotFound()

    def list_measurements(self, request: interfaces.MeasurementListReq) -> interfaces.MeasurementListResponse:
        logger.info(f"Listing measurements with filters: {request}")
        
        queryset = Measurement.objects.all()
        
        # Apply filters
        if request.technology:
            queryset = queryset.filter(technology=request.technology)
        
        if request.start_date:
            queryset = queryset.filter(timestamp__gte=request.start_date)
        
        if request.end_date:
            queryset = queryset.filter(timestamp__lte=request.end_date)
        
        # Get total count
        total_count = queryset.count()
        
        # Apply pagination
        measurements = queryset[request.offset:request.offset + request.limit]
        
        # Convert to DTOs
        results = [self._convert_measurement_to_dataclass(m) for m in measurements]
        
        response = interfaces.MeasurementListResponse(
            count=total_count,
            results=results
        )
        
        logger.info(f"Retrieved {len(results)} measurements out of {total_count} total")
        return response

    def bulk_create_measurements(self, request: interfaces.BulkCreateMeasurementReq) -> interfaces.BulkCreateMeasurementResponse:
        logger.info(f"Bulk creating {len(request.measurements)} measurements")
        
        try:
            with transaction.atomic():
                created_measurements = []
                
                for measurement_data in request.measurements:
                    measurement = Measurement.objects.create(
                        timestamp=measurement_data.timestamp,
                        latitude=measurement_data.latitude,
                        longitude=measurement_data.longitude,
                        technology=measurement_data.technology,
                        plmn_id=measurement_data.plmn_id,
                        lac=measurement_data.lac,
                        rac=measurement_data.rac,
                        tac=measurement_data.tac,
                        cell_id=measurement_data.cell_id,
                        frequency_band=measurement_data.frequency_band,
                        arfcn=measurement_data.arfcn,
                        rsrp=measurement_data.rsrp,
                        rsrq=measurement_data.rsrq,
                        rscp=measurement_data.rscp,
                        ec_no=measurement_data.ec_no,
                        rxlev=measurement_data.rxlev,
                        download_rate=measurement_data.download_rate,
                        upload_rate=measurement_data.upload_rate,
                        ping_response_time=measurement_data.ping_response_time,
                        dns_response_time=measurement_data.dns_response_time,
                        web_response_time=measurement_data.web_response_time,
                        sms_delivery_time=measurement_data.sms_delivery_time
                    )
                    created_measurements.append(measurement)
                
                results = [self._convert_measurement_to_dataclass(m) for m in created_measurements]
                
                response = interfaces.BulkCreateMeasurementResponse(
                    created_count=len(results),
                    results=results
                )
                
                logger.info(f"Successfully created {len(results)} measurements")
                return response
                
        except Exception as e:
            logger.error(f"Error in bulk create: {e}")
            raise interfaces.BulkCreateError()

    def delete_measurement(self, measurement_id: int) -> bool:
        logger.info(f"Deleting measurement with ID: {measurement_id}")
        
        try:
            measurement = Measurement.objects.get(id=measurement_id)
            measurement.delete()
            logger.info(f"Successfully deleted measurement with ID: {measurement_id}")
            return True
        except Measurement.DoesNotExist:
            logger.debug(f"Measurement with ID {measurement_id} doesn't exist")
            raise interfaces.MeasurementNotFound()

    @staticmethod
    def _convert_measurement_to_dataclass(measurement: Measurement) -> interfaces.MeasurementDTO:
        return interfaces.MeasurementDTO(
            id=measurement.id,
            timestamp=measurement.timestamp,
            latitude=measurement.latitude,
            longitude=measurement.longitude,
            technology=measurement.technology,
            plmn_id=measurement.plmn_id,
            lac=measurement.lac,
            rac=measurement.rac,
            tac=measurement.tac,
            cell_id=measurement.cell_id,
            frequency_band=measurement.frequency_band,
            arfcn=measurement.arfcn,
            rsrp=measurement.rsrp,
            rsrq=measurement.rsrq,
            rscp=measurement.rscp,
            ec_no=measurement.ec_no,
            rxlev=measurement.rxlev,
            download_rate=measurement.download_rate,
            upload_rate=measurement.upload_rate,
            ping_response_time=measurement.ping_response_time,
            dns_response_time=measurement.dns_response_time,
            web_response_time=measurement.web_response_time,
            sms_delivery_time=measurement.sms_delivery_time,
            created_at=measurement.created_at,
            updated_at=measurement.updated_at
        ) 