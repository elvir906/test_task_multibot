from aiogram.types import InlineKeyboardMarkup
from aiogram.types.inline_keyboard import InlineKeyboardButton

# список из пунктов меню
kbd_items = [
        'Посмотреть погоду',
        'Конвертировать валюту',
        'Картинка с животным',
        'Создать опрос в чате'
    ]

# словарь с городами их id в системе OpenWeatherMap
cities = {
    'Санкт-Петербург': 498817,
    'Москва': 524894,
    'Уфа': 479561,
    'Казань': 551487,
    'Ижевск': 554840,
    'Нижний Новгород': 520555,
    'Владивосток': 2013348,
    'Нефтекамск': 522942
}


def func_choice_kbd():
    """Клавиатура на выбор функции."""
    # формирую кнопки
    buttons = [
        InlineKeyboardButton(
            text=kbd_items[i],
            callback_data=kbd_items[i]
        ) for i in range(len(kbd_items))
    ]

    # формирую клавиатуру
    keyboard = InlineKeyboardMarkup()
    for item in buttons:
        keyboard.row(item)
    return keyboard


def city_choice_kbd():
    """Клавиатура на выбор города."""
    buttons = [
        InlineKeyboardButton(
            text=key,
            callback_data=value
        ) for key, value in cities.items()
    ]

    keyboard = InlineKeyboardMarkup()
    keyboard.add(*buttons)
    return keyboard


def poll_kbd(data):
    """Клавиатура на опрос"""

    answer_1 = data.get('answer_1')
    answer_2 = data.get('answer_2')
    answer_3 = data.get('answer_3')

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text=answer_1, callback_data='1'))
    keyboard.add(InlineKeyboardButton(text=answer_2, callback_data='2'))
    keyboard.add(InlineKeyboardButton(text=answer_3, callback_data='3'))

    return keyboard
