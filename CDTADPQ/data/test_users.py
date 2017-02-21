import unittest, unittest.mock
from . import users

class UsersTests (unittest.TestCase):

    def test_add_verified_signup(self):
        '''
        '''
        db, account = unittest.mock.Mock(), unittest.mock.Mock()
        to_number, pin_number = '+1 (510) 555-1212', 1234
        
        with unittest.mock.patch('CDTADPQ.data.users.send_verification_code') as send_verification_code, \
             unittest.mock.patch('random.randint') as randint:
            randint.return_value = pin_number
            users.add_verified_signup(db, account, to_number)
        
        db.execute.assert_called_once_with(
            '''INSERT INTO unverified_signups
                  (phone_number, pin_number) VALUES (%s, %s)''',
               (to_number, str(pin_number)))
        
        send_verification_code.assert_called_once_with(account, to_number, str(pin_number))
