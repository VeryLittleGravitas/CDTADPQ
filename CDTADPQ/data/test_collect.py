import unittest, unittest.mock
from . import collect

class CollectTests (unittest.TestCase):
    
    def test_main(self):
        '''
        '''
        with unittest.mock.patch('CDTADPQ.data.wildfires.main') as wildfires, \
             unittest.mock.patch('CDTADPQ.data.earthquakes.main') as earthquakes, \
             unittest.mock.patch('CDTADPQ.data.floods.main') as floods:
            collect.main()
        
        wildfires.assert_called_once_with()
        earthquakes.assert_called_once_with()
        floods.assert_called_once_with()
