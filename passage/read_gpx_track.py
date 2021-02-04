import xmltodict
from django.utils.dateparse import parse_datetime
from passage.models import TrackPoint, Track


def read_track(in_file, track):

    with open(in_file) as fd:
        gpx = xmltodict.parse(fd.read())

        if gpx['gpx'].get('trk'):
            for trk_data in gpx['gpx']['trk']:
                if trk_data.get('name') == 'Track 1':
                    number = 1
                    for trk_seg in trk_data['trkseg']:
                        for trk_pt in trk_seg['trkpt']:
                            tp = TrackPoint(
                                track=track,
                                number=number,
                                lat=trk_pt.get('@lat'),
                                long=trk_pt.get('@lat')
                            )
                            tp.save()
                            number += 1


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
