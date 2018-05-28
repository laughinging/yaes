import requests
import time

local_url = 'http://127.0.0.1:5000/'
remote_url = 'http://35.204.58.232:8888/'

email_info = {
    'sender': 'test@test.com', 
    'recipient': 'test@test.com',
    'subject': 'test subject.',
    'body': 'This is a test email.'
    }

# post an email request
r = requests.post(remote_url, data=email_info)

# get the job id and check job status
job_id = r.json().get('job_id') 
r = requests.post(remote_url+'check', data={'job_id': job_id})
print(r.text)

# wait for sometime and check again
time.sleep(2)
r = requests.post(remote_url+'check', data={'job_id': job_id})
print(r.text)
