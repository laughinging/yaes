import unittest
import redis
import json
import time

from rq import Queue
from fakeredis import FakeStrictRedis
from send import * 

class SendMailTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        provider_pool = ['sendgrid', 'mailgun']
        redis_conn.set('provider_pool', ' '.join(provider_pool))

    def test_send_email_without_worker(self):

        self.queue = Queue(async=True, connection=FakeStrictRedis())
        job = self.queue.enqueue(send_mail,
                sender='test@test.com',
                recipient='test@test.com',
                subject='test subject',
               body='This is a test email.')
        self.assertIsNotNone(job.id)
        self.assertTrue(job.is_queued)

        # no worker to consume jobs, jobs are waiting in the queue
        time.sleep(2) 
        self.assertTrue(job.is_queued)

    def test_send_normal_email_with_worker(self):

        self.queue = Queue(async=False, connection=FakeStrictRedis())
        job = self.queue.enqueue(send_mail,
                sender='test@test.com',
                recipient='test@test.com',
                subject='test subject',
               body='This is a test email.')
        self.assertIsNotNone(job.id)
        self.assertTrue(job.is_queued or job.is_started or job.is_finished)

        # wait for the job to be finished
        time.sleep(2) 
        self.assertTrue(job.is_finished)

    def test_send_invalid_email_with_work(self):

        self.queue = Queue(async=False, connection=FakeStrictRedis())
        try:
            self.queue.enqueue(
                    send_mail,
                    sender='a_bad_email_address',
                    recipient='another_bad_email_address',
                    subject='test subject',
                    body='This is a bad email.')

        except Exception as e:
            self.assertIsInstance(e, InvalidRequestError)

    def test_send_normal_email_with_no_service_provider_available(self):

        # manually remove providers
        redis_conn.set('provider_pool', '')
        self.queue = Queue(async=False, connection=FakeStrictRedis())
        try:
            self.queue.enqueue(send_mail,
                sender='test@test.com',
                recipient='test@test.com',
                subject='test subject',
               body='This is a test email.')
        except Exception as e:
            self.assertIsInstance(e, ServerError)
        
if __name__ == '__main__':
    unittest.main()
