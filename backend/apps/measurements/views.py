from rest_framework import viewsets, response, status
from rest_framework.decorators import action
from django.http import JsonResponse
import logging
from runner.bootstrap import get_bootstrapper
from . import interfaces

logger = logging.getLogger(__name__)

class MeasurementViewSet(viewsets.GenericViewSet):

    def create(self, request):
        """Create a single measurement"""
        logger.info(f"Processing create request with data: {request.data}")
        service = get_bootstrapper().get_measurements_service()
        
        try:
            create_request = interfaces.CreateMeasurementReq(**request.data)
            result = service.create_measurement(request=create_request)
            logger.info(f"Successfully created measurement with ID: {result.id}")
            return response.Response(result.model_dump(), status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error creating measurement: {str(e)}")
            return response.Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        """Get a single measurement by ID"""
        logger.info(f"Processing retrieve request for measurement ID: {pk}")
        service = get_bootstrapper().get_measurements_service()
        
        try:
            measurement_id = int(pk)
            result = service.get_measurement(measurement_id=measurement_id)
            logger.info(f"Successfully retrieved measurement with ID: {measurement_id}")
            return response.Response(result.model_dump())
        except (ValueError, interfaces.MeasurementNotFound):
            logger.warning(f"Measurement with ID {pk} not found")
            return response.Response(
                {"error": "Measurement not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

    def list(self, request):
        """List measurements with optional filtering"""
        logger.info(f"Processing list request with params: {dict(request.query_params)}")
        service = get_bootstrapper().get_measurements_service()
        
        try:
            # Parse query parameters
            start_date_str = request.query_params.get('start_date')
            end_date_str = request.query_params.get('end_date')
            
            # Parse datetime strings if provided
            start_date = None
            end_date = None
            
            if start_date_str:
                try:
                    from datetime import datetime
                    start_date = datetime.fromisoformat(start_date_str.replace('Z', '+00:00'))
                    logger.debug(f"Parsed start_date: {start_date}")
                except ValueError:
                    logger.error(f"Invalid start_date format: {start_date_str}")
                    return response.Response(
                        {"error": "Invalid start_date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            if end_date_str:
                try:
                    from datetime import datetime
                    end_date = datetime.fromisoformat(end_date_str.replace('Z', '+00:00'))
                    logger.debug(f"Parsed end_date: {end_date}")
                except ValueError:
                    logger.error(f"Invalid end_date format: {end_date_str}")
                    return response.Response(
                        {"error": "Invalid end_date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            list_request = interfaces.MeasurementListReq(
                technology=request.query_params.get('technology'),
                start_date=start_date,
                end_date=end_date,
                limit=int(request.query_params.get('limit', 100)),
                offset=int(request.query_params.get('offset', 0))
            )
            
            logger.debug(f"Executing list_measurements with filters: technology={list_request.technology}, start_date={list_request.start_date}, end_date={list_request.end_date}, limit={list_request.limit}, offset={list_request.offset}")
            
            result = service.list_measurements(request=list_request)
            logger.info(f"Successfully retrieved {len(result.results)} measurements out of {result.count} total")
            return response.Response(result.model_dump())
        except ValueError as e:
            logger.error(f"Invalid parameter in list request: {str(e)}")
            return response.Response(
                {"error": f"Invalid parameter: {str(e)}"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error in list request: {str(e)}")
            return response.Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, pk=None):
        """Delete a measurement by ID"""
        logger.info(f"Processing delete request for measurement ID: {pk}")
        service = get_bootstrapper().get_measurements_service()
        
        try:
            measurement_id = int(pk)
            service.delete_measurement(measurement_id=measurement_id)
            logger.info(f"Successfully deleted measurement with ID: {measurement_id}")
            return response.Response(status=status.HTTP_204_NO_CONTENT)
        except (ValueError, interfaces.MeasurementNotFound):
            logger.warning(f"Measurement with ID {pk} not found for deletion")
            return response.Response(
                {"error": "Measurement not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """Create multiple measurements in bulk"""
        logger.info(f"Processing bulk create request with {len(request.data.get('measurements', []))} measurements")
        service = get_bootstrapper().get_measurements_service()
        
        try:
            bulk_request = interfaces.BulkCreateMeasurementReq(**request.data)
            result = service.bulk_create_measurements(request=bulk_request)
            logger.info(f"Successfully created {result.created_count} measurements in bulk")
            return response.Response(result.model_dump(), status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error in bulk create request: {str(e)}")
            return response.Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            ) 