# Generated by Django 3.1.6 on 2021-02-14 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planning', '0005_auto_20210214_1051'),
    ]

    operations = [
        migrations.AddField(
            model_name='planpoint',
            name='major',
            field=models.BooleanField(db_index=True, default=True),
        ),
    ]
