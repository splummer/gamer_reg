# Generated by Django 2.0.8 on 2018-09-11 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('con', '0011_auto_20180911_0246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventschedule',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='End Time'),
        ),
        migrations.AlterField(
            model_name='eventschedule',
            name='room',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Room'),
        ),
        migrations.AlterField(
            model_name='eventschedule',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Start time'),
        ),
    ]
