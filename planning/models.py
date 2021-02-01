from django.db import models


class Plan(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    start_from = models.CharField(max_length=200)
    to = models.CharField(max_length=200)
    notes = models.TextField()
    wind_force = models.DecimalField(max_digits=1, decimal_places=0)
    wind_direction = models.DecimalField(max_digits=3, decimal_places=0)
    becoming_wind_force = models.DecimalField(max_digits=1, decimal_places=0)
    becoming_direction = models.DecimalField(max_digits=3, decimal_places=0)
    plan_speed = models.DecimalField(max_digits=3, decimal_places=1)


class PlanPoint(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    number = models.IntegerField()
    eta = models.DateTimeField()
    lat = models.FloatField()
    long = models.FloatField()
    set = models.DecimalField(max_digits=3, decimal_places=0)
    drift = models.DecimalField(max_digits=3, decimal_places=1)
    cts = models.DecimalField(max_digits=3, decimal_places=0)
    smg = models.DecimalField(max_digits=3, decimal_places=1)
    distance = models.DecimalField(max_digits=7, decimal_places=1)
