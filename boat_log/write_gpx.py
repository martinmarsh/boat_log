import xmltodict
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from passage.models import TrackPoint, Track
from planning.models import WayPoint, PlanPoint
from django.utils.dateparse import parse_datetime
import math


def read_track(in_file, gpx):
    for trk_data in gpx['gpx']['trk']:
        track_data_name = trk_data.get('name')
        try:
            track = Track.objects.get(gpx_track_name=track_data_name,
                                      gpx_source_file=in_file)
        except ObjectDoesNotExist:
            track = Track.objects.create(
                name=f'{in_file}/{track_data_name}',
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
            for trk_seg in trk_data['trkseg']:
                for trk_pt in trk_seg['trkpt']:
                    if seg_num == 1:
                        lat0 = float(trk_pt.get('@lat', 0))
                        long0 = float(trk_pt.get('@lon', 0))
                        delta_lat = delta / math.cos(math.radians(lat0))
                    lat1 = float(trk_pt.get('@lat'))
                    long1 = float(trk_pt.get('@lon'))
                    if seg_num == 1 or math.fabs(long1-long0) > delta or math.fabs(lat1-lat0) > delta_lat:
                        tp = TrackPoint(
                            track=track,
                            number=number,
                            segment=segment,
                            seg_num=seg_num,
                            lat=lat1,
                            long=long1
                        )
                        tp.save()
                        lat0 = lat1
                        long0 = long1
                        number += 1

                    seg_num += 1
                segment += 1
                seg_num = 1
    print("done")


def write_waypoints(gpx, way_pts):
    pass


def write_out(directory, in_file, from_date, content):
    full_file = f'{directory}{in_file}'
    gpx = {}
    with open(full_file, 'w') as fd:
        for do_content in ['WP', 'RT', 'TR']:
            if content == 'AL' or content == do_content:
                if do_content == 'WP':
                    way_pts = WayPoint.objects.filter(from_date >= from_date)
                    write_waypoints(gpx, way_pts)
                if do_content == 'TR':
                    track = WayPoint
