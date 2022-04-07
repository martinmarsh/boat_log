from inspect import CO_GENERATOR
import re
import math
import decimal

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


def knots_to_ms(x: float) -> float:
    return x * 0.514444


def ms_to_knots(x: float) -> float:
    return x * 1.94384


def to_rec(course: float, mag: float) -> tuple:
    d = math.radians(course)
    x = mag * math.sin(d)
    y = mag * math.cos(d)
    return x, y

def to_polar(x: float, y: float)-> tuple:
    course = math.degrees(math.atan2(x,y))
    if course < 0:
        course +=360
        distance = math.sqrt(x * x + y * y)
        return course, distance


def course_over_water(cog: decimal.Decimal, dog: decimal.Decimal, speed: decimal.Decimal, set: decimal.Decimal, drift: decimal.Decimal): 
    cts = cog
    dtw = dog
    sog = speed
    time = float(dog) / float(speed)
    if drift and set is not None:
        x, y = to_rec(float(cog), float(speed))
        x1, y1 = to_rec(float(set), float(drift))
        x += x1
        y += y1
        f_cts, f_sog = to_polar(x, y)
        cts = decimal.Decimal(f_cts)
        sog = decimal.Decimal(f_sog)
        time = float(dog/sog)
        dtw = decimal.Decimal(time * float(speed))

    return cts, dtw, sog, time


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
        bearing = decimal.Decimal((math.degrees(math.atan2(d_long, d_phi)) + 360.0) % 360.0)

        if math.fabs(d_phi) > 10e-12:
            q = delta_lat / d_phi
        else:
            q = math.cos(lat1)

        if delta_lon > math.pi:
            delta_lon = -(2 * math.pi - delta_lon)
        elif delta_lon < -math.pi:
            delta_lon = 2 * math.pi + delta_lon

        distance = decimal.Decimal(math.sqrt(delta_lat * delta_lat + q * q * delta_lon * delta_lon) * r)

        return bearing, distance

    except Exception as e:
        raise CalculationError(e)
