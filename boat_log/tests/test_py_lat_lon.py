from boat_log.nav_functions import lat_long_to_string, str_to_lat_long, course
from math import isclose
from unittest import TestCase


def assert_near_match(tup, m0, m1, tol=1e-05):
    assert isclose(tup[0], m0, rel_tol=tol)
    assert isclose(tup[1], m1, rel_tol=tol)


class LatLongTestCase(TestCase):

    @staticmethod
    def test_lat_to_string():
        assert lat_long_to_string(50.1, -1.56789356) == ("50° 6.000'N", "001° 34.074'W")
        assert lat_long_to_string(50.1, -1.5) == ("50° 6.000'N", "001° 30.000'W")
        assert lat_long_to_string(50.1, 1.5) == ("50° 6.000'N", "001° 30.000'E")
        assert lat_long_to_string(-50.1, 1.5) == ("50° 6.000'S", "001° 30.000'E")
        assert lat_long_to_string(-50.75, 179.5) == ("50° 45.000'S", "179° 30.000'E")
        assert lat_long_to_string(-50.75, 179.999999) == ("50° 45.000'S", "180° 0.000'E")
        assert lat_long_to_string(-50.75, 179.99999) == ("50° 45.000'S", "179° 59.999'E")
        assert lat_long_to_string(-50.75, 179.999990000000011) == ("50° 45.000'S", "179° 59.999'E")
        assert lat_long_to_string(-50.75, 179.999990000000012) == ("50° 45.000'S", "180° 0.000'E")


    @staticmethod
    def test_string_to_lat_long():
        assert_near_match(str_to_lat_long("50° 6.000'N", "001° 34.074'W"), 50.1, -1.56789356)
        assert_near_match(str_to_lat_long("50° 6.000'N", "001° 30.000'W"), 50.1, -1.5)
        assert_near_match(str_to_lat_long("50° 6.000'N", "001° 30.000'E"), 50.1, 1.5)
        assert_near_match(str_to_lat_long("50° 6.000'S", "001° 30.000'E"), -50.1, 1.5)
        assert_near_match(str_to_lat_long("50° 45.000'S", "179° 30.000'E"), -50.75, 179.5)
        assert_near_match(str_to_lat_long("50° 45.000'S", "180° 0.000'E"), -50.75, 179.999999)
        assert_near_match(str_to_lat_long("50° 45.000'S", "180° 0.000'E"), -50.75, 180)

    @staticmethod
    def test_lat_long_to_mercator():
        assert_near_match(
            course(
                str_to_lat_long("50° 37.4712'N", "000° 36.7764'W"),
                str_to_lat_long("50° 11.0321'N", "001° 13.6288'W")), 222, 35.4, tol=0.1)
        assert_near_match(
            course(
                str_to_lat_long("50° 11.0321'N", "001° 13.6288'W"),
                str_to_lat_long("50° 11.0914'N", "000° 46.0358'W")), 90, 17.7, tol=0.1)
        assert_near_match(
            course(
                str_to_lat_long("50° 11.0914'N", "000° 46.0358'W"),
                str_to_lat_long("50° 37.4712'N", "000° 36.7764'W")), 13, 27.1, tol=0.1)
