import requests

email_info = {'recipient':'aaa@bb.cc', 'subject':'aaa', 'body':'ccc'}
r = requests.post('http://127.0.0.1:5000/', data=email_info)
print(r.text)
r = requests.get('http://127.0.0.1:5000/check/c9fc2ec7-e5f1-45e5-a9e9-b44a6fe0a0e1')
print(r.text)
