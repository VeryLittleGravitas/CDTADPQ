#!/usr/bin/env python
import unittest

from CDTADPQ.web.test_init import AppTests
from CDTADPQ.data.test_users import UsersTests
from CDTADPQ.data.test_collect import CollectTests
from CDTADPQ.data.test_notify import NotifyTests
from CDTADPQ.data.test_wildfires import WildfireTests
from CDTADPQ.data.test_earthquakes import EarthquakeTests
from CDTADPQ.data.test_floods import FloodTests
from CDTADPQ.data.test_zipcodes import ZipcodeTests

if __name__ == '__main__':
    unittest.main()
