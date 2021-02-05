# Generated by Django 3.1.6 on 2021-02-05 01:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('planning', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Passage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('start_from', models.CharField(max_length=200)),
                ('to', models.CharField(blank=True, default='', max_length=200)),
                ('towards', models.CharField(blank=True, default='', max_length=200)),
                ('narrative', models.TextField(blank=True, default='')),
                ('weather', models.TextField(blank=True, default='')),
                ('gpx_source_file', models.CharField(blank=True, default='', max_length=180)),
                ('maintenance', models.TextField(blank=True, default='')),
                ('max_wind_force', models.DecimalField(blank=True, decimal_places=0, max_digits=1, null=True)),
                ('max_wind_direction', models.DecimalField(blank=True, decimal_places=0, max_digits=3, null=True)),
                ('min_wind_force', models.DecimalField(blank=True, decimal_places=0, max_digits=1, null=True)),
                ('distance', models.DecimalField(blank=True, decimal_places=1, max_digits=7, null=True)),
                ('fuel_used', models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True)),
                ('day_hrs', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True)),
                ('night_hrs', models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True)),
                ('plan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='planning.plan')),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=150)),
                ('gpx_source_file', models.CharField(blank=True, default='', max_length=180)),
                ('gpx_track_name', models.CharField(blank=True, default='', max_length=150)),
                ('passage', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='passage.passage')),
            ],
        ),
        migrations.CreateModel(
            name='TrackPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.DecimalField(blank=True, decimal_places=0, max_digits=6, null=True)),
                ('segment', models.DecimalField(blank=True, decimal_places=0, max_digits=3, null=True)),
                ('seg_num', models.DecimalField(blank=True, decimal_places=0, max_digits=4, null=True)),
                ('lat', models.FloatField(blank=True, null=True)),
                ('long', models.FloatField(blank=True, null=True)),
                ('depth', models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True)),
                ('track', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='passage.track')),
            ],
        ),
        migrations.CreateModel(
            name='TideLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('when', models.DateTimeField()),
                ('HW', models.DateTimeField()),
                ('LW', models.DateTimeField()),
                ('port', models.CharField(blank=True, default='', max_length=100)),
                ('spring_neap_percent', models.DecimalField(blank=True, decimal_places=0, max_digits=2, null=True)),
                ('passage', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='passage.passage')),
            ],
        ),
        migrations.CreateModel(
            name='SailLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('when', models.DateTimeField()),
                ('wind_side', models.CharField(choices=[('p', 'port'), ('s', 'starboard'), ('a', 'stern/aft'), ('u', 'unknown')], default='u', max_length=1, null=True)),
                ('wind_force', models.DecimalField(blank=True, decimal_places=0, max_digits=1, null=True)),
                ('wind_direction', models.DecimalField(blank=True, decimal_places=0, max_digits=3, null=True)),
                ('sail_plan', models.CharField(choices=[('FS', 'Full Sail'), ('A1', 'All sails reef 1'), ('A2', 'All sails reef 1'), ('A3', 'All sails reef 3'), ('MF', 'Only Main Full'), ('M1', 'Only Main Reef 1'), ('M2', 'Only Main Reef 2'), ('M3', 'Only Main Reef 3'), ('GF', 'only Full Genoa'), ('G1', 'only Genoa reef 1'), ('G2', 'only Genoa reef 2'), ('G3', 'only Genoa reef 3'), ('NN', 'no sails')], default='NN', max_length=2, null=True)),
                ('spinnaker', models.BooleanField(default=False)),
                ('cruising_shoot', models.BooleanField(default=False)),
                ('passage', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='passage.passage')),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('when', models.DateTimeField()),
                ('narrative', models.TextField(blank=True, default='')),
                ('lat', models.FloatField(blank=True, null=True)),
                ('long', models.FloatField(blank=True, null=True)),
                ('log', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('course', models.DecimalField(blank=True, decimal_places=0, max_digits=3, null=True)),
                ('speed', models.DecimalField(blank=True, decimal_places=0, max_digits=3, null=True)),
                ('sog', models.DecimalField(blank=True, decimal_places=0, max_digits=3, null=True)),
                ('cog', models.DecimalField(blank=True, decimal_places=0, max_digits=3, null=True)),
                ('status', models.CharField(choices=[('MB', 'Moored/Berthed'), ('UW', 'under way'), ('ME', 'main engine'), ('UT', 'under tow'), ('TV', 'towing vessel'), ('AD', 'adrift'), ('AA', 'at anchor'), ('AG', 'aground'), ('HT', 'heaved too'), ('MS', 'Motor Sailing'), ('II', 'In Irons'), ('CH', 'Close Hauled'), ('CR', 'Close Reach'), ('BB', 'Beam Reach'), ('BR', 'Broad Reach'), ('RU', 'running under sail')], default='MB', max_length=2, null=True)),
                ('passage', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='passage.passage')),
            ],
        ),
        migrations.CreateModel(
            name='FixLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('when', models.DateTimeField()),
                ('lat', models.FloatField(blank=True, null=True)),
                ('long', models.FloatField(blank=True, null=True)),
                ('depth', models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True)),
                ('by', models.CharField(blank=True, default='GPS', max_length=20)),
                ('passage', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='passage.passage')),
            ],
        ),
        migrations.CreateModel(
            name='DepthLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('when', models.DateTimeField()),
                ('depth', models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True)),
                ('lat', models.FloatField(blank=True, null=True)),
                ('long', models.FloatField(blank=True, null=True)),
                ('tide', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='passage.tidelog')),
            ],
        ),
    ]
