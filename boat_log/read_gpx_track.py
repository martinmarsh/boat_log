import xmltodict
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from passage.models import TrackPoint, Track
from django.utils.dateparse import parse_datetime


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
            print(track, segment)
            for trk_seg in trk_data['trkseg']:
                for trk_pt in trk_seg['trkpt']:
                    tp = TrackPoint(
                        track=track,
                        number=number,
                        segment=segment,
                        seg_num=seg_num,
                        lat=trk_pt.get('@lat'),
                        long=trk_pt.get('@lat')
                    )
                    tp.save()
                    number += 1
                    seg_num += 1
                    if seg_num > 20:
                        break
                segment += 1
                seg_num = 1
    print("done")


def read_in(directory, in_file):
    full_file = f'{directory}{in_file}'

    with open(full_file) as fd:
        gpx = xmltodict.parse(fd.read())
        if gpx['gpx'].get('trk'):
            read_track(in_file, gpx)


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
