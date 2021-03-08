from django.test import TestCase

from boat_log.nav_functions import str_to_lat_long, lat_long_to_string, course


class LatLongTestCase(TestCase):

    def setUp(self):
        pass

    def test_lat_to_string(self):
        self.assertTupleEqual(lat_long_to_string(50.1, -1.56789356), ("50° 6.000'N", "001° 34.074'W"))
        self.assertTupleEqual(lat_long_to_string(50.1, -1.5), ("50° 6.000'N", "001° 30.000'W"))
        self.assertTupleEqual(lat_long_to_string(50.1, 1.5), ("50° 6.000'N", "001° 30.000'E"))
        self.assertTupleEqual(lat_long_to_string(-50.1, 1.5), ("50° 6.000'S", "001° 30.000'E"))
        self.assertTupleEqual(lat_long_to_string(-50.75, 179.5), ("50° 45.000'S", "179° 30.000'E"))
        self.assertTupleEqual(lat_long_to_string(-50.75, 179.999999), ("50° 45.000'S", "180° 0.000'E"))
        self.assertTupleEqual(lat_long_to_string(-50.75, 179.99999), ("50° 45.000'S", "179° 59.999'E"))
        self.assertTupleEqual(lat_long_to_string(-50.75, 179.999990000000011), ("50° 45.000'S", "179° 59.999'E"))
        self.assertTupleEqual(lat_long_to_string(-50.75, 179.999990000000012), ("50° 45.000'S", "180° 0.000'E"))

    def test_string_to_lat_long(self):
        x = str_to_lat_long("50° 6.000'N", "001° 34.074'W")
        self.assertAlmostEqual(x[0], 50.1)
        self.assertAlmostEqual(x[1], -1.56789356, 4)
        x = str_to_lat_long("50° 6.000'N", "001° 30.000'W")
        self.assertAlmostEqual(x[0], 50.1, 4)
        self.assertAlmostEqual(x[1], -1.5, 4)
        x = str_to_lat_long("50° 6.000'N", "001° 30.000'E")
        self.assertAlmostEqual(x[0], 50.1, 4)
        self.assertAlmostEqual(x[1], 1.5, 4)
        x = str_to_lat_long("50° 6.000'S", "001° 30.000'E")
        self.assertAlmostEqual(x[0], -50.1, 4)
        self.assertAlmostEqual(x[1], 1.5, 4)
        x = str_to_lat_long("50° 45.000'S", "179° 30.000'E")
        self.assertAlmostEqual(x[0], -50.75, 4)
        self.assertAlmostEqual(x[1], 179.5, 4)
        x = str_to_lat_long("50° 45.000'S", "180° 0.000'E")
        self.assertAlmostEqual(x[0], -50.75, 4)
        self.assertAlmostEqual(x[1], 180, 4)
        x = str_to_lat_long("50° 45.000'S", "180° 0.000'W")
        self.assertAlmostEqual(x[0], -50.75, 4)
        self.assertAlmostEqual(x[1], -180, 4)
        x = str_to_lat_long("50° 45.000'S", "179° 59.999'E")
        self.assertAlmostEqual(x[0], -50.75, 4)
        self.assertAlmostEqual(x[1], 179.99999, 4)
        x = str_to_lat_long("50 6.000'N", "001° 30.000'W")
        self.assertAlmostEqual(x[0], 50.1, 4)
        x = str_to_lat_long("50 6.000 N", "001 30.000W")
        self.assertAlmostEqual(x[0], 50.1, 4)

    def test_lat_long_to_mercator(self):
        x = course(
            str_to_lat_long("50° 37.4712'N", "000° 36.7764'W"),
            str_to_lat_long("50° 11.0321'N", "001° 13.6288'W"))
        self.assertAlmostEqual(x[0], 222, 0)
        self.assertAlmostEqual(x[1], 35.4, 1)
        x = course(
            str_to_lat_long("50° 11.0321'N", "001° 13.6288'W"),
            str_to_lat_long("50° 11.0914'N", "000° 46.0358'W"))
        self.assertAlmostEqual(x[0], 90, 0)
        self.assertAlmostEqual(x[1], 17.7, 1)
        x = course(
            str_to_lat_long("50° 11.0914'N", "000° 46.0358'W"),
            str_to_lat_long("50° 37.4712'N", "000° 36.7764'W"))
        self.assertAlmostEqual(x[0], 13, 0)
        self.assertAlmostEqual(x[1], 27.1, 1)
