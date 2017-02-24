import unittest, unittest.mock
from . import zipcodes

class ZipcodeTests (unittest.TestCase):

    def test_lookup_zipcode(self):
        '''
        '''
        db = unittest.mock.Mock()
        db.fetchone.return_value = ('94612', )
        zipcode = zipcodes.lookup_zipcode(db, 37, -122)
        
        db.execute.assert_called_once_with(
               '''SELECT "ZCTA5CE10"
                  FROM tl_2016_us_zcta510
                  WHERE ST_Intersects(geog, ST_Buffer(ST_GeogFromText(%s), 500))
                  ORDER BY ST_Distance(geog, %s) ASC
                  LIMIT 1
                  ''',
               ('POINT (-122 37)', 'POINT (-122 37)'))

        self.assertEqual(zipcode, '94612')
