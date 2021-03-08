from planning.models import TideStation, TideTimes
import datetime


def tide_times(port, time):
    hrs7 = datetime.timedelta(hours=-7)
    tides = TideTimes.objects.filter(tide_station=port, date__range=[time - hrs7, time + hrs7])
    percent_spring = 0.5

    if len(tides) < 2:
        return False, False, False

    prev_time = -28800
    next_time = 28800
    next_tide = None
    last_tide = None

    for tide in tides:
        delta_secs = (tide.time - time).total_seconds()
        if prev_time < delta_secs <= 0:
            last_tide = tide
            prev_time = delta_secs
        if next_time > delta_secs >= 0:
            next_tide = tide
            next_time = delta_secs

    return last_tide, next_tide, percent_spring


def find_tide_time(port, time):
    """
    Searches back through linked ports until it finds  a time period
    :param port:
    :param time:
    :return:
    """
    last_tide, next_tide, sp = tide_times(port, time)
    diff_time = 0
    sp = .5
    while not (last_tide and next_tide):
        if port.tide_station:
            diff_time += port.hrs_difference
            last_tide, next_tide, sp = tide_times(port.tide_station, time-datetime.timedelta(hours=diff_time))
            port = port.tide_station
        else:
            break

    if not (last_tide and next_tide):
        return False, 0

    if last_tide.high_water:
        hw_time = last_tide.time + datetime.timedelta(hours=diff_time)
    else:
        hw_time = last_tide.time + datetime.timedelta(hours=diff_time)

    return hw_time, sp
