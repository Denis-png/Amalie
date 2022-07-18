# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Companies(models.Model):
    name = models.CharField(max_length=-1)
    contact = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'companies'


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


class DataBluebeatle(models.Model):
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    value = models.FloatField(blank=True, null=True)
    sensor = models.ForeignKey('Sensors', models.DO_NOTHING, blank=True, null=True)
    variable = models.ForeignKey('Variables', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'data_BlueBeatle'


class DataCleverfarm(models.Model):
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    value = models.FloatField(blank=True, null=True)
    sensor = models.ForeignKey('Sensors', models.DO_NOTHING, blank=True, null=True)
    variable = models.ForeignKey('Variables', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'data_Cleverfarm'


class DataEkotechnika(models.Model):
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    value = models.FloatField(blank=True, null=True)
    sensor = models.ForeignKey('Sensors', models.DO_NOTHING, blank=True, null=True)
    variable = models.ForeignKey('Variables', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'data_Ekotechnika'


class DataEmsbrno(models.Model):
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    value = models.FloatField(blank=True, null=True)
    sensor = models.ForeignKey('Sensors', models.DO_NOTHING, blank=True, null=True)
    variable = models.ForeignKey('Variables', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'data_Emsbrno'


class DataTomst(models.Model):
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    value = models.FloatField(blank=True, null=True)
    sensor = models.ForeignKey('Sensors', models.DO_NOTHING, blank=True, null=True)
    variable = models.ForeignKey('Variables', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'data_Tomst'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


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
    sensor_type_id = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'people'


class Sensors(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    serial = models.CharField(max_length=255)
    company = models.ForeignKey(Companies, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sensors'


class SummaryStats(models.Model):
    company = models.ForeignKey(Companies, models.DO_NOTHING, blank=True, null=True)
    variable = models.ForeignKey('Variables', models.DO_NOTHING, blank=True, null=True)
    mean = models.FloatField(blank=True, null=True)
    median = models.FloatField(blank=True, null=True)
    std = models.FloatField(blank=True, null=True)
    max = models.FloatField(blank=True, null=True)
    min = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'summary_stats'


class Variables(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    company = models.ForeignKey(Companies, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'variables'
