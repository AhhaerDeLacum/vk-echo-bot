# !/usr/bin/vk_env
import random
import logging
import vk_api #TODO fix version
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
try:
    import settings
except ImportError:
    exit('Do cp settings.py.default settings.py and set token')

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
    """ Echo bot для vk.com

    Use version python 3.10
    """
    def __init__(self, group_id, token):
        """
        :param:group_id: group id из группы VK
        :param:token: секретный токен из этой же группы
        """
        self.group_id = group_id
        self.token = token
        self.vk = vk_api.VkApi(token=token)
        self.vk_long_poll = VkBotLongPoll(self.vk, self.group_id)

        self.api_vk = self.vk.get_api()

    def run(self):
        """Запуск бота"""
        for event in self.vk_long_poll.listen():
            #print(event) Позволяет лучше понять к чему обращаться
            try:
                self.on_event(event)
            except Exception as exc:
                log.exception('Ошибка в обработке события')

    def on_event(self, event):
        """Отправляет сообщение назад, если это текст

        :param event: VkBotMessageEvent object
        :return: None
        """
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
    bot = Bot(settings.GROUP_ID, settings.TOKEN)
    bot.run()
