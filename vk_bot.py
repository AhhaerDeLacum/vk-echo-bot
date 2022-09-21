# !/usr/bin/vk_env
import random
import logging
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from _token import token
from _token import group_id
""" В отдельном файле _token хранится значения token и group_id !
"""
log = logging.getLogger('bot')


def configure_logging():
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%d-%m-%Y %H:%M:%S"))
    stream_handler.setLevel(logging.DEBUG)
    log.addHandler(stream_handler)

    file_handler = logging.FileHandler('bot.log', 'w', 'utf8')
    file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%d-%m-%Y %H:%M:%S"))
    file_handler.setLevel(logging.DEBUG)
    log.addHandler(file_handler)
    log.setLevel(logging.DEBUG)#Общий уровень DEBUG



# logging.

class Bot:
    def __init__(self, group_id, token):
        self.group_id = group_id
        self.token = token
        self.vk = vk_api.VkApi(token=token)
        self.vk_long_poll = VkBotLongPoll(self.vk, self.group_id)

        self.api_vk = self.vk.get_api()

    def run(self):
        for event in self.vk_long_poll.listen():
            #print(event) Позволяет лучше понять к чему обращаться
            try:
                self.on_event(event)
            except Exception as exc:
                log.exception('Ошибка в обработке события')

    def on_event(self, event):
        if event.type == VkBotEventType.MESSAGE_NEW:
            log.debug('Отправили это же сообщение обратно этому пользователю')
            self.api_vk.messages.send(
                message=event.message.text,#message.text,
                random_id=random.randint(0, 2 ** 20),
                peer_id=event.message.peer_id,
            )
        else:
            log.info("Неизвестное событие - %s", event.type)
            # print("Неизвестное событие - ", event.type)





if __name__ == '__main__':
    configure_logging()
    bot = Bot(group_id, token)
    bot.run()
