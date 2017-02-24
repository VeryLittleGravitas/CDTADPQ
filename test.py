#!/usr/bin/env python
import unittest

from CDTADPQ.web.test_init import AppTests
from CDTADPQ.data.test_users import UsersTests
from CDTADPQ.data.test_wildfires import WildfireTests
from CDTADPQ.data.test_zipcodes import ZipcodeTests

if __name__ == '__main__':
    unittest.main()
