from aiogram.dispatcher.filters.state import State, StatesGroup


class WeatherInfo(StatesGroup):
    """
    Классы с состояниями опросов. Нужны для правильной последовательности
    при работе с вопросами-ответами.
    """
    step2 = State()


class Exchange(StatesGroup):
    step2 = State()


class Survey(StatesGroup):
    question = State()
    answer1 = State()
    answer2 = State()
    answer3 = State()
