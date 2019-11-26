import requests

BASE_URL = "http://colormind.io/api/"

payload =  {"model": "default"}

resp = requests.get(BASE_URL, data=payload)

SUCESSFUL = 200

assert resp.status_code == SUCESSFUL

print(resp.text)
