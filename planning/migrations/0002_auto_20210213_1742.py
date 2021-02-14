# Generated by Django 3.1.6 on 2021-02-13 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planning', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='planpoint',
            name='merc_lat',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='planpoint',
            name='merc_long',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='planpoint',
            name='str_lat',
            field=models.CharField(blank=True, default='', max_length=150),
        ),
        migrations.AddField(
            model_name='planpoint',
            name='str_long',
            field=models.CharField(blank=True, default='', max_length=150),
        ),
    ]
