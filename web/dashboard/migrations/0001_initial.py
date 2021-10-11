# Generated by Django 3.2.8 on 2021-10-11 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Api',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('connection_id', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=255)),
                ('link', models.CharField(blank=True, max_length=1000, null=True)),
            ],
            options={
                'db_table': 'api',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('start_date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_date', models.DateField()),
                ('end_time', models.TimeField()),
                ('condition', models.CharField(max_length=255)),
                ('note', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'condition',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('group_id', models.CharField(max_length=255)),
                ('price', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Maintenance',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('action', models.CharField(max_length=255)),
                ('note', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'maintenance',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Maintenanceactions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('label', models.CharField(max_length=255)),
                ('value', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'maintenanceactions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='People',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=254, unique=True)),
                ('technician_czu', models.BooleanField()),
                ('technician_company', models.BooleanField()),
            ],
            options={
                'db_table': 'people',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('project_id', models.CharField(max_length=255)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('investigator', models.CharField(max_length=255)),
                ('link', models.CharField(blank=True, max_length=1000, null=True)),
                ('identification_code', models.CharField(blank=True, max_length=255, null=True)),
                ('license', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'project',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Sensors',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('sensor_name', models.CharField(max_length=255)),
                ('serial_number', models.CharField(max_length=255)),
                ('x', models.FloatField()),
                ('y', models.FloatField()),
                ('elevation', models.FloatField()),
                ('price', models.FloatField(blank=True, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('spatial_precision', models.CharField(max_length=255)),
                ('warranty', models.DateTimeField()),
            ],
            options={
                'db_table': 'sensors',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SensorsGroup',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('group_id', models.CharField(max_length=255)),
                ('price', models.FloatField()),
            ],
            options={
                'db_table': 'sensors_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SensorType',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('sensor_type_id', models.CharField(max_length=255)),
                ('company', models.CharField(max_length=255)),
                ('calibration_interval', models.IntegerField()),
                ('time_step', models.IntegerField()),
                ('note_link', models.CharField(blank=True, max_length=1000, null=True)),
                ('tech_doc_link', models.CharField(blank=True, max_length=1000, null=True)),
                ('photos_link', models.CharField(blank=True, max_length=1000, null=True)),
            ],
            options={
                'db_table': 'sensor_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SensorVariable',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('chip_id', models.CharField(blank=True, max_length=255, null=True)),
                ('limit_value_min', models.FloatField()),
                ('limit_value_max', models.FloatField()),
                ('unit', models.CharField(max_length=255)),
                ('vertical_floor', models.CharField(max_length=255)),
                ('note', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'sensor_variable',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Variables',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('variable_id', models.CharField(blank=True, max_length=255, null=True)),
                ('name', models.CharField(max_length=255)),
                ('note', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'variables',
                'managed': False,
            },
        ),
    ]