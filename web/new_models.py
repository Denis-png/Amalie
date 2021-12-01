# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
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
    sensor = models.ForeignKey('Sensors', models.DO_NOTHING, blank=True, null=True)
    variable = models.ForeignKey('Variables', models.DO_NOTHING, blank=True, null=True)

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


class Api(models.Model):
    id = models.BigAutoField(primary_key=True)
    connection_id = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    link = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'api'


class Condition(models.Model):
    id = models.BigAutoField(primary_key=True)
    start_date = models.DateField()
    start_time = models.TimeField()
    end_date = models.DateField()
    end_time = models.TimeField()
    condition = models.CharField(max_length=255)
    note = models.TextField(blank=True, null=True)
    sensor = models.ForeignKey('Sensors', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'condition'


class DataCleverfarm(models.Model):
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    value = models.FloatField(blank=True, null=True)
    sensor = models.ForeignKey('Sensors', models.DO_NOTHING, blank=True, null=True)
    variable = models.ForeignKey('Variables', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'data_Cleverfarm'


class DataEmsbrno(models.Model):
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    value = models.FloatField(blank=True, null=True)
    sensor = models.ForeignKey('Sensors', models.DO_NOTHING, blank=True, null=True)
    variable = models.ForeignKey('Variables', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'data_EMSBrno'


class DataEkotechnika(models.Model):
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    value = models.FloatField(blank=True, null=True)
    sensor = models.ForeignKey('Sensors', models.DO_NOTHING, blank=True, null=True)
    variable = models.ForeignKey('Variables', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'data_Ekotechnika'


class DataNone(models.Model):
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    value = models.FloatField(blank=True, null=True)
    sensor = models.ForeignKey('Sensors', models.DO_NOTHING, blank=True, null=True)
    variable = models.ForeignKey('Variables', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'data_None'


class DataTomst(models.Model):
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    value = models.FloatField(blank=True, null=True)
    sensor = models.ForeignKey('Sensors', models.DO_NOTHING, blank=True, null=True)
    variable = models.ForeignKey('Variables', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'data_Tomst'


class DataVrty(models.Model):
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    value = models.FloatField(blank=True, null=True)
    sensor = models.ForeignKey('Sensors', models.DO_NOTHING, blank=True, null=True)
    variable = models.ForeignKey('Variables', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'data_Vrty'


class Group(models.Model):
    id = models.BigAutoField(primary_key=True)
    group_id = models.CharField(max_length=255)
    price = models.FloatField(blank=True, null=True)
    connection_id = models.ForeignKey(Api, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'group'


class Maintenance(models.Model):
    id = models.BigAutoField(primary_key=True)
    date = models.DateField()
    time = models.TimeField()
    user = models.ForeignKey('People', models.DO_NOTHING, blank=True, null=True)
    action = models.CharField(max_length=255)
    note = models.TextField(blank=True, null=True)
    sensor = models.ForeignKey('Sensors', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'maintenance'


class Maintenanceactions(models.Model):
    id = models.BigAutoField(primary_key=True)
    label = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'maintenanceactions'


class People(models.Model):
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(unique=True, max_length=254)
    technician_czu = models.BooleanField()
    technician_company = models.BooleanField()
    sensor = models.ForeignKey('Sensors', models.DO_NOTHING, blank=True, null=True)
    sensor_type = models.ForeignKey('SensorType', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'people'


class Project(models.Model):
    id = models.BigAutoField(primary_key=True)
    project_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255, blank=True, null=True)
    investigator = models.CharField(max_length=255)
    link = models.CharField(max_length=1000, blank=True, null=True)
    identification_code = models.CharField(max_length=255, blank=True, null=True)
    license = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(People, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'project'


class SensorType(models.Model):
    id = models.BigAutoField(primary_key=True)
    sensor_type_id = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    calibration_interval = models.IntegerField()
    time_step = models.IntegerField()
    note_link = models.CharField(max_length=1000, blank=True, null=True)
    tech_doc_link = models.CharField(max_length=1000, blank=True, null=True)
    photos_link = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sensor_type'


class SensorVariable(models.Model):
    id = models.BigAutoField(primary_key=True)
    chip_id = models.CharField(max_length=255, blank=True, null=True)
    limit_value_min = models.FloatField()
    limit_value_max = models.FloatField()
    unit = models.CharField(max_length=255)
    vertical_floor = models.CharField(max_length=255)
    project = models.ForeignKey(Project, models.DO_NOTHING, blank=True, null=True)
    sensor = models.ForeignKey('Sensors', models.DO_NOTHING, blank=True, null=True)
    variable = models.ForeignKey('Variables', models.DO_NOTHING, blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sensor_variable'


class Sensors(models.Model):
    id = models.BigAutoField(primary_key=True)
    sensor_name = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=255)
    x = models.FloatField()
    y = models.FloatField()
    elevation = models.FloatField()
    price = models.FloatField(blank=True, null=True)
    connection = models.ForeignKey(Api, models.DO_NOTHING, blank=True, null=True)
    sensor_type = models.ForeignKey(SensorType, models.DO_NOTHING, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    spatial_precision = models.CharField(max_length=255)
    warranty = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'sensors'


class SensorsGroup(models.Model):
    id = models.BigAutoField(primary_key=True)
    group_id = models.CharField(max_length=255)
    price = models.FloatField()
    connection = models.ForeignKey(Api, models.DO_NOTHING, blank=True, null=True)
    sensor = models.ForeignKey(Sensors, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sensors_group'


class Variables(models.Model):
    id = models.BigAutoField(primary_key=True)
    variable_id = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'variables'
