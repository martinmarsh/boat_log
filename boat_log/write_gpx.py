from collections import OrderedDict

import xmltodict

from boat_log.models import GPXWriteFile
from boat_log.nav_functions import str_to_lat_long
from passage.models import TrackPoint, Track, Passage, Position
from planning.models import WayPoint, Plan, PlanPoint
from .read_gpx import ex_plan_defs, ex_rte_defs


def list_segs(track_points, extensions):
    segment = 0
    seg_list = []
    point_list = []
    for track_point in track_points:
        segmemt = int(getattr(track_point, "segment", 1))
        if segment != segmemt:
            segment = segmemt
            if point_list:
                seg_list.append(OrderedDict([('trkpt', point_list)]))
                point_list = []

        lat, long = str_to_lat_long(track_point.lat, track_point.long)
        trp_pt = OrderedDict([
                ('@lat', lat),
                ('@lon', long),
                ])
        if track_point.when:
            trp_pt['time'] = track_point.when.strftime('%Y-%m-%dT%H:%M:%S%Z')
        if extensions == GPXWriteFile.RAYMARINE and track_point.extensions:
            trp_pt['extensions'] = track_point.extensions
        elif extensions == GPXWriteFile.OPEN_CPN and track_point.opencpn_extensions:
            trp_pt['extensions'] = track_point.opencpn_extensions

        point_list.append(trp_pt)
    if point_list:
        seg_list.append(OrderedDict([('trkpt', point_list)]))

    return seg_list


def track_dict(track, extensions, do_content):
    track_gpx = OrderedDict([
        ('name', track.name),
        ('desc', track.description),
    ])
    if extensions == GPXWriteFile.RAYMARINE:
        track_gpx['extensions'] = track.extensions
    elif extensions == GPXWriteFile.OPEN_CPN:
        track_gpx['extensions'] = track.opencpn_extensions
    if do_content == GPXWriteFile.TRACKS:
        track_points = TrackPoint.objects.filter(track=track).order_by('number')
    else:
        track_points = Position.objects.filter(passage=track).order_by('number')
    track_gpx['trkseg'] = list_segs(track_points, extensions)
    return track_gpx


# noinspection DuplicatedCode
def plan_point_dict(plan_point, extensions):
    lat, long = str_to_lat_long(plan_point.lat, plan_point.long)
    plan_point_gpx = OrderedDict([
        ('@lat', lat),
        ('@lon', long),
        ('time', plan_point.time),
        ('name', plan_point.name),
        ('sym', plan_point.symbol),
        ('type', plan_point.type),

    ])
    if extensions == GPXWriteFile.RAYMARINE:
        plan_point_gpx['extensions'] = plan_point.extensions
    elif extensions == GPXWriteFile.OPEN_CPN:
        plan_point_gpx['extensions'] = plan_point.opencpn_extensions
        for field_name, ext_name in ex_rte_defs.items():
            plan_point_gpx['extensions'][ext_name] = getattr(plan_point, field_name)

    return plan_point_gpx


def plan_dict(plan, extensions):
    plan_gpx = OrderedDict([
        ('name', plan.title)
    ])
    if extensions == GPXWriteFile.RAYMARINE:
        plan_gpx['extensions'] = plan.extensions
    elif extensions == GPXWriteFile.OPEN_CPN:
        plan_gpx['extensions'] = plan.opencpn_extensions
        for field_name, ext_name in ex_plan_defs.items():
            plan_gpx['extensions'][ext_name] = getattr(plan, field_name)
    rtept_list = []
    plan_points = PlanPoint.objects.filter(plan=plan).order_by('number')
    for plan_point in plan_points:
        rtept_list.append(plan_point_dict(plan_point, extensions))
    plan_gpx['rtept'] = rtept_list

    return plan_gpx


# noinspection DuplicatedCode
def waypoint_dict(way_pt, extensions):
    lat, long = str_to_lat_long(way_pt.lat, way_pt.long)
    wpt = OrderedDict([
        ('@lat', lat),
        ('@lon', long),
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


def write_out(directory, out_file, select, content, extensions):
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

        for do_content in [GPXWriteFile.WAYPOINTS, GPXWriteFile.ROUTES, GPXWriteFile.TRACKS, GPXWriteFile.PASSAGE]:
            if content == GPXWriteFile.ALL or content == do_content:
                if do_content == GPXWriteFile.WAYPOINTS:
                    way_pts = WayPoint.objects.filter(select)
                    wpt_list = []
                    for way_pt in way_pts:
                        wpt_list.append(waypoint_dict(way_pt, extensions))
                    gpx['gpx']['wpt'] = wpt_list

                if do_content == GPXWriteFile.ROUTES:
                    selected_plans = Plan.objects.filter(select)
                    rte_list = []
                    for plan in selected_plans:
                        rte_list.append(plan_dict(plan, extensions))
                    gpx['gpx']['rte'] = rte_list
                if do_content == GPXWriteFile.TRACKS or do_content == GPXWriteFile.PASSAGE:
                    if do_content == GPXWriteFile.TRACKS:
                        tracks = Track.objects.filter(select)
                    else:
                        tracks = Passage.objects.filter(select)
                    track_list = []
                    for track in tracks:
                        track_list.append(track_dict(track, extensions, do_content))
                    gpx['gpx']['trk'] = track_list
        xmltodict.unparse(gpx, output=fd, encoding='utf-8', pretty=True, indent="  ")
