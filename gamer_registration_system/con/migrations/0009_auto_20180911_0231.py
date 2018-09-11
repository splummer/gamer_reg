# Generated by Django 2.0.8 on 2018-09-11 02:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('con', '0008_auto_20180909_1946'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Name')),
                ('key', models.CharField(max_length=4, unique=True, verbose_name='Short Name')),
                ('start_date', models.DateTimeField(verbose_name='Start time')),
                ('end_date', models.DateTimeField(verbose_name='End Time')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('convention', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='con.Convention')),
            ],
        ),
        migrations.AlterField(
            model_name='event',
            name='convention',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', related_query_name='event', to='con.Convention'),
        ),
        migrations.AlterField(
            model_name='eventschedule',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', related_query_name='schedule', to='con.Event'),
        ),
    ]