from django.db import models


class EngineLog(models.Model):
    when = models.DateTimeField()
    eng_log = models.DecimalField(max_digits=10, decimal_places=3)
    fuel_rate = models.DecimalField(max_digits=4, decimal_places=1)
    est_tank = models.DecimalField(max_digits=5, decimal_places=1)
    fuel_added = models.DecimalField(max_digits=6, decimal_places=2)
    full_tank = models.BooleanField(default=False)


class WeatherLog(models.Model):
    when = models.DateTimeField()
    wind_force = models.DecimalField(max_digits=1, decimal_places=0)
    wind_direction = models.DecimalField(max_digits=3, decimal_places=0)
    temperature = models.DecimalField(max_digits=3, decimal_places=1)
    humidity = models.DecimalField(max_digits=3, decimal_places=0)
    pressure = models.DecimalField(max_digits=4, decimal_places=0)
