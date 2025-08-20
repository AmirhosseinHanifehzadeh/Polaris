from rest_framework import viewsets, response, status
from rest_framework.decorators import action
from django.http import JsonResponse
from runner.bootstrap import get_bootstrapper
from . import interfaces


class MeasurementViewSet(viewsets.GenericViewSet):

    def create(self, request):
        """Create a single measurement"""
        service = get_bootstrapper().get_measurements_service()
        
        try:
            create_request = interfaces.CreateMeasurementReq(**request.data)
            result = service.create_measurement(request=create_request)
            return response.Response(result.model_dump(), status=status.HTTP_201_CREATED)
        except Exception as e:
            return response.Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        """Get a single measurement by ID"""
        service = get_bootstrapper().get_measurements_service()
        
        try:
            measurement_id = int(pk)
            result = service.get_measurement(measurement_id=measurement_id)
            return response.Response(result.model_dump())
        except (ValueError, interfaces.MeasurementNotFound):
            return response.Response(
                {"error": "Measurement not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

    def list(self, request):
        """List measurements with optional filtering"""
        service = get_bootstrapper().get_measurements_service()
        
        try:
            # Parse query parameters
            list_request = interfaces.MeasurementListReq(
                technology=request.query_params.get('technology'),
                start_date=request.query_params.get('start_date'),
                end_date=request.query_params.get('end_date'),
                limit=int(request.query_params.get('limit', 100)),
                offset=int(request.query_params.get('offset', 0))
            )
            
            result = service.list_measurements(request=list_request)
            return response.Response(result.model_dump())
        except Exception as e:
            return response.Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, pk=None):
        """Delete a measurement by ID"""
        service = get_bootstrapper().get_measurements_service()
        
        try:
            measurement_id = int(pk)
            service.delete_measurement(measurement_id=measurement_id)
            return response.Response(status=status.HTTP_204_NO_CONTENT)
        except (ValueError, interfaces.MeasurementNotFound):
            return response.Response(
                {"error": "Measurement not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """Create multiple measurements in bulk"""
        service = get_bootstrapper().get_measurements_service()
        
        try:
            bulk_request = interfaces.BulkCreateMeasurementReq(**request.data)
            result = service.bulk_create_measurements(request=bulk_request)
            return response.Response(result.model_dump(), status=status.HTTP_201_CREATED)
        except Exception as e:
            return response.Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            ) 