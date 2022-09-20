# !/usr/bin/vk_env
import random
import vk_api
import vk_api.bot_longpoll
from _token import token
from _token import group_id
""" В отдельном файле _token хранится значения token и group_id !
"""


class Bot:
    def __init__(self, group_id, token):
        self.group_id = group_id
        self.token = token
        self.vk = vk_api.VkApi(token=token)
        self.vk_long_poll = vk_api.bot_longpoll.VkBotLongPoll(self.vk, self.group_id)

        self.api_vk = self.vk.get_api()

    def run(self):
        for event in self.vk_long_poll.listen():
            print('Произошло некое событие')
            #print(event) Позволяет лучше понять к чему обращаться
            try:
                self.on_event(event)
            except Exception as exc:
                print(exc)

    def on_event(self, event):
        if event.type == vk_api.bot_longpoll.VkBotEventType.MESSAGE_NEW:
            self.api_vk.messages.send(
                message=event.message.text,#message.text,
                random_id=random.randint(0, 2 ** 20),
                peer_id=event.message.peer_id,
            )
        else:
            print("Неизвестное событие - ", event.type)





if __name__ == '__main__':
    bot = Bot(group_id, token)
    bot.run()
