import unittest
import redis
import json
import time

from rq import Queue
from fakeredis import FakeStrictRedis
from send import PROVIDER, send_mail



class SendMailTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

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

    def test_send_normal_email_without_worker(self):

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

    def test_send_invalid_email_with_work_on(self):

        self.queue = Queue(async=True, connection=FakeStrictRedis())
        job = self.queue.enqueue(send_mail,
                sender='a_bad_email_address',
                recipient='another_bad_email_address',
                subject='test subject',
                body='This is a bad email.')
        self.assertIsNotNone(job.id)
        self.assertTrue(job.is_failed or job.is_queued or job.is_started)

        #time.sleep(2) # waiting for the job to be finished
        #self.assertTrue(job.is_failed)

        
if __name__ == '__main__':
    unittest.main()
