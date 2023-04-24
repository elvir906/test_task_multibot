from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, MediaGroup, Message
from decouple import config

from animal import get_new_image
from answ_txts import msg_txts as mt
from exchange import convert_currency_erapi as c
from states import Exchange, Survey, WeatherInfo
from utils import city_choice_kbd, func_choice_kbd, poll_kbd
from weather import get_weather

GROUP_CHAT_ID = config('GROUP_CHAT_ID')
bot = Bot(token=config('TELEGRAM_TOKEN'))

dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def start(message: Message):
    """
    Хэндлер на команду '/start'. Метод выводит приветствие и клавиатуру
    на выбор функции бота.
    """
    await message.answer(
        text=mt.greeting(user_name=message.from_user.first_name),
        parse_mode='Markdown',
        reply_markup=func_choice_kbd()
    )


@dp.callback_query_handler(text='Посмотреть погоду')
async def weather_info_step_1(callback: CallbackQuery):
    """Хэндлер на команду 'Посмотреть погоду'."""

    await callback.message.answer(
        text='Выбери город:',
        reply_markup=city_choice_kbd()
    )
    await WeatherInfo.step2.set()


@dp.callback_query_handler(state=WeatherInfo.step2)
async def weather_info_step_2(callback: CallbackQuery, state: FSMContext):
    """Хэндлер на выбор города. Вывод погоды по этому городу"""

    weather = get_weather(city_id=callback.data)
    await callback.message.edit_text(
        text=weather,
        parse_mode='Markdown',
        reply_markup=func_choice_kbd()
    )
    await state.finish()


@dp.callback_query_handler(text='Конвертировать валюту')
async def exchange_step_1(callback: CallbackQuery):
    """Хэндлер на команду 'Конвертировать валюту'."""

    await callback.message.answer(text=mt.on.get('cur_input'))
    await Exchange.step2.set()


@dp.message_handler(state=Exchange.step2)
async def exchange_step_2(messsage: Message, state: FSMContext):
    """
    Хэндлер на строку введённых данных о валютах и количеству.
    Вызов метода для конвертации
    """
    string = messsage.text.split()
    try:
        amount = float(string[0])
        source_cur = string[1].upper()
        destination_cur = string[2].upper()

        convertation_res = c(
            amount=amount,
            dst=destination_cur,
            src=source_cur
        )

        await messsage.answer(
            text=f'На {convertation_res[0].date().strftime("%d.%m.%Y")}:\n'
            + f'{amount} {source_cur} = '
            + f'{convertation_res[1]} {destination_cur}',
            reply_markup=func_choice_kbd()
        )
        await state.finish()
    except Exception as e:
        await messsage.answer(
            text='К сожадению, ты ошибся с водом данных.\n\n'
            + '*Введи заново.*\n\n'
            + 'Следует вводить *три* значения по порядку через пробел: '
            + 'количестово (числовое значение), конвертируемую валюту, '
            + 'исходную валюту.\n'
            + 'Так же используйте официальные обозначению валют.\n'
            + f'Ошибка: {e}',
            parse_mode='Markdown'
        )
        await Exchange.step2.set()


@dp.callback_query_handler(text='Картинка с животным')
async def get_animal_image(callback: CallbackQuery, state: FSMContext):
    """Хэндлер на команду 'Картинка с животным'."""
    album = MediaGroup()
    album.attach_photo(
        get_new_image(),
        caption='Милый котик, не правда ли?'
    )
    await callback.message.answer_media_group(media=album)
    await callback.message.answer(text='Меню:', reply_markup=func_choice_kbd())
    await state.finish()


# Обработка команды 'Создать опрос в чате' для начала опроса
@dp.callback_query_handler(text='Создать опрос в чате')
async def start_survey(callback: CallbackQuery):
    await callback.message.edit_text(text='Введите вопрос для опроса')
    await Survey.question.set()


# Обработка вопроса и переход к следующему состоянию
@dp.message_handler(state=Survey.question)
async def answer_question_1(message: Message, state: FSMContext):
    await state.update_data(question=message.text)
    await message.answer(text='Введите первый вариант ответа')
    await Survey.answer1.set()


# Обработка ответа и переход к следующему состоянию
@dp.message_handler(state=Survey.answer1)
async def answer_question_2(message: Message, state: FSMContext):
    await state.update_data(answer_1=message.text)
    await message.answer(text='Введите второй вариант ответа')
    await Survey.answer2.set()


# Обработка ответа и переход к следующему состоянию
@dp.message_handler(state=Survey.answer2)
async def answer_question_3(message: Message, state: FSMContext):
    await state.update_data(answer_2=message.text)
    await message.answer(text='Введите третий вариант ответа')
    await Survey.answer3.set()


# Обработка ответа и завершение опроса
@dp.message_handler(state=Survey.answer3)
async def read_answer_3(message: Message, state: FSMContext):
    await state.update_data(answer_3=message.text)
    await message.answer(
        text='Отправка опроса в чат произошла.',
        reply_markup=func_choice_kbd()
    )
    await send_survey(message, state)


# Отправка опроса в чат
async def send_survey(message: Message, state: FSMContext):
    data = await state.get_data()
    question = data.get('question')

    await bot.send_message(
        chat_id=GROUP_CHAT_ID,
        text=question,
        reply_markup=poll_kbd(data)
    )
    await state.finish()


def main():
    """
    Запуск бота.
    """
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()
