from django.db import models
from django.contrib.gis.db import models


class Sensors(models.Model):
    sensor_id = models.CharField(max_length=255, null=False)
    sensor_name = models.CharField(max_length=255, null=False)
    company = models.CharField(max_length=255, null=False)
    measured_quantity = models.TextField(max_length=255, null=False)
    geometry = models.PointField(null=True)
    calibration_interval = models.IntegerField()
    calibrated_on = models.DateField(auto_now_add=True)
    units = models.TextField(max_length=50)
    limit_min = models.FloatField(null=True)
    limit_max = models.FloatField(null=True)

    def __str__(self):
        return self.sensor_name


class MaintenanceActions(models.Model):
    label = models.CharField(max_length=255, null=False)
    value = models.CharField(max_length=255, null=False)
