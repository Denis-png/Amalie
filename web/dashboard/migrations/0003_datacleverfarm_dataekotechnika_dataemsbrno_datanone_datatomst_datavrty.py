# Generated by Django 3.2.8 on 2021-11-18 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_data_humidity_data_leafwetness_data_pressure_data_rainfall_data_resistance_data_swp_data_temperature'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataCleverfarm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('time', models.TimeField(blank=True, null=True)),
                ('value', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'data_Cleverfarm',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DataEkotechnika',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('time', models.TimeField(blank=True, null=True)),
                ('value', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'data_Ekotechnika',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DataEmsbrno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('time', models.TimeField(blank=True, null=True)),
                ('value', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'data_EMSBrno',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DataNone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('time', models.TimeField(blank=True, null=True)),
                ('value', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'data_None',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DataTomst',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('time', models.TimeField(blank=True, null=True)),
                ('value', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'data_Tomst',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DataVrty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('time', models.TimeField(blank=True, null=True)),
                ('value', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'data_Vrty',
                'managed': False,
            },
        ),
    ]