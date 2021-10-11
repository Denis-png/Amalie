from django.contrib.gis.db import models


class Humidity(models.Model):
    date = models.DateField()
    time = models.TimeField()
    value = models.FloatField(blank=True, null=True)
    signal = models.CharField(max_length=200)
    sensor_id = models.IntegerField(blank=True, null=True)
    variable_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'HUMIDITY'


class LeafWetness(models.Model):
    date = models.DateField()
    time = models.TimeField()
    value = models.FloatField(blank=True, null=True)
    signal = models.CharField(max_length=200)
    sensor_id = models.IntegerField(blank=True, null=True)
    variable_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'LEAF_WETNESS'


class Pressure(models.Model):
    date = models.DateField()
    time = models.TimeField()
    value = models.FloatField(blank=True, null=True)
    signal = models.CharField(max_length=200)
    sensor_id = models.IntegerField(blank=True, null=True)
    variable_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'PRESSURE'


class Rainfall(models.Model):
    date = models.DateField()
    time = models.TimeField()
    value = models.FloatField(blank=True, null=True)
    signal = models.CharField(max_length=200)
    sensor_id = models.IntegerField(blank=True, null=True)
    variable_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'RAINFALL'


class Resistance(models.Model):
    id = models.BigAutoField(primary_key=True)
    date = models.DateField()
    time = models.TimeField()
    value = models.FloatField(blank=True, null=True)
    signal = models.CharField(max_length=200)
    sensor_id = models.IntegerField(blank=True, null=True)
    variable_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'RESISTANCE'


class Swp(models.Model):
    date = models.DateField()
    time = models.TimeField()
    value = models.FloatField(blank=True, null=True)
    signal = models.CharField(max_length=200)
    sensor_id = models.IntegerField(blank=True, null=True)
    variable_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'SWP'


class Temperature(models.Model):
    date = models.DateField()
    time = models.TimeField()
    value = models.FloatField(blank=True, null=True)
    signal = models.CharField(max_length=200)
    sensor_id = models.IntegerField(blank=True, null=True)
    variable_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'TEMPERATURE'


class WindDirection(models.Model):
    date = models.DateField()
    time = models.TimeField()
    value = models.FloatField(blank=True, null=True)
    signal = models.CharField(max_length=200)
    sensor_id = models.IntegerField(blank=True, null=True)
    variable_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'WIND_DIRECTION'


class WindGust(models.Model):
    date = models.DateField()
    time = models.TimeField()
    value = models.FloatField(blank=True, null=True)
    signal = models.CharField(max_length=200)
    sensor_id = models.IntegerField(blank=True, null=True)
    variable_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'WIND_GUST'


class WindSpeed(models.Model):
    date = models.DateField()
    time = models.TimeField()
    value = models.FloatField(blank=True, null=True)
    signal = models.CharField(max_length=200)
    sensor_id = models.IntegerField(blank=True, null=True)
    variable_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'WIND_SPEED'