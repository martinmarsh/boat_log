# Generated by Django 3.1.6 on 2021-02-09 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boat_log', '0002_gpxwritefile_extensions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gpxwritefile',
            name='content',
            field=models.CharField(choices=[('AL', 'All Elements 9s Data Waypoints, Routes, Tracks'), ('WP', 'Waypoints OpenCPN/Element 9s'), ('RT', 'Plans and Plan Points OpenCPN/Element 9s'), ('TR', 'Tracks OpenCPN/Element 9s')], default='AL', max_length=2, null=True),
        ),
    ]
