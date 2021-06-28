from django.db import models
from django.contrib.gis.db import models


class Sensors(models.Model):
    sensor_id = models.CharField(max_length=255, null=False)
    sensor_name = models.CharField(max_length=255, null=False)
    company = models.CharField(max_length=255, null=False)
    measured_quantity = models.CharField(max_length=255, null=False)
    geometry = models.PointField()
    calibration_interval = models.DateField()
    calibrated_on = models.DateField(auto_now_add=True)
    units = models.CharField(max_length=50)
    limit_min = models.FloatField()
    limit_max = models.FloatField()

    def __str__(self):
        return self.sensor_name


class MaintenanceActions(models.Model):
    label = models.CharField(max_length=255, null=False)
    value = models.CharField(max_length=255, null=False)
