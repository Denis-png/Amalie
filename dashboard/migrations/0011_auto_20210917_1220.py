# Generated by Django 3.2.4 on 2021-09-17 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_auto_20210914_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maintenance',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='time',
            field=models.TimeField(),
        ),
    ]