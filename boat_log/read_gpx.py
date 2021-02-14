import datetime
import math

import xmltodict
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.utils.dateparse import parse_datetime

from boat_log.nav_functions import lat_long_to_string
from passage.models import TrackPoint, Track
from planning.models import WayPoint, Plan, PlanPoint

ex_plan_defs = {
    'opencpn_guid': 'opencpn:guid',
    'start_from': 'opencpn:start',
    'to': 'opencpn:end',
    'plan_speed': 'opencpn:planned_speed',
    'start_time': 'opencpn:planned_departure',
}

ex_rte_defs = {
    'opencpn_guid': 'opencpn:guid',
    'arrival_radius': 'opencpn:arrival_radius'
}


def read_route(in_file, gpx_rte):
    route_name = gpx_rte.get('name', in_file)
    route_extensions = gpx_rte.get('extensions', {})

    passage_fields = {field_name: route_extensions.get(gpx_name, '') for field_name, gpx_name in ex_plan_defs.items()}
    for field_name in passage_fields:
        try:
            del (route_extensions[ex_plan_defs[field_name]])
        except KeyError:
            pass
    passage_fields['title'] = route_name
    passage_fields['opencpn_extensions'] = route_extensions
    set_fields = {field_name: field_value for field_name, field_value in passage_fields.items() if field_value}
    ids = {}
    if set_fields['opencpn_guid']:
        ids['opencpn_guid'] = set_fields['opencpn_guid']
    elif passage_fields['title']:
        ids['title'] = passage_fields['title']
        if passage_fields['start_time']:
            ids['start_time'] = passage_fields['start_time']
    plan, _ = Plan.objects.update_or_create(**ids, defaults=set_fields)

    defs = {
        'name': 'name',
        'time': 'time',
        'description': 'desc',
        'type': 'type',
        'links': 'link',
        'lat': '@lat',
        'long': '@lon',
        'symbol': 'sym',
        'psym': 'psym',
    }
    number = 1
    for rte_data in gpx_rte.get('rtept', {}):
        rte_extensions = rte_data.get('extensions')
        passage_point_exts = {field_name: rte_extensions.get(gpx_name, '') 
                              for field_name, gpx_name in ex_rte_defs.items()}
        for field_name in passage_point_exts:
            try:
                del (rte_extensions[ex_rte_defs[field_name]])
            except KeyError:
                pass
        field = {field_name: rte_data.get(gpx_name, '') for field_name, gpx_name in defs.items()}
        field['opencpn_extensions'] = rte_extensions
        field['number'] = number
        field['plan'] = plan
        field.update(passage_point_exts)
        field['lat'], field['long'] = lat_long_to_string(field.get('lat'), field.get('long'))
        set_fields = {field_name: field_value for field_name, field_value in field.items() if field_value}

        ids = {}
        if set_fields['opencpn_guid']:
            ids['opencpn_guid'] = set_fields['opencpn_guid']
        elif passage_fields['name']:
            ids['name'] = passage_fields['name']
            if passage_fields['time']:
                ids['time'] = passage_fields['time']
        PlanPoint.objects.update_or_create(**ids, defaults=set_fields)
        number += 1


def process_trk_segment(trk_pt, seg_num, number, track, segment, delta, lat0, long0, delta_lat):
    if seg_num == 1:
        lat0 = float(trk_pt.get('@lat', 0))
        long0 = float(trk_pt.get('@lon', 0))
        delta_lat = delta / math.cos(math.radians(lat0))
    lat1 = float(trk_pt.get('@lat'))
    long1 = float(trk_pt.get('@lon'))
    if seg_num == 1 or math.fabs(long1 - long0) > delta or math.fabs(lat1 - lat0) > delta_lat:
        data = {
            'track': track,
            'number': number,
            'segment': segment,
            'seg_num': seg_num,
            'lat': lat1,
            'long': long1
        }
        if trk_pt.get('time'):
            data['when'] = trk_pt['time']
        if trk_pt.get('extensions'):
            if trk_pt['extensions'].get('raymarine:TrackPointExtension'):
                data['extensions'] = trk_pt['extensions']
                if trk_pt['extensions']['raymarine:TrackPointExtension'].get('raymarine:WaterDepth'):
                    data['depth'] = trk_pt['extensions']['raymarine:TrackPointExtension']['raymarine:WaterDepth']
            else:
                data['opencpn_extensions'] = trk_pt['extensions']
                
        data['lat'], data['long'] = lat_long_to_string(data.get('lat'), data.get('long'))

        TrackPoint.objects.create(**data)
        lat0 = lat1
        long0 = long1
        number += 1
    seg_num += 1
    return seg_num, number, lat0, long0


def read_track(in_file, trk_data, track_number):
    track_data_name = trk_data.get('name', in_file)
    if track_number > 0:
        track_data_name = f'{track_data_name}/trk-{track_number}'
    try:
        track = Track.objects.get(gpx_track_name=track_data_name)
    except ObjectDoesNotExist:
        track = Track.objects.create(
            name=track_data_name,
            description=trk_data.get('desc', in_file),
            gpx_track_name=track_data_name,
            gpx_source_file=in_file
        )
    except MultipleObjectsReturned:
        track = None

    if not TrackPoint.objects.filter(track=track).exists():
        number = 1
        segment = 1
        seg_num = 1
        delta = 2E-04  # about22.4
        delta_lat = delta  # recalculated for segment lat
        lat0 = 0
        long0 = 0

        print(track, segment)
        try:
            for trk_seg in trk_data['trkseg'].values():
                for trk_pt in trk_seg:
                    seg_num, number, lat0, long0 = process_trk_segment(
                        trk_pt, seg_num, number, track, segment, delta, lat0, long0, delta_lat
                    )
                print(track, segment, seg_num)
                segment += 1
                seg_num = 1
        except AttributeError:
            for trk_seg in trk_data['trkseg']:
                for trk_pt in trk_seg['trkpt']:
                    seg_num, number, lat0, long0 = process_trk_segment(
                        trk_pt, seg_num, number, track, segment, delta, lat0, long0, delta_lat
                    )
                print(track, segment, seg_num)
                segment += 1
                seg_num = 1


def read_tracks(in_file, gpx_trk):
    track_number = 1
    try:
        for trk_data in gpx_trk:
            read_track(in_file, trk_data, track_number)
            track_number += 1
        print("done")
    except AttributeError:
        track_number = 0
        read_track(in_file, gpx_trk, track_number)


def read_waypoint(in_file, gpx_wpt):
    defs = {
        'name': 'name',
        'time': 'time',
        'description': 'desc',
        'type': 'type',
        'links': 'link',
        'lat': '@lat',
        'long': '@lon',
        'symbol': 'sym',
        'psym': 'psym',
    }
    for wpt_data in gpx_wpt:
        field = {field_name: wpt_data.get(gpx_name, '') for field_name, gpx_name in defs.items()}
        extensions = wpt_data.get('extensions')
        ids = {}
        if extensions:
            opencpn_guid = extensions.get('opencpn:guid', '')
            if opencpn_guid:
                field['opencpn_guid'] = opencpn_guid
                ids['opencpn_guid'] = opencpn_guid
                field['opencpn_extensions'] = extensions
            else:
                field['extensions'] = extensions
                raymarine = extensions.get('raymarine:WaypointExtension')
                if raymarine:
                    field['raymarine_guid'] = raymarine.get('raymarine:GUID')
                    ids['raymarine_guid'] = field['raymarine_guid']

        field['lat'], field['long'] = lat_long_to_string(field.get('lat'), field.get('long'))
        set_fields = {field_name: field_value for field_name, field_value in field.items() if field_value}
        if not ids:
            ids['time'] = field.get('time', datetime.datetime.now())

        WayPoint.objects.update_or_create(**ids, defaults=set_fields)


def read_in(directory, in_file):
    full_file = f'{directory}{in_file}'

    with open(full_file) as fd:
        gpx = xmltodict.parse(fd.read())
        if gpx['gpx'].get('trk'):
            read_tracks(in_file, gpx['gpx']['trk'])
        if gpx['gpx'].get('wpt'):
            read_waypoint(in_file, gpx['gpx']['wpt'])
        if gpx['gpx'].get('rte'):
            read_route(in_file,  gpx['gpx']['rte'])


def get_first_track_time(gpx):
    try:
        first_date = parse_datetime(gpx['gpx']['trk']['trkseg']['trkpt'][0]['time'])
        date_str = first_date.strftime('%Y-%dm-%d')
        time_str = first_date.strftime('%H:%M:%S')
        zone_str = first_date.strftime('%z')
    except (AttributeError, TypeError, IndexError):
        first_date = None
        date_str = ""
        time_str = ""
        zone_str = ""
    return first_date,  date_str,  time_str, zone_str
