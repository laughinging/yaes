from app import app
import unittest
import redis
import json

_normal_email = {
        'sender': 'test@test.com',
        'recipient': 'test@test.com',
        'subject': 'test_subject',
        'body': 'This is a test email.'
        }

_invalid_email = {
        'sender': 'a_bad_email_address',
        'recipient': 'another_bad_email_address',
        'subject': 'test_subject',
        'body': 'This is a bad email.'
        }

class FlaskAppTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_status_get(self):
        rv = self.app.get('/')
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'text/html', rv.data)

    def test_home_status_post(self):
        rv = self.app.post('/', data=_normal_email)
        self.assertIn(b'job_id', rv.data)
        self.assertIn(b'status', rv.data)
        rv = self.app.post('/', data=_invalid_email)
        self.assertIn(b'job_id', rv.data)
        self.assertIn(b'status', rv.data)

    def test_check_job_get(self):
        rv = self.app.get('/check')
        self.assertEqual(rv.status_code, 200)
        self.assertIn(b'text/html', rv.data)

    def test_check_job_post_invalid_job_id(self):
        rv = self.app.post('/check', data={'job_id': 'xxx'})
        self.assertIn(b'Invalid', rv.data)
        self.assertIn(b'400', rv.data)
        self.assertEqual(rv.status_code, 200)

    def test_check_job_post_valid_job_id(self):
        r = json.loads(self.app.post('/', data=_normal_email).data)
        valid_job_id = r.get('job_id')
        rv = self.app.post('/check', data={'job_id': valid_job_id})
        status_code = json.loads(rv.data).get('status_code')
        self.assertIn(status_code, (200, 201, 202, 203))
        
if __name__ == '__main__':
    unittest.main()
