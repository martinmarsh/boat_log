from planning.models import Plan, PlanPoint, TideRate, TideRatePoint
from boat_log.common import dict_from_attr_list
from boat_log.nav_functions import course, str_to_lat_long, course_over_water
from datetime import timedelta


plan_items = ("start_time", "end_time", "start_from", "to", "notes", "wind_force", "wind_direction",
              "becoming_wind_force", "becoming_direction", "plan_speed")

plan_point_items = ('name', 'number', 'fixed', 'major', 'description', 'time', 'lat', 'long', 'symbol', 'psym', 'type',
                    'tide_rates', 'tide_station', 'set_rotation', 'drift_factor', 'way_point', 'arrival_radius')


def copy_plan(rec):
    attrs = dict_from_attr_list(plan_items, rec)
    attrs['title'] = f'{rec.title} copy'
    plan_copy = Plan.objects.create(**attrs)

    plan_points = PlanPoint.objects.filter(plan=rec).order_by('number')
    for plan_point in plan_points:
        attrs = dict_from_attr_list(plan_point_items, plan_point)
        attrs['plan'] = plan_copy
        PlanPoint.objects.create(**attrs)


def copy_tide_rate(rec):
    rec['name'] = f'{rec.name} copy'
    tr_copy = TideRate.objects.create(**rec)

    tr_points = TideRatePoint.objects.filter(tide_rate=rec).order_by('hrs')
    for tr_point in tr_points:
        tr_point['tide_rate'] = tr_copy
        PlanPoint. objects.create(**tr_point)


def reverse_copy_plan(rec):

    attrs = dict_from_attr_list(plan_items, rec)
    attrs['title'] = f'{rec.title} Reversed'
    if attrs.get('start_from'):
        to = attrs.get('to', '')
        attrs['to'] = attrs['start_from']
        attrs['start_from'] = to
    elif attrs.get('to'):
        start = attrs.get('start_from', '')
        attrs['start_from'] = attrs['to']
        attrs['to'] = start
    plan_copy = Plan.objects.create(**attrs)

    plan_points = PlanPoint.objects.filter(plan=rec).order_by('-number')
    number = 1
    for plan_point in plan_points:
        attrs = dict_from_attr_list(plan_point_items, plan_point)
        attrs['plan'] = plan_copy
        attrs['number'] = number
        PlanPoint.objects.create(**attrs)
        number += 1


def plan_route(rec):
    current_time = rec.start_time
    plan_speed = float(rec.plan_speed)
    plan_points = PlanPoint.objects.filter(plan=rec).order_by('number')
    number = 0
    sub_number = 0
    total_distance = 0
    total_water_distance = 0
    last_lat = None
    last_long = None
    drift_start = None
    set_start = None

    changed = []
    for pt in plan_points:
        if pt.fixed:
            number += 1
            sub_number = 0
        elif not pt.fixed:
            sub_number += 1

        if int(pt.number) != number and pt.fixed:
            pt.number = number
            changed = ['number']
        elif int((pt.number-int(pt.number))*100) != sub_number:
            pt.number = number + sub_number/100
            changed = ['number']

        nav_change =[]
        # now calculate eta
        if number == 1:
            pt.time = current_time
            drift_start = pt.drift
            set_start = pt.set
            pt.cts = None
            pt.smg = None
            pt.distance = 0
            last_lat = pt.lat
            last_long = pt.long
            nav_change = ['time', 'drift', 'set', 'cts', 'smg', 'distance']
        else:
            bearing, distance = course(
                str_to_lat_long(last_lat, last_long),
                str_to_lat_long(pt.lat, pt.long)
            )
            last_lat = pt.lat
            last_long = pt.long
            if pt.plan_speed is not None:
                course_plan_speed = pt.plan_speed 
            else:
                course_plan_speed = plan_speed 
        
            pt.cts, pt.dtw, pt.smg, delta_time = course_over_water(bearing, distance, course_plan_speed, set_start, drift_start)
 
            pt.distance = distance
            total_distance += distance
            total_water_distance += pt.dtw
            pt.cog = bearing
    
            nav_change = ['time', 'drift', 'set', 'cts', 'cog', 'smg', 'distance', "dtw"]
            pt.time = current_time + timedelta(hours=delta_time)
            current_time = pt.time
            drift_start = pt.drift
            set_start = pt.set

        changed.extend(nav_change)
        if changed:
            changed.append('updated_at')
            pt.save(update_fields=changed)

    rec.end_time = current_time
    rec.distance = total_distance
    rec.dtw = total_water_distance
    rec.save(update_fields=['end_time', 'distance', 'dtw'])
