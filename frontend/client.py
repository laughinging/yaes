import requests
import time

email_info = {'body':'ccc'}
r = requests.post('http://127.0.0.1:5000/', data=email_info)
print(r.text)

job_id = "539018ce-4214-47bb-856e-b9513f0437f2"
r = requests.post('http://127.0.0.1:5000/check', data={'job_id': job_id})
print(r.text)
time.sleep(2)

r = requests.post('http://127.0.0.1:5000/check', data={'job_id': job_id})
print(r.text)
