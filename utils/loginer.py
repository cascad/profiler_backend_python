import json

import requests

data = {
    # "email": "123",
    "login": "cascad",
    "password": "123",
    # "id": "12345"
}

data2 = {
    "pid": 58,
    "title_ru": "Гейм дизайнер",
    "title_en": "",
    "body_ru": "<p><span style=\"font-size: 22px;\">Вы - наш человек, если у вас есть:</span>&nbsp;&nbsp;</p>\n<ul>\n<li><span style=\"font-size: 12px;\">огромный интерес к играм на мобильных платформах</span>&nbsp;</li>\n<li><span style=\"font-size: 12px;\">большой игровой опыт</span>&nbsp;</li>\n<li><span style=\"font-size: 12px;\">умение генерировать нестандартные идеи</span>&nbsp;</li>\n<li><span style=\"font-size: 12px;\">аналитический склад ума</span>&nbsp;</li>\n<li><span style=\"font-size: 12px;\">хороший письменный русский язык</span>&nbsp;</li>\n<li><span style=\"font-size: 12px;\">активность, целеустремленность и ответственность</span>&nbsp;</li>\n</ul>\n<p><span style=\"font-size: 22px;\">Значительным преимуществом будет:</span>&nbsp;&nbsp;</p>\n<ul>\n<li><span style=\"font-size: 12px;\">опыт в разработке модификаций к играм и дизайне карт</span>&nbsp;</li>\n</ul>\n<p><span style=\"font-size: 22px;\">Задачи, которые ждут вас:</span>&nbsp;&nbsp;</p>\n<ul>\n<li><span style=\"font-size: 12px;\">аналитика рынка приложений</span>&nbsp;</li>\n<li><span style=\"font-size: 12px;\">разработка концепта игры</span>&nbsp;</li>\n<li><span style=\"font-size: 12px;\">разработка сеттинга игры</span>&nbsp;</li>\n<li><span style=\"font-size: 12px;\">проработка экономики игры</span>&nbsp;</li>\n<li><span style=\"font-size: 12px;\">проработка геймплея</span>&nbsp;</li>\n<li><span style=\"font-size: 12px;\">сопровождение разработки, консультирование</span>&nbsp;</li>\n</ul>\n",
    "body_en": "",
    "city": "volgograd",
    "active": True
}

cookie = "gAAAAABaJqNFZgF3JbnzEMaR8ko9uoyuBj4VxgT5lFeUbscUIDh3M11fVFIoi6lEmrBkg4ENsL9_aB3YSYKuKxqhVsp2SCLPpIREJvO8rnstCu-QA-eb_C2jr8flFwxH48dWa8nztwJM8be1aRaZd92H_mk2Z-Hyegd1-dXYqk34Xi7GMcYAqPvMVC8H1KvWYIZJRxpbO3O0vqw-Pqgx1Z3f4c3m58OFPA=="

# resp = requests.post("http://192.168.2.207:8000/signup", json=data)
resp = requests.post("http://192.168.2.207:8000/vacancies", json.dumps(data2).encode(), cookies={"KEFIR_WEB": cookie})
# resp = requests.post("http://192.168.2.207:8000/login", json=data)

# resp = requests.get("http://192.168.2.207:8000/vacancies")
# resp = requests.post("http://192.168.2.207:8000/signin", data)
# resp = requests.get("http://192.168.2.207:8000/signout")
# resp = requests.get("http://192.168.2.207:8000/")
print(resp.text)
print(resp.headers)
