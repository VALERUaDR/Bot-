import random
from datetime import date

from db import VKUser
from dictionaries import FEMALE, MALE_DESC, map_relation, FEMALE_DESC, MALE

BDATE = "bdate"
HOME_TOWN = "home_town"
CITY = "city"
SEX = "sex"
RELATION = "relation"


def age(birthdate):
    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age


class VKMessages:
    def __init__(self, vk):
        self.vk = vk

    def write_msg(self, user_id, message, attachment=None):
        if attachment is None:
            attachment = []
        random_id = random.randint(1, 100000000)
        self.vk.method('messages.send',
                       {'user_id': user_id, 'message': message, 'random_id': random_id, 'attachment': attachment})

    def write_hello(self, user_id):
        self.write_msg(user_id, 'Привет')

    def write_goodby(self, user_id):
        self.write_msg(user_id, 'Пока((')

    def write_welcome_message(self, user_id):
        self.write_msg(user_id, "Добро пожаловать в бот VKinder \n"
                       + "Возможные команды: \n"
                       + "Поиск: +\n"
                       + "Инфо обо мне: я\n"
                       + "Изменить инфо: изменить возраст/пол/город/статус (Пример: изменить город)")

    def write_request(self, user_id, req, errors):
        message = "Не хватает данных. Пожалуйста введите " + req + " \n"
        for m in errors:
            message += m + '\n'
        self.write_msg(user_id, message)

    def write_match(self, user_id, profile, photos):
        message = 'Погляди кого нашёл \n'
        message += profile['first_name'] + " " + profile['last_name'] + "\n"
        message += "https://vk.com/id" + str(profile["id"])
        attachments = []
        for p in photos:
            attachments.append("photo" + str(profile["id"]) + "_" + str(p["id"]))
        self.write_msg(user_id, message, ','.join(attachments))

    def write_notfound(self, user_id):
        self.write_msg(user_id, "Совпадений не найдено :-(")

    def write_info(self, user):
        sex = MALE_DESC if user.sex == MALE else FEMALE_DESC
        rel = map_relation.get(user.relation)
        self.write_msg(user.id, "Инфо обо мне: \n" + str(user.age) + " " + sex
                       + " " + user.hometown + " " + "/".join(rel))


class VKSearch:
    def __init__(self, vk, vku, db):
        self.vk = vk
        self.vks = vku
        self.db = db

    # Получение данных текущего пользователя
    def get_user_info(self, vk_id) -> VKUser:
        result = self.vk.method("users.get",
                                {'user_ids': vk_id, "fields": [SEX, RELATION, BDATE, HOME_TOWN, CITY]})
        res = result[0]

        uage = age(res[BDATE]) if BDATE in res and res[BDATE] is not None else None
        hometown = None
        if HOME_TOWN in res and res[HOME_TOWN] is not None:
            hometown = res[HOME_TOWN]
        else:
            if CITY in res and res[CITY] is not None:
                hometown = res[CITY]["title"]
        relation = res[RELATION] if RELATION in res and res[RELATION] is not None else None
        sex = res[SEX] if SEX in res and res[SEX] is not None else None
        return VKUser(vk_id, uage, sex, hometown, relation)

    # Поиск пользователя
    def search_user(self, user):
        sex = MALE if user.sex == FEMALE else FEMALE

        result = self.vks.method("users.search",
                                 {'count': 1000,
                                  'age_from': user.age,
                                  'age_to': user.age,
                                  'hometown': user.hometown,
                                  "sex": sex, "has_photo": 1})

        items = result['items']
        not_found = True
        profile = None
        size = len(items)
        if size == 0:
            return None
        search_try = 0
        while not_found:
            search_try += 1
            i = random.randint(0, size - 1)
            profile = items[i]
            if not self.db.has_match(user.id, profile["id"]):
                self.db.save_match(user.id, profile["id"])
                if not profile["is_closed"]:
                    not_found = False
            else:
                profile = None
            if search_try == size:
                profile = None
                break

        return profile

    # Поиск фото
    def search_photos(self, profile):
        result = self.vks.method("photos.get",
                                 {'count': 100,
                                  'owner_id': profile["id"],
                                  "album_id": "profile",
                                  "extended": 1,
                                  "rev": 0})
        items = []
        for item in result["items"]:
            items.append({
                "id": item["id"],
                "score": item["likes"]["count"] + item["comments"]["count"]
            })
        items = sorted(items, key=lambda x: (-x['score']))
        photos = items[0:3]
        return photos
