# !/usr/bin/vk_env
import random
import logging

import handlers
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


class UserState:
    """Состояние пользователя внутри сценария """
    def __init__(self, scenario_name, step_name, context=None):
        self.scenario_name = scenario_name
        self.step_name = step_name
        self.context = context or {}


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
        self.user_states = dict() # user_id -> UserState

    def run(self):
        """Запуск бота"""
        for event in self.vk_long_poll.listen():
            #print(event) #Позволяет лучше понять к чему обращаться

            # print(event.object.from_id)
            try:
                self.on_event(event)
            except Exception as exc:
                log.exception('Ошибка в обработке события')

    def on_event(self, event):
        """Отправляет сообщение назад, если это текст

        :param event: VkBotMessageEvent object
        :return: None
        """
        if event.type != VkBotEventType.MESSAGE_NEW:
            log.info('Мы пока не умеем отрабатывать сообщение такого типа', event.type)
            return

        message = event.object['message']
        # peer_id = message['peer_id']
        # text = message['text']
        user_id = message['peer_id']#event.object.peer_id #event.message.peer_id, !!!!!!!
        text = message['text'].lower()#event.object.text #event.message.text!!!!!!!!!!
        if user_id in self.user_states:
            # continue scenario
            text_to_send = self.continue_scenario(user_id, text)
        else:
            #search intent
            for intent in settings.INTENTS:
                log.debug(f'User gets {intent}')
                if any(token in text for token in intent['tokens']):
                    #run intent
                    if intent['answer']:
                        text_to_send = intent['answer']
                    else:
                        text_to_send = self.start_scenario(user_id, intent['scenario'])
                    break
            else:
                text_to_send = settings.DEFAULT_ANSWER

        self.api_vk.messages.send(
            message=text_to_send,  # message.text,
            random_id=random.randint(0, 2 ** 20),
            peer_id=user_id #event.message.peer_id,
        )

    def start_scenario(self, user_id, scenario_name):
        scenario = settings.SCENARIOS[scenario_name]
        firs_step = scenario['first_step']
        step = scenario['steps'][firs_step]
        text_to_send = step['text']
        self.user_states[user_id] = UserState(scenario_name=scenario_name, step_name=firs_step)
        return text_to_send

    def continue_scenario(self, user_id, text):
        state = self.user_states[user_id]
        steps = settings.SCENARIOS[state.scenario_name]['steps']
        step = steps[state.step_name]
        handler = getattr(handlers, step['handler'])
        if handler(text=text, context=state.context):
            # new step
            next_step = steps[step['next_step']]
            text_to_send = next_step['text'].format(**state.context)
            if next_step['next_step']:
                # switch to next step
                state.step_name = step['next_step']
            else:
                # finish scenario

                log.info("Зарегистрирован {name} {email}".format(**state.context))
                self.user_states.pop(user_id)
        else:
            #retry current step
            text_to_send = step['failure_text'].format(**state.context)

        return text_to_send
    # def continue_scenario(self, text, state, user_id):
    #     steps = settings.SCENARIOS[state.scenario_name]['steps']
    #     step = steps[state.step_name]
    #
    #     handler = getattr(handlers, step['handler'])
    #     # print('2', state.context, type(state.context))
    #     if handler(text=text, context=state.context):
    #         next_step = steps[step['next_step']]
    #         # text_to_send = next_step['text'].format(**state.context)
    #         # self.send_text(text_to_send, user_id)
    #         self.send_step(next_step, user_id, text, state.context)
    #         if next_step['next_step']:
    #             state.step_name = step['next_step']
    #         else:
    #             # log.debug(f'Зарегистрирован {name} {email}'.format(**state.context))
    #             Registration(name=state.context['name'], email=state.context['email'])
    #             state.delete()
    #     else:
    #         text_to_send = step['failure_text'].format(**state.context)
    #         self.send_text(text_to_send, user_id)
            # search intent
            # print("Неизвестное событие - ", event.type)

            # if event.type == VkBotEventType.MESSAGE_NEW:
            #     log.debug('Отправили это же сообщение обратно этому пользователю')
            #     self.api_vk.messages.send(
            #         message=event.message.text,  # message.text,
            #         random_id=random.randint(0, 2 ** 20),
            #         peer_id=event.message.peer_id,
            #     )
            # else:
            #     log.info("Неизвестное событие - %s", event.type)
            #     # print("Неизвестное событие - ", event.type)


if __name__ == '__main__':
    configure_logging()
    bot = Bot(settings.GROUP_ID, settings.TOKEN)
    bot.run()
