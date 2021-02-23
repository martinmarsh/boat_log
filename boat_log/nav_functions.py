import re
import math


RE_LAT = re.compile("^(\d{1,2})[ °][ ]*(\d{1,2}[.]?[0-9]*)[\x27 ]*([NSns])$")
RE_LONG = re.compile("^(\d{1,3})[ °][ ]*(\d{1,2}[.]?[0-9]*)[\x27 ]*([WEwe])$")


class ParserError(Exception):
    pass


class LatParserError(ParserError):
    pass


class LongParserError(ParserError):
    pass


class CalculationError(ArithmeticError):

    def __init__(self, message):
        self.message = message


def _to_real(x, err):
    if not x:
        raise err
    v = float(x[0][0]) + float(x[0][1])/60.0
    v = round(v, 6)
    if x[0][2] in ['S', 's', 'W', 'w']:
        v = -v
    return v


def str_to_lat_long(lat_str, long_str):
    lat = _to_real(RE_LAT.findall(lat_str), LatParserError)
    long = _to_real(RE_LONG.findall(long_str), LongParserError)
    return lat, long


def _to_string(x, le, pos_sym, neg_sym):
    sym = pos_sym
    x = float(x)
    if x < 0:
        x = -x
        sym = neg_sym
    d = int(x)
    m = (x-d)*60.0

    if m >= 59.9994:
        m = 0
        d = d + 1

    if le == 3:
        d0 = f"{d:03}"
    else:
        d0 = f"{d:02}"

    return f"{d0}° {m:2.3f}'{sym}"


def lat_long_to_string(lat, long):
    return _to_string(lat, 2, 'N', 'S'), _to_string(long, 3, 'E', 'W')


def course(pos1: tuple, pos2: tuple) -> tuple:
    try:
        lat1 = math.radians(pos1[0])
        long1 = math.radians(pos1[1])
        lat2 = math.radians(pos2[0])
        long2 = math.radians(pos2[1])

        r = 3440.1  # Radius of earth in Nm
        # delta = math.log(math.tan(math.pi / 4 + lat2 / 2) / math.tan(math.pi / 4 + lat1 / 2))
        delta_lon = long2 - long1
        delta_lat = lat2 - lat1

        d_phi = math.log(math.tan(lat2 / 2.0 + math.pi / 4.0) / math.tan(lat1 / 2.0 + math.pi / 4.0))
        d_long = delta_lon
        if math.fabs(delta_lon) > math.pi:
            if delta_lon > 0.0:
                d_long = -(2.0 * math.pi - delta_lon)
            else:
                d_long = (2.0 * math.pi + delta_lon)
        bearing = (math.degrees(math.atan2(d_long, d_phi)) + 360.0) % 360.0

        if math.fabs(d_phi) > 10e-12:
            q = delta_lat / d_phi
        else:
            q = math.cos(lat1)

        if delta_lon > math.pi:
            delta_lon = -(2 * math.pi - delta_lon)
        elif delta_lon < -math.pi:
            delta_lon = 2 * math.pi + delta_lon

        distance = math.sqrt(delta_lat * delta_lat + q * q * delta_lon * delta_lon) * r

        return bearing, distance

    except Exception as e:
        raise CalculationError(e)
