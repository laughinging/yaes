import requests
import time

#email_info = {'sender': 'qianyunguo@gmail.com',
#        'recipient':'qianyunguo@gmail.com', 'subject':'aaa', 'body':'ccc'}
#r = requests.post('http://127.0.0.1:5000/', data=email_info)

job_id = "10199492-811a-4a99-b39f-c9ff9bec515c"

r = requests.post('http://127.0.0.1:5000/check', data={'job_id': job_id})
print(r.text)
time.sleep(2)

r = requests.post('http://127.0.0.1:5000/check', data={'job_id': job_id})
print(r.text)
