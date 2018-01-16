import bson
import requests
import time

data = {"pid": 1,
        'title': "title",
        'body_ru': "body_ru",
        'body_en': "body_en",
        'lang': "lang",
        'publish': "publish",
        'date': int(time.time())}

email = {
    "email": 'qwe@qwe.ru',
    "name": 'volgograd',
    "phone": '+7...',
    "vacancy": 'manager',
    "link": "123"
}

resp = requests.post("http://new.kefirgames.ru/remove_vacancy", json={"_id": "5a5882409158635e5781e761"})
# resp = requests.post("http://192.168.2.209:8000/remove_vacancy", json={"_id": "5a313691fefd25b57dc307d5"})
# resp = requests.post("http://35.198.161.58/feedback", json=email)
# resp = requests.get("http://35.198.161.58/static/123.png", params={"filename": "123.png"})
# resp = requests.post("http://192.168.2.207:8000/feedback", json=email)
# resp = requests.post("http://192.168.2.207:8000/vacancies", data)
# resp = requests.get("http://192.168.2.207:8000/blog")
# resp = requests.post("http://192.168.2.207:8000/signin", data)
# resp = requests.get("http://192.168.2.207:8000/signout")
# resp = requests.get("http://192.168.2.207:8000/")
print(resp.text)
print(resp.headers)
