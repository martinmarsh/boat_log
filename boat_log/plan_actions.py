from planning.models import Plan, PlanPoint


def copy_plan(rec):
    plan_copy = Plan.objects.create(
        title=f'{rec.title} copy'
    )
    plan_points = PlanPoint.objects.filter(plan=rec).order_by('number')
    for plan_point in plan_points:
        items = ['name', 'number', 'description', 'time', 'lat', 'long', 'symbol', 'psym', 'type', 'tide_rates',
                 'tide_station', 'set_rotation', 'drift_factor', 'way_point', 'arrival_radius',
                 ]
        attrs = {}
        for item in items:
            if getattr(plan_point, item, False):
                attrs[item] = getattr(plan_point, item)
        attrs['plan'] = plan_copy
        PlanPoint. objects.create(**attrs)
