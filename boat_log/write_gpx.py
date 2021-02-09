import xmltodict
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from passage.models import TrackPoint, Track
from planning.models import WayPoint, Plan, PlanPoint
from boat_log.models import GPXWriteFile
import math
from collections import OrderedDict


def plan_dict(plan, extensions):
    plan_gpx = OrderedDict([
        ('name', plan.title)
    ])
    if extensions == GPXWriteFile.RAYMARINE:
        plan_gpx['extensions'] = plan.extensions
    elif extensions == GPXWriteFile.OPEN_CPN:
        plan_gpx['extensions'] = plan.opencpn_extensions

    return plan_gpx


def waypoint_dict(way_pt, extensions):
    wpt = OrderedDict([
        ('@lat', way_pt.lat),
        ('@lon', way_pt.long),
        ('time', way_pt.time),
        ('name', way_pt.name),
        ('sym', way_pt.symbol),
        ('type', way_pt.type),
    ])
    if extensions == GPXWriteFile.RAYMARINE:
        wpt['psym'] = way_pt.psym
        wpt['extensions'] = way_pt.extensions
    elif extensions == GPXWriteFile.OPEN_CPN:
        wpt['extensions'] = way_pt.opencpn_extensions

    return wpt


def write_out(directory, out_file, from_date, content, extensions):
    full_file = f'{directory}{out_file}'
    with open(full_file, 'w') as fd:
        if extensions == GPXWriteFile.RAYMARINE:
            gpx = OrderedDict([
                ('gpx', OrderedDict([
                    ('@xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance'),
                    ('@version', '1.1'),
                    ('@xmlns', 'http://www.topografix.com/GPX/1/1'),
                    ('@creator', 'Raymarine'),
                    ('@xmlns:raymarine', 'http://www.raymarine.com'),
                    ('@xsi:schemaLocation', 'http://www.topografix.com/GPX/1/1 '
                                            'http://www.topografix.com/GPX/1/1/gpx.xsd'
                                            ' http://www.raymarine.com '
                                            'http://www.raymarine.com/gpx_schema/RaymarineGPXExtensions.xsd'),
                    ])
                 )
                ])
        elif extensions == GPXWriteFile.OPEN_CPN:
            gpx = OrderedDict([
                ('gpx', OrderedDict([
                    ('@version', '1.1'),
                    ('@creator', 'OpenCPN'),
                    ('@xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance'),
                    ('@xmlns', 'http://www.topografix.com/GPX/1/1'),
                    ('@xmlns:gpxx', 'http://www.garmin.com/xmlschemas/GpxExtensions/v3'),
                    ('@xsi:schemaLocation', 'http://www.topografix.com/GPX/1/1 '
                                            'http://www.topografix.com/GPX/1/1/gpx.xsd'),
                    ('@xmlns:opencpn', 'http://www.opencpn.org')
                ]))
            ])

        else:
            gpx = OrderedDict([
                ('gpx', OrderedDict([
                    ('@version', '1.1'),
                    ('@creator', 'BoatLog'),
                    ('@xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance'),
                    ('@xmlns', 'http://www.topografix.com/GPX/1/1'),
                    ('@xsi:schemaLocation', 'http://www.topografix.com/GPX/1/1 '
                                            'http://www.topografix.com/GPX/1/1/gpx.xsd'),
                ]))
            ])

        for do_content in [GPXWriteFile.WAYPOINTS, GPXWriteFile.ROUTES, GPXWriteFile.TRACKS]:
            if content == GPXWriteFile.ALL or content == do_content:
                if do_content == GPXWriteFile.WAYPOINTS:
                    way_pts = WayPoint.objects.filter(updated_at__gte=from_date)
                    wpt_list = []
                    for way_pt in way_pts:
                        wpt_list.append(waypoint_dict(way_pt, extensions))
                    gpx['gpx']['wpt'] = wpt_list

                if do_content == GPXWriteFile.ROUTES:
                    selected_plans = Plan.objects.filter(updated_at__gte=from_date)
                    rte_list = []
                    for plan in selected_plans:
                        rte_list.append(plan_dict(plan, extensions))
                    gpx['gpx']['rte'] = rte_list
                if do_content == GPXWriteFile.TRACKS:
                    pass
        xmltodict.unparse(gpx, output=fd, encoding='utf-8', pretty=True, indent="  ")
