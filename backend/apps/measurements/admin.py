from django.contrib import admin
from .models import Measurement


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'timestamp', 'technology', 'latitude', 'longitude', 
        'download_rate', 'upload_rate', 'created_at'
    ]
    list_filter = ['technology', 'timestamp', 'created_at']
    search_fields = ['technology', 'plmn_id', 'frequency_band']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('timestamp', 'latitude', 'longitude', 'technology')
        }),
        ('Network Information', {
            'fields': ('plmn_id', 'lac', 'rac', 'tac', 'cell_id', 'frequency_band', 'arfcn')
        }),
        ('Signal Quality', {
            'fields': ('rsrp', 'rsrq', 'rscp', 'ec_no', 'rxlev')
        }),
        ('Performance Metrics', {
            'fields': ('download_rate', 'upload_rate', 'ping_response_time', 'dns_response_time', 'web_response_time', 'sms_delivery_time')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['-timestamp'] 