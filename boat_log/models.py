from django.db import models
from passage.models import Passage


class EngineLog(models.Model):
    when = models.DateTimeField()
    passage = models.ForeignKey(Passage, on_delete=models.CASCADE, blank=True, null=True)
    eng_log = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    fuel_rate = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    est_tank = models.DecimalField(max_digits=5, decimal_places=1,  blank=True, null=True)
    fuel_added = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    full_tank = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.when} {self.passage.start_from}'


class WeatherLog(models.Model):
    when = models.DateTimeField()
    passage = models.ForeignKey(Passage, on_delete=models.CASCADE, blank=True, null=True)
    wind_force = models.DecimalField(max_digits=1, decimal_places=0, blank=True, null=True)
    wind_direction = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    temperature = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    humidity = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    pressure = models.DecimalField(max_digits=4, decimal_places=0,  blank=True, null=True)

    def __str__(self):
        return f'{self.when} {self.passage.start_from}'


class SeaLog(models.Model):
    BREAKING = 'BR'
    WHITE_TOP = 'WT'
    RIPPLES = "RP"
    GLASSY = 'GY'
    UNDEFINED = 'UD'
    sea_state = [
        (BREAKING, 'Breaking'),
        (WHITE_TOP, 'White tops/ Foam '),
        (RIPPLES, 'Ripples'),
        (GLASSY, 'Flat / Glassy'),
        (UNDEFINED, 'undefined')
    ]
    when = models.DateTimeField()
    passage = models.ForeignKey(Passage, on_delete=models.CASCADE, blank=True, null=True)
    drift = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    set = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    wave_ht = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    wave_length = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    swell = models.BooleanField(default=False)
    sea = models.CharField(choices=sea_state, max_length=2, default=UNDEFINED, null=True)

    def __str__(self):
        return f'{self.when} {self.passage.start_from}'
