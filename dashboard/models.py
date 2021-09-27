from django.db import models
from django.contrib.gis.db import models
from datetime import datetime


class API(models.Model):
    connection_id = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    link = models.CharField(max_length=1000, null=True)


class Variables(models.Model):
    variable_id = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255)
    note = models.TextField(null=True)


class Group(models.Model):
    group_id = models.CharField(max_length=255)
    price = models.FloatField(null=True)
    connection_id = models.ForeignKey(API, on_delete=models.RESTRICT, null=True)



class SensorType(models.Model):
    sensor_type_id = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    calibration_interval = models.IntegerField()
    time_step = models.IntegerField()
    note_link = models.CharField(max_length=1000, null=True)
    tech_doc_link = models.CharField(max_length=1000, null=True)
    photos_link = models.CharField(max_length=1000, null=True)


def auto_sensor_id():
    last_element = Sensors.objects.using('global').all().order_by('id').last()
    head = ''
    if not last_element:
        return '0001'
    new_element = int(last_element) + 1
    zero_count = 4 - len(str(new_element))
    for zero in zero_count:
        head = head + '0'
    if len(head) > 0:
        result = head + str(new_element)
        return result


class Sensors(models.Model):
    sensor_type = models.ForeignKey(SensorType, on_delete=models.RESTRICT, null=True)
    sensor_name = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=255)
    x = models.FloatField()
    y = models.FloatField()
    elevation = models.FloatField()
    spatial_precision = models.CharField(max_length=255, default='blank')
    price = models.FloatField(null=True)
    warranty = models.DateTimeField(default=datetime.now, blank=True)
    connection = models.ForeignKey(API, on_delete=models.RESTRICT, null=True)
    note = models.TextField(null=True)


class SensorsGroup(models.Model):
    group_id = models.CharField(max_length=255)
    sensor = models.ForeignKey(Sensors, on_delete=models.SET_NULL, null=True)
    price = models.FloatField()
    connection = models.ForeignKey(API, on_delete=models.RESTRICT, null=True)


class SensorGroup(models.Model):
    sensor = models.ForeignKey(Sensors, on_delete=models.SET_NULL, null=True)
    group = models.ForeignKey(Group, on_delete=models.RESTRICT, null=True)


class People(models.Model):
    sensor_type = models.ForeignKey(SensorType, on_delete=models.SET_NULL, null=True, related_name='sensor_type')
    sensor = models.ForeignKey(Sensors, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    technician_czu = models.BooleanField()
    technician_company = models.BooleanField()


class Project(models.Model):
    project_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255, null=True)
    investigator = models.CharField(max_length=255)
    link = models.CharField(max_length=1000, null=True)
    identification_code = models.CharField(max_length=255, null=True)
    license = models.CharField(max_length=255, null=True)
    user = models.ForeignKey(People, on_delete=models.SET_NULL, null=True)


class SensorVariable(models.Model):
    sensor = models.ForeignKey(Sensors, on_delete=models.SET_NULL, null=True, editable=False)
    variable = models.ForeignKey(Variables, on_delete=models.SET_NULL, null=True)
    chip_id = models.CharField(max_length=255, null=True)
    project = models.ForeignKey(Project, on_delete=models.RESTRICT, null=True)
    limit_value_min = models.FloatField()
    limit_value_max = models.FloatField()
    unit = models.CharField(max_length=255)
    vertical_floor = models.CharField(max_length=255)
    note = models.TextField(null=True)


class Maintenance(models.Model):
    sensor = models.ForeignKey(Sensors, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    time = models.TimeField()
    user = models.ForeignKey(People, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255)
    note = models.TextField(null=True)


class Condition(models.Model):
    sensor = models.ForeignKey(Sensors, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField(auto_now=True)
    start_time = models.TimeField(auto_now=True)
    end_date = models.DateField(auto_now_add=True)
    end_time = models.TimeField(auto_now_add=True)
    condition = models.CharField(max_length=255)
    note = models.TextField(null=True)


class MaintenanceActions(models.Model):
    label = models.CharField(max_length=255, null=False)
    value = models.CharField(max_length=255, null=False)

