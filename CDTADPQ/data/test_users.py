import unittest, unittest.mock
from . import users

class UsersTests (unittest.TestCase):

    def test_add_unverified_signup(self):
        '''
        '''
        db, account = unittest.mock.Mock(), unittest.mock.Mock()
        to_number, signup_id, pin_number = '+1 (510) 555-1212', 'xxx-yy-zzz', 1234
        
        with unittest.mock.patch('CDTADPQ.data.users.send_verification_code') as send_verification_code, \
             unittest.mock.patch('random.randint') as randint, \
             unittest.mock.patch('uuid.uuid4') as uuid4:
            randint.return_value = pin_number
            uuid4.return_value = signup_id
            output_id = users.add_unverified_signup(db, account, to_number)
        
        self.assertEqual(output_id, signup_id)
        
        db.execute.assert_called_once_with(
            '''INSERT INTO unverified_signups
                  (signup_id, phone_number, pin_number) VALUES (%s, %s, %s)''',
               (signup_id, to_number, str(pin_number)))
        
        send_verification_code.assert_called_once_with(account, to_number, str(pin_number))
    
    def test_verify_user_signup(self):
        '''
        '''
        db = unittest.mock.Mock()
        
        db.fetchone.return_value = ('1234', '+15105551212')
        verified = users.verify_user_signup(db, '1234', 'xxx-yy-zzz')
        
        self.assertTrue(verified)
        self.assertEqual(db.execute.mock_calls[-2][1], ('SELECT pin_number, phone_number FROM unverified_signups WHERE signup_id = %s', ('xxx-yy-zzz',)))
        self.assertEqual(db.execute.mock_calls[-1][1], ('INSERT INTO users (phone_number) VALUES (%s)', ('+15105551212',)))
        
        db.fetchone.return_value = None
        verified = users.verify_user_signup(db, '1234', 'xxx-yy-zzz')
        
        self.assertFalse(verified)
        self.assertEqual(db.execute.mock_calls[-1][1], ('SELECT pin_number, phone_number FROM unverified_signups WHERE signup_id = %s', ('xxx-yy-zzz',)))
