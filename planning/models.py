from django.db import models


class Plan(models.Model):
    title = models.CharField(max_length=150, default="")
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    start_from = models.CharField(max_length=100, blank=True, default="")
    to = models.CharField(max_length=100, blank=True, default="")
    notes = models.TextField(blank=True, default="")
    wind_force = models.DecimalField(max_digits=1, decimal_places=0, blank=True, null=True)
    wind_direction = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    becoming_wind_force = models.DecimalField(max_digits=1, decimal_places=0, blank=True, null=True)
    becoming_direction = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    plan_speed = models.DecimalField(max_digits=3, decimal_places=1, default=5.5)

    def __str__(self):
        return f'{self.title} {self.start_from} to {self.to} {self.start_time}'


class TideStation(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class TideHeightPoint(models.Model):
    hrs = models.DecimalField(max_digits=1, decimal_places=0, blank=True, null=True)
    tide_station = models.ForeignKey(TideStation, on_delete=models.CASCADE)
    spring = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    neap = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f'{self.hrs} - {self.tide_station}'


class TideRates(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class TideRatePoint(models.Model):
    hrs = models.DecimalField(max_digits=1, decimal_places=0, blank=True, null=True)
    tide_rates = models.ForeignKey(TideRates, on_delete=models.CASCADE)
    direction = models.DecimalField(max_digits=1, decimal_places=0, blank=True, null=True)
    spring = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    neap = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)

    def __str__(self):
        return f'{self.hrs} - {self.tide_rates}'


class WayPoint(models.Model):
    name = models.CharField(max_length=150, default="", blank=True)
    description = models.TextField(default="", blank=True)
    lat = models.FloatField()
    long = models.FloatField()
    symbol = models.CharField(max_length=80, default="", blank=True)
    viz_name = models.CharField(max_length=150, default="",  blank=True)
    arrival_radius = models.JSONField(null=True,  blank=True)
    range_rings = models.JSONField(null=True,  blank=True)
    scale = models.JSONField(null=True,  blank=True)
    links = models.JSONField(null=True,  blank=True)
    tide_station = models.ForeignKey(TideStation, on_delete=models.CASCADE, blank=True, null=True)
    tide_rates = models.ForeignKey(TideRates, on_delete=models.CASCADE, blank=True, null=True)
    drift_factor = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    set_rotation = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)

    def __str__(self):
        return self.name


class PlanPoint(models.Model):
    number = models.IntegerField()
    way_point = models.ForeignKey(WayPoint, on_delete=models.CASCADE, blank=True, null=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, blank=True, null=True)
    eta = models.DateTimeField(blank=True, null=True)
    set = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    drift = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    cts = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    smg = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    distance = models.DecimalField(max_digits=7, decimal_places=1, blank=True, null=True)

    def __str__(self):
        return f'{self.number} - {self.way_point}'
