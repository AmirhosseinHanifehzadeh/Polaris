from django.db import models


class Measurement(models.Model):
    timestamp = models.DateTimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    technology = models.CharField(max_length=10)  # LTE, GSM, etc.
    plmn_id = models.CharField(max_length=10, blank=True, null=True)
    lac = models.IntegerField(blank=True, null=True)
    rac = models.IntegerField(blank=True, null=True)
    tac = models.IntegerField(blank=True, null=True)
    cell_id = models.IntegerField(blank=True, null=True)
    frequency_band = models.CharField(max_length=20, blank=True, null=True)
    arfcn = models.IntegerField(blank=True, null=True)
    rsrp = models.FloatField(blank=True, null=True)  # Reference Signal Received Power (dBm)
    rsrq = models.FloatField(blank=True, null=True)  # Reference Signal Received Quality (dB)
    rscp = models.FloatField(blank=True, null=True)  # Received Signal Code Power (dBm)
    ec_no = models.FloatField(blank=True, null=True)  # Ec/N0 (dB)
    rxlev = models.FloatField(blank=True, null=True)  # RxLev (dBm)
    download_rate = models.FloatField(blank=True, null=True)  # Mbps
    upload_rate = models.FloatField(blank=True, null=True)  # Mbps
    ping_response_time = models.FloatField(blank=True, null=True)  # ms
    dns_response_time = models.FloatField(blank=True, null=True)  # ms
    web_response_time = models.FloatField(blank=True, null=True)  # ms
    sms_delivery_time = models.FloatField(blank=True, null=True)  # seconds

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'measurements'
        ordering = ['-timestamp']

    def __str__(self):
        return f"Measurement at {self.timestamp} - {self.technology} - Lat: {self.latitude}, Lon: {self.longitude}" 