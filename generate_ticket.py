from io import BytesIO

import requests
from PIL import Image, ImageDraw, ImageFont

PATH_FOR_TICKET_PNG = 'files/ticket_to_event.png'
FONT_PATH = 'files/Roboto-Regular.ttf'
FONT_SIZE = 20
BLACK_COLOR = (0, 0, 0, 255)
NAME_OFFSET = (230, 230)
EMAIL_OFFSET = (230, 275)
AVATAR_SIZE = (100, 100)
AVATAR_OFFSET = (80, 220)




def generate_ticket(name, email):

    base = Image.open(PATH_FOR_TICKET_PNG).convert('RGBA')
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    draw = ImageDraw.Draw(base)
    draw.text(NAME_OFFSET, name, font=font, fill=BLACK_COLOR)
    draw.text(EMAIL_OFFSET, email, font=font, fill=BLACK_COLOR)

    response = requests.get(url=f'https://api.multiavatar.com/{email}.png')
    avatar_file_like = BytesIO(response.content)
    avatar = Image.open(avatar_file_like)
    avatar = avatar.resize(AVATAR_SIZE)

    base.paste(avatar, AVATAR_OFFSET, )

    temp_file = BytesIO()
    base.save(temp_file, 'png')
    temp_file.seek(0)

    """
    Альтернативное сохранение
    # with open('files/ticket-example.png', 'wb') as file:
    #     base.save(file, 'png')
    """

    #base.show()-просто открывает получаемый файл в проводнике
    return temp_file



# generate_ticket('name', 'email') использоваль для проверки