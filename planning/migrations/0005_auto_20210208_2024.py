# Generated by Django 3.1.6 on 2021-02-08 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planning', '0004_auto_20210208_1958'),
    ]

    operations = [
        migrations.RenameField(
            model_name='planpoint',
            old_name='eta',
            new_name='time',
        ),
        migrations.AddField(
            model_name='planpoint',
            name='name',
            field=models.CharField(blank=True, default='', max_length=150),
        ),
        migrations.AddField(
            model_name='planpoint',
            name='type',
            field=models.CharField(blank=True, default='WPT', max_length=10),
        ),
    ]
