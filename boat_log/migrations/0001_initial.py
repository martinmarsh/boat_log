# Generated by Django 3.1.6 on 2021-02-11 22:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('passage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExchangeLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('directory', models.CharField(blank=True, default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='WeatherLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('when', models.DateTimeField()),
                ('wind_force', models.DecimalField(blank=True, decimal_places=0, max_digits=1, null=True)),
                ('wind_direction', models.DecimalField(blank=True, decimal_places=0, max_digits=3, null=True)),
                ('temperature', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True)),
                ('humidity', models.DecimalField(blank=True, decimal_places=0, max_digits=3, null=True)),
                ('pressure', models.DecimalField(blank=True, decimal_places=0, max_digits=4, null=True)),
                ('passage', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='passage.passage')),
            ],
        ),
        migrations.CreateModel(
            name='SeaLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('when', models.DateTimeField()),
                ('drift', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True)),
                ('set', models.DecimalField(blank=True, decimal_places=0, max_digits=3, null=True)),
                ('wave_ht', models.DecimalField(blank=True, decimal_places=0, max_digits=3, null=True)),
                ('wave_length', models.DecimalField(blank=True, decimal_places=0, max_digits=3, null=True)),
                ('swell', models.BooleanField(default=False)),
                ('sea', models.CharField(choices=[('BR', 'Breaking'), ('WT', 'White tops/ Foam '), ('RP', 'Ripples'), ('GY', 'Flat / Glassy'), ('UD', 'undefined')], default='UD', max_length=2, null=True)),
                ('passage', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='passage.passage')),
            ],
        ),
        migrations.CreateModel(
            name='GPXWriteFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gpx_file_name', models.CharField(max_length=150)),
                ('content', models.CharField(choices=[('AL', 'All Elements 9s Data Waypoints, Routes, Tracks'), ('WP', 'Waypoints OpenCPN/Element 9s'), ('RT', 'Plans and Plan Points OpenCPN/Element 9s'), ('TR', 'Tracks OpenCPN/Element 9s'), ('PA', 'Passage OpenCPN/Element 9s')], default='AL', max_length=2, null=True)),
                ('extensions', models.CharField(choices=[('NO', 'Add No Extensions'), ('OP', 'OpenCPN'), ('RA', 'Raymarine')], default='AL', max_length=2, null=True)),
                ('from_date', models.DateTimeField(blank=True, null=True)),
                ('write_time', models.DateTimeField(blank=True, null=True)),
                ('directory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boat_log.exchangelocation')),
            ],
        ),
        migrations.CreateModel(
            name='GPXReadFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gpx_file_name', models.CharField(max_length=150)),
                ('write_time', models.DateTimeField(blank=True, null=True)),
                ('directory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boat_log.exchangelocation')),
            ],
        ),
        migrations.CreateModel(
            name='EngineLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('when', models.DateTimeField()),
                ('eng_log', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('fuel_rate', models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True)),
                ('est_tank', models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True)),
                ('fuel_added', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('full_tank', models.BooleanField(default=False)),
                ('passage', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='passage.passage')),
            ],
        ),
    ]
