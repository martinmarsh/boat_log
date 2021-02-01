from django.db import models
from planning.models import Plan


class Passage(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    start_from = models.CharField(max_length=200)
    to = models.CharField(max_length=200)
    towards = models.CharField(max_length=200)
    narrative = models.TextField()
    weather = models.TextField()
    maintenance = models.TextField()
    max_wind_force = models.DecimalField(max_digits=1, decimal_places=0)
    max_wind_direction = models.DecimalField(max_digits=3, decimal_places=0)
    min_wind_force = models.DecimalField(max_digits=1, decimal_places=0)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    distance = models.DecimalField(max_digits=7, decimal_places=1)
    fuel_used = models.DecimalField(max_digits=5, decimal_places=1)
    day_hrs = models.DecimalField(max_digits=3, decimal_places=1)
    night_hrs = models.DecimalField(max_digits=3, decimal_places=1)


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

    sail_plans = [
        (FULL_SAIL, 'Full Sail'),
        (ALL_SAILS_REEF_1, 'All sails reef 1'),
        (ALL_SAILS_REEF_2, 'All sails reef 1'),
        (ALL_SAILS_REEF_3, 'All sails reef 3'),
        (FULL_MAIN_ONLY, 'Only Main Full'),
        ('M1', 'Only Main Reef 1'),
        ('M2', 'Only Main Reef 2'),
        ('M3', 'Only Main Reef 3'),
        ('GF', 'only Full Genoa'),
        ('G1', 'only Genoa reef 1'),
        ('G2', 'only Genoa reef 2'),
        ('G3', 'only Genoa reef 3'),
        (NO_SAILS, 'no sails')
    ]

    when = models.DateTimeField()
    wind_side = models.CharField(choices=tack, max_length=1, default=UNKNOWN)
    wind_force = models.DecimalField(max_digits=1, decimal_places=0)
    wind_direction = models.DecimalField(max_digits=3, decimal_places=0)
    sail_plan = models.CharField(choices=sail_plans, max_length=2, default=NO_SAILS)
    spinnaker = models.BooleanField(default=False)
    cruising_shoot = models.BooleanField(default=False)


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
    passage = models.ForeignKey(Passage, on_delete=models.CASCADE)
    lat = models.FloatField()
    long = models.FloatField()
    log = models.DecimalField(max_digits=10, decimal_places=3)
    eng_log = models.DecimalField(max_digits=10, decimal_places=3)
    course = models.DecimalField(max_digits=3, decimal_places=0)
    speed = models.DecimalField(max_digits=3, decimal_places=0)
    sog = models.DecimalField(max_digits=3, decimal_places=0)
    cog = models.DecimalField(max_digits=3, decimal_places=0)
    depth = models.DecimalField(max_digits=3, decimal_places=0)
    status = models.CharField(choices=sail_status, max_length=2, default=MOORED)
