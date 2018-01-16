import requests

url = 'http://192.168.2.207:8000/save'

fin = open('ff.jpg', 'rb')
files = {'file': fin}
try:
    r = requests.post(url, files=files)
    print(r.text)
finally:
    fin.close()

# print(r.request.headers)
# print(dir(r.request.body))
