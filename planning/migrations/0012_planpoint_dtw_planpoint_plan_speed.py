# Generated by Django 4.0.3 on 2022-04-06 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planning', '0011_auto_20210223_0014'),
    ]

    operations = [
        migrations.AddField(
            model_name='planpoint',
            name='dtw',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
        migrations.AddField(
            model_name='planpoint',
            name='plan_speed',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True),
        ),
    ]
