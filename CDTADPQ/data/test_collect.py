import unittest, unittest.mock
from . import collect

class CollectTests (unittest.TestCase):
    
    def test_main(self):
        '''
        '''
        with unittest.mock.patch('CDTADPQ.data.wildfires.main') as wildfires:
            collect.main()
        
        wildfires.assert_called_once_with()
