import xmltodict
from django.utils.dateparse import parse_datetime
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from passage.models import TrackPoint, Track


def read_track(in_file, selected_track):
    selected_track_track_name = selected_track.gpx_track_name
    with open(in_file) as fd:
        gpx = xmltodict.parse(fd.read())
        if gpx['gpx'].get('trk'):
            for trk_data in gpx['gpx']['trk']:
                track_data_name = trk_data.get('name')
                if track_data_name == selected_track_track_name:
                    track = selected_track
                else:
                    try:
                        track = Track.objects.get(gpx_track_name=track_data_name,
                                                  gpx_source_file=in_file)
                    except ObjectDoesNotExist:
                        track = Track.objects.create(
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


def read_in(in_file):

    with open(in_file) as fd:
        gpx = xmltodict.parse(fd.read())
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

        if gpx['gpx'].get('wpt'):
            for wpt_data in gpx['gpx']['wpt']:
                print(wpt_data)

        if gpx['gpx'].get('trk'):
            for trk_data in gpx['gpx']['trk']:
                print(wpt_data)
