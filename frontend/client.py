import requests
import time

email_info = {'recipient':'aaa@bb.cc', 'subject':'aaa', 'body':'ccc'}
r = requests.post('http://127.0.0.1:5000/', data=email_info)
print(r.text)
job_id = (r.json().get('job_id'))
r = requests.get('http://127.0.0.1:5000/check/{}'.format(job_id))
print(r.text)
time.sleep(2)
r = requests.get('http://127.0.0.1:5000/check/{}'.format(job_id))
print(r.text)
