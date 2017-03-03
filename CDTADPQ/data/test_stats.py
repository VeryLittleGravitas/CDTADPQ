import unittest, unittest.mock
from . import stats

class StatsTests (unittest.TestCase):

    def test_get_all_notifications_log_rows(self):
        '''
        '''
        db = unittest.mock.Mock()
        db.fetchall.return_value = [dict(id=1, message='fire!!', notified_users_count=1)]
        stats.get_all_notifications_log_rows(db)
        self.assertEqual(db.execute.mock_calls[-1][1],
                 ('SELECT * FROM notifications_log',))
