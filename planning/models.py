from django.db import models


class Plan(models.Model):
    title = models.CharField(max_length=150, db_index=True, default="")
    opencpn_guid = models.CharField(max_length=150, db_index=True, default="", blank=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    start_from = models.CharField(max_length=100, db_index=True, blank=True, default="")
    to = models.CharField(max_length=100, blank=True, db_index=True, default="")
    notes = models.TextField(blank=True, default="")
    wind_force = models.DecimalField(max_digits=1, decimal_places=0, blank=True, null=True)
    wind_direction = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    becoming_wind_force = models.DecimalField(max_digits=1, decimal_places=0, blank=True, null=True)
    becoming_direction = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    plan_speed = models.DecimalField(max_digits=3, decimal_places=1, default=5.5)
    distance = models.DecimalField(max_digits=7, decimal_places=1, blank=True, null=True)
    dtw = models.DecimalField(max_digits=7, decimal_places=1, blank=True, null=True)
    opencpn_extensions = models.JSONField(null=True,  blank=True)
    extensions = models.JSONField(null=True, blank=True)
    active = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class TideStation(models.Model):
    name = models.CharField(max_length=150, db_index=True)
    hrs_difference = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    tide_station = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class TideTimes(models.Model):
    tide_station = models.ForeignKey(TideStation, on_delete=models.CASCADE)
    time = models.DateTimeField(blank=True, null=True)
    ht = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    high_water = models.BooleanField(default=True, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tide_station


class TideHeightPoint(models.Model):
    hrs = models.DecimalField(max_digits=1, decimal_places=0, blank=True, null=True)
    tide_station = models.ForeignKey(TideStation, on_delete=models.CASCADE)
    spring = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    neap = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f'{self.hrs} - {self.tide_station}'


class TideRate(models.Model):
    name = models.CharField(max_length=150, db_index=True )
    lat = models.CharField(max_length=16, default="", blank=True)
    long = models.CharField(max_length=16, default="", blank=True)
    tide_station = models.ForeignKey(TideStation, on_delete=models.CASCADE, blank=True, null=True)
    channel_flow = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class TideRatePoint(models.Model):
    hrs = models.DecimalField(max_digits=1, decimal_places=0, blank=True, null=True)
    tide_rate = models.ForeignKey(TideRate, on_delete=models.CASCADE)
    direction = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    spring = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    neap = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)

    def __str__(self):
        return f'{self.hrs} - {self.tide_rate}'


class WayPoint(models.Model):
    name = models.CharField(max_length=150, db_index=True, default="", blank=True)
    description = models.TextField(default="", blank=True)
    lat = models.CharField(max_length=16, default="", blank=True)
    long = models.CharField(max_length=16, default="", blank=True)
    time = models.DateTimeField(blank=True, null=True)
    type = models.CharField(max_length=10, default="WPT", blank=True)
    symbol = models.CharField(max_length=80, default="", blank=True)
    psym = models.CharField(max_length=80, default="", blank=True)
    opencpn_guid = models.CharField(max_length=150, default="",  blank=True)
    raymarine_guid = models.CharField(max_length=150, default="",  blank=True)
    extensions = models.JSONField(null=True,  blank=True)
    opencpn_extensions = models.JSONField(null=True,  blank=True)
    links = models.JSONField(null=True,  blank=True)
    tide_station = models.ForeignKey(TideStation, on_delete=models.CASCADE, blank=True, null=True)
    tide_rates = models.ForeignKey(TideRate, on_delete=models.CASCADE, blank=True, null=True)
    drift_factor = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    set_rotation = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    active = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class PlanPoint(models.Model):
    name = models.CharField(max_length=150,db_index=True, default="", blank=True)
    time = models.DateTimeField(blank=True, null=True)
    number = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    major = models.BooleanField(default=True, db_index=True)
    fixed = models.BooleanField(default=True, db_index=True)
    description = models.TextField(default="", blank=True)
    type = models.CharField(max_length=10, default="WPT", blank=True)
    way_point = models.ForeignKey(WayPoint, on_delete=models.CASCADE, blank=True, null=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, blank=True, null=True)
    symbol = models.CharField(max_length=80, default="", blank=True)
    psym = models.CharField(max_length=80, default="", blank=True)
    lat = models.CharField(max_length=16, default="", blank=True)
    long = models.CharField(max_length=16, default="", blank=True)
    extensions = models.JSONField(null=True, blank=True)
    opencpn_extensions = models.JSONField(null=True,  blank=True)
    opencpn_guid = models.CharField(max_length=150, default="",  blank=True)
    arrival_radius = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    links = models.JSONField(null=True, blank=True)
    tide_rates = models.ForeignKey(TideRate, on_delete=models.CASCADE, blank=True, null=True)
    set = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    drift = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    cts = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    cog = models.DecimalField(max_digits=3, decimal_places=0, blank=True, null=True)
    smg = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    dtw = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    distance = models.DecimalField(max_digits=7, decimal_places=1, blank=True, null=True)
    plan_speed = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['number', 'plan']),
        ]

    def __str__(self):
        return f'{self.name}_{self.number}'
