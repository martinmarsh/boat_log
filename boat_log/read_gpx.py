import xmltodict
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from passage.models import TrackPoint, Track
from planning.models import WayPoint
from django.utils.dateparse import parse_datetime
import math
import datetime


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
        TrackPoint.objects.create(**data)
        lat0 = lat1
        long0 = long1
        number += 1
    seg_num += 1
    return seg_num, number, lat0, long0


def read_track(in_file, gpx):
    track_number = 1
    for trk_data in gpx['gpx']['trk']:
        track_data_name = trk_data.get('name', in_file)
        if track_number > 1:
            track_data_name = f'{track_data_name}/trk-{track_number}'
        track_number += 1
        try:
            track = Track.objects.get(gpx_track_name=track_data_name)
        except ObjectDoesNotExist:
            track = Track.objects.create(
                name=track_data_name,
                gpx_track_name=track_data_name,
                gpx_source_file=in_file
            )
        except MultipleObjectsReturned:
            track = None

        if not TrackPoint.objects.filter(track=track).exists():
            number = 1
            segment = 1
            seg_num = 1
            delta = 1E-04  # about 11.2m
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
    print("done")


def read_waypoint(in_file, gpx):
    for wpt_data in gpx['gpx']['wpt']:
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
        set_fields = {field_name: field_value for field_name, field_value in field.items() if field_value}
        if not ids:
            ids['time'] = field.get('time', datetime.datetime.now())

        WayPoint.objects.update_or_create(**ids, defaults=set_fields)


def read_in(directory, in_file):
    full_file = f'{directory}{in_file}'

    with open(full_file) as fd:
        gpx = xmltodict.parse(fd.read())
        if gpx['gpx'].get('trk'):
            read_track(in_file, gpx)
        if gpx['gpx'].get('wpt'):
            read_waypoint(in_file, gpx)


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
