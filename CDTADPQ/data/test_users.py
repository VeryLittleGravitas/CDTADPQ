import unittest, unittest.mock
from . import users

class UsersTests (unittest.TestCase):

    def test_add_verified_signup(self):
        '''
        '''
        db, account = unittest.mock.Mock(), unittest.mock.Mock()
        to_number, signup_id, pin_number = '+1 (510) 555-1212', 'xxx-yy-zzz', 1234
        
        with unittest.mock.patch('CDTADPQ.data.users.send_verification_code') as send_verification_code, \
             unittest.mock.patch('random.randint') as randint, \
             unittest.mock.patch('uuid.uuid4') as uuid4:
            randint.return_value = pin_number
            uuid4.return_value = signup_id
            output_id = users.add_verified_signup(db, account, to_number)
        
        self.assertEqual(output_id, signup_id)
        
        db.execute.assert_called_once_with(
            '''INSERT INTO unverified_signups
                  (signup_id, phone_number, pin_number) VALUES (%s, %s, %s)''',
               (signup_id, to_number, str(pin_number)))
        
        send_verification_code.assert_called_once_with(account, to_number, str(pin_number))
