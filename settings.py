GROUP_ID = 199970529
TOKEN = 'vk1.a.BZaUsDJf0sk9LNf6OS5XARAmNjtRRdYhEVnBFdwMIe9MNDHh-7BCL9QoTq8WOyKmpLl70WFR0bc4NaIi0RAQzbl-DdCzZteJcnjBSMzHufidz625RCDs4MXLGzhf6W79tTHpUcOA980vTcJn9talaGmVpX_HSPCpHAWZ4UMivS7nuWizUphjPOkvUUkDHVJI'
INTENTS = [
    {
        "name": "Дата проведения",
        "tokens": ("когда", "сколько", "дата", "дату", "Когда"),
        "scenario": None,
        "answer": "Мероприятие проводится 15-го октября,а начнется в 10 утра"
    },
    {
        "name": "Место проведения",
        "tokens": ("где", "место", "локация", "адрес", "метро" ),
        "scenario": None,
        "answer": "Мероприятие пройдет на Китай-городе"
    },
    {
        "name": "Регистрация",
        "tokens": ("регист", "добав", "рег" ),
        "scenario": "registration",
        "answer": None
    },
]
SCENARIOS = {
    "registration": {
        "first_step": "step1",
        "steps": {
            "step1": {
                "text": "Чтобы зарегистрироваться введите ваше имя. оно будет написано на бейдже",
                "failure_text": "Имя может состоять из 3-30 букв и дефиса. Попробуйте еще раз",
                "handler": "handler_name",
                "next_step": "step2"
            },
            "step2": {
                "text": "Введите email. мы отправим на него все данные",
                "failure_text": "В веденном адресе ошибка. Попробуйте еще раз",
                "handler": "handler_email",
                "next_step": "step3"
            },
            "step3": {
                "text": "Спасибо за регистрацию. Вот ваш билет",
                "image": "generate_ticket_handler",
                "failure_text": None,
                "handler": None,
                "next_step": None
            }
        }
    }
}
DEFAULT_ANSWER = 'Не могу на это ответить.' \
                 'Могу сказать когда и где пройдет конференция, а также зарегистрировать вас. Просто спросите.'
DB_CONFIG = dict(
    provider='postgres',
    user='postgres',
    password='279400',
    host='localhost',
    database='vk_chat_bot'
)