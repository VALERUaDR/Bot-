import vk_api
import traceback
import logging

from vk_api.longpoll import VkLongPoll, VkEventType

from checker import MessageChecker
from config import group_token, user_token
from db import KinderDatabase
from dictionaries import actions
from vkactions import VKMessages, VKSearch

vk = vk_api.VkApi(token=group_token)
vk_user = vk_api.VkApi(token=user_token)

# Работа с сообщениями
longpoll = VkLongPoll(vk)

db = KinderDatabase()
vkm = VKMessages(vk)
vks = VKSearch(vk, vk_user, db)
mc = MessageChecker(vkm, db)


# Изменение полей пользователя
def reset_user_field(user, text):
    parts = text.split(" ")
    action = parts[1]
    if actions.__contains__(action):
        db.reset_field(user, action)
    else:
        vkm.write_msg(user.id, "Неккоректная команда: " + action + " возможные значения: " + ", ".join(actions))
    return db.find_user(user.id)


# Основной цикл
for event in longpoll.listen():
    try:
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                request = event.text

                user_id = event.user_id
                user = db.find_user(user_id)
                if user is None:
                    user = vks.get_user_info(user_id)
                    db.create_user(user)
                    if not mc.check_user(user, request):
                        continue
                else:
                    if not mc.check_user(user, request):
                        continue

                if request.lower() == "привет":
                    vkm.write_hello(user_id)
                elif request.lower() == "пока":
                    vkm.write_goodby(user_id)
                elif request.lower() == "я":
                    vkm.write_info(user)
                elif "изменить" in request.lower():
                    user = reset_user_field(user, request)
                    if not mc.check_user(user, ""):
                        continue
                elif request == "+":
                    profile = vks.search_user(user)
                    if profile is None:
                        vkm.write_notfound(user_id)
                    else:
                        photos = vks.search_photos(profile)
                        vkm.write_match(user_id, profile, photos)
                else:
                    vkm.write_welcome_message(user_id)
    except Exception:
        logging.error("Error occurred", traceback.print_exc())
