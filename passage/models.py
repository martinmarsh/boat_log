from django.db import models
from planning.models import Plan


class Passage(models.Model):
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    start_from = models.CharField(max_length=200)
    to = models.CharField(max_length=200, blank=True, default="")
    towards = models.CharField(max_length=200, blank=True, default='')
    narrative = models.TextField(blank=True, default='')
    weather = models.TextField(blank=True, default='')
    gpx_source_file = models.CharField(max_length=180, blank=True, default="")
    maintenance = models.TextField(blank=True, default='')
    max_wind_force = models.DecimalField(max_digits=1, decimal_places=0, blank=True, null=True)
    max_wind_direction = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    min_wind_force = models.DecimalField(max_digits=1, decimal_places=0, blank=True, null=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, blank=True, null=True)
    distance = models.DecimalField(max_digits=7, decimal_places=1, blank=True, null=True)
    fuel_used = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    day_hrs = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    night_hrs = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)

    def __str__(self):
        return f'{self.start_from} to {self.to} on {self.start_time}'


class SailLog(models.Model):
    PORT = 'p'
    STARBOARD = 's'
    STERN = 'a'
    UNKNOWN = 'u'
    tack = [  # Wind side
        (PORT, 'port'),
        (STARBOARD, 'starboard'),
        (STERN, 'stern/aft'),
        (UNKNOWN, 'unknown')
    ]
    FULL_SAIL = 'FS'
    ALL_SAILS_REEF_1 = 'A1'
    ALL_SAILS_REEF_2 = 'A2'
    ALL_SAILS_REEF_3 = 'A3'
    FULL_MAIN_ONLY = 'MF'
    NO_SAILS = 'NN'
    MAIN_REEF1 = 'M1'
    MAIN_REEF2 = 'M2'
    MAIN_REEF3 = 'M3'
    FULL_GENOA_ONLY = 'GF'
    GENOA_REEF1 = 'G1'
    GENOA_REEF2 = 'G2'
    GENOA_REEF3 = 'G3'

    sail_plans = [
        (FULL_SAIL, 'Full Sail'),
        (ALL_SAILS_REEF_1, 'All sails reef 1'),
        (ALL_SAILS_REEF_2, 'All sails reef 1'),
        (ALL_SAILS_REEF_3, 'All sails reef 3'),
        (FULL_MAIN_ONLY, 'Only Main Full'),
        (MAIN_REEF1, 'Only Main Reef 1'),
        (MAIN_REEF2, 'Only Main Reef 2'),
        (MAIN_REEF3, 'Only Main Reef 3'),
        (FULL_GENOA_ONLY, 'only Full Genoa'),
        (GENOA_REEF1, 'only Genoa reef 1'),
        (GENOA_REEF2, 'only Genoa reef 2'),
        (GENOA_REEF3, 'only Genoa reef 3'),
        (NO_SAILS, 'no sails')
    ]

    when = models.DateTimeField()
    passage = models.ForeignKey(Passage, on_delete=models.CASCADE, blank=True, null=True)
    wind_side = models.CharField(choices=tack, max_length=1, default=UNKNOWN, null=True)
    wind_force = models.DecimalField(max_digits=1, decimal_places=0, blank=True, null=True)
    wind_direction = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    sail_plan = models.CharField(choices=sail_plans, max_length=2, default=NO_SAILS, null=True)
    spinnaker = models.BooleanField(default=False)
    cruising_shoot = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.when} {self.passage.start_from}'


class Position(models.Model):
    MOORED = 'MB'
    UNDER_WAY = 'UW'
    MAIN_ENGINE = 'ME'
    UNDER_TOW = 'UT'
    TOWING = 'TV'
    ADRIFT = 'AD'
    AT_ANCHOR = 'AA'
    AGROUND = 'AG'
    HEAVED_TO = 'HT'
    MOTOR_SAILING = 'MS'
    IN_IRONS = 'II'
    CLOSE_HAULED = 'CH'
    CLOSE_REACH = 'CR'
    BEAM_REACH = 'BB'
    BROAD_REACH = 'BR'
    RUNNING = 'RU'

    sail_status = [
        (MOORED, 'Moored/Berthed'),
        (UNDER_WAY, 'under way'),
        (MAIN_ENGINE, 'main engine'),
        (UNDER_TOW, 'under tow'),
        (TOWING, 'towing vessel'),
        (ADRIFT, 'adrift'),
        (AT_ANCHOR, 'at anchor'),
        (AGROUND, 'aground'),
        (HEAVED_TO, 'heaved too'),
        (MOTOR_SAILING, 'Motor Sailing'),
        (IN_IRONS, 'In Irons'),
        (CLOSE_HAULED, 'Close Hauled'),
        (CLOSE_REACH, 'Close Reach'),
        (BEAM_REACH, 'Beam Reach'),
        (BROAD_REACH, 'Broad Reach'),
        (RUNNING, 'running under sail')
    ]

    when = models.DateTimeField()
    narrative = models.TextField(blank=True, default='')
    passage = models.ForeignKey(Passage, on_delete=models.CASCADE, blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)
    log = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    course = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    speed = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    sog = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    cog = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    status = models.CharField(choices=sail_status, max_length=2, default=MOORED, null=True)

    def __str__(self):
        return f'{self.when} {self.passage.start_from}'


class TideLog(models.Model):
    when = models.DateTimeField()
    passage = models.ForeignKey(Passage, on_delete=models.CASCADE, blank=True, null=True)
    HW = models.DateTimeField()
    LW = models.DateTimeField()
    port = models.CharField(max_length=100, blank=True, default='')
    spring_neap_percent = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)

    def __str__(self):
        return f'{self.when} {self.port}'


class DepthLog(models.Model):
    when = models.DateTimeField()
    depth = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)
    tide = models.ForeignKey(TideLog, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.when} {self.depth}'


class Track(models.Model):
    name = models.CharField(max_length=150, default="")
    passage = models.ForeignKey(Passage, on_delete=models.CASCADE, blank=True, null=True)
    gpx_source_file = models.CharField(max_length=180, blank=True, default="")
    gpx_track_name = models.CharField(max_length=150, default="", blank=True)

    def __str__(self):
        return f'{self.name} {self.passage}'


class TrackPoint(models.Model):
    track = models.ForeignKey(Track, on_delete=models.CASCADE, blank=True, null=True)
    number = models.DecimalField(max_digits=6, decimal_places=0, blank=True, null=True)
    segment = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    seg_num = models.DecimalField(max_digits=4, decimal_places=0, blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)
    depth = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)

    def __str__(self):
        return f'{self.track} - {self.number}'


class FixLog(models.Model):
    when = models.DateTimeField()
    passage = models.ForeignKey(Passage, on_delete=models.CASCADE, blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)
    depth = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    by = models.CharField(max_length=20, blank=True, default='GPS')

    def __str__(self):
        return f'{self.when} {self.passage.start_from}'
