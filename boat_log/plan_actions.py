from planning.models import Plan, PlanPoint
from boat_log.common import dict_from_attr_list

plan_items = ("start_time", "end_time", "start_from", "to", "notes", "wind_force", "wind_direction",
              "becoming_wind_force", "becoming_direction", "plan_speed")

plan_point_items = ('name', 'number', 'description', 'time', 'lat', 'long', 'symbol', 'psym', 'type', 'tide_rates',
                    'tide_station', 'set_rotation', 'drift_factor', 'way_point', 'arrival_radius')


def copy_plan(rec):
    attrs = dict_from_attr_list(plan_items, rec)
    attrs['title'] = f'{rec.title} copy'
    plan_copy = Plan.objects.create(**attrs)

    plan_points = PlanPoint.objects.filter(plan=rec).order_by('number')
    for plan_point in plan_points:
        attrs = dict_from_attr_list(plan_point_items, plan_point)
        attrs['plan'] = plan_copy
        PlanPoint. objects.create(**attrs)


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
