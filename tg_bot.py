import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot, storage=MemoryStorage())


class WeatherType(StatesGroup):
    temperature = State()
    details = State()
    time = State()


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message, state: FSMContext):
    """Обработчик команды /start

    Args:
        message (types.Message): сообщение от пользователя
        state (FSMContext): состояние бота
    """
    button_temperature = KeyboardButton(text='/Temperature')
    button_details = KeyboardButton(text='/Details')
    button_time = KeyboardButton(text='/Time')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(button_temperature)
    keyboard.add(button_details)
    keyboard.add(button_time)
    await message.reply(
        "Привет, я помогу тебе узнать погоду в твоем городе! ⛈️\n\n\
        🌡️ Чтобы узнать температуру в своем городе нажми /Temperature\n\
        📝 Чтобы узнать подробный прогноз, нажми /Details\n\
        🕑 Чтобы узнать продолжительность дня, нажми /Time",
        reply_markup=keyboard)


@dp.message_handler(commands=["Temperature"])
async def get_weather(message: types.Message, state: FSMContext):
    """Обработчик команды /Temperature

    Args:
        message (types.Message): сообщение от пользователя
        state (FSMContext): состояние бота
    """
    await bot.send_message(message.chat.id, "🌆 Введите название города:")
    await state.set_state(WeatherType.temperature)


@dp.message_handler(commands=["Details"])
async def get_details(message: types.Message, state: FSMContext):
    """Обработчик команды /Details

    Args:
        message (types.Message): сообщение от пользователя
        state (FSMContext): состояние бота
    """
    await bot.send_message(message.chat.id, "🌆 Введите название города:")
    await state.set_state(WeatherType.details)


@dp.message_handler(commands=["Time"])
async def get_time(message: types.Message, state: FSMContext):
    """Обработчик команды /Time

    Args:
        message (types.Message): сообщение от пользователя
        state (FSMContext): состояние бота
    """
    await bot.send_message(message.chat.id, "🌆 Введите название города:")
    await state.set_state(WeatherType.time)


@dp.message_handler(state=WeatherType.temperature)
async def get_temp_by_city(message: types.Message, state: FSMContext):
    """Получение температуры в городе

    Args:
        message (types.Message): сообщение от пользователя c названием города
        state (FSMContext): состояние бота
    """
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data['name']
        cur_temp = data['main']['temp']

        await message.reply(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}]\n"
                            f"❄️ Температура в городе {city}: {cur_temp}C\n")
        await state.finish()

    except Exception as e:
        print(e)
        await message.reply("Проверьте правильность написания названия города.")
        await state.set_state(WeatherType.temperature)


@dp.message_handler(state=WeatherType.details)
async def get_details_by_city(message: types.Message, state: FSMContext):
    """Получение подробного прогноза погоды в городе

    Args:
        message (types.Message): сообщение от пользователя c названием города
        state (FSMContext): состояние бота
    """
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data['name']
        cur_temp = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']

        await message.reply(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}]\n"
                            f"❄️ Температура в городе {city}: {cur_temp}C\n"
                            f"💧 Влажность: {humidity}%\n"
                            f"🌬️ Скорость ветра: {wind} м/с\n"
                            f"🌡️ Давление: {pressure} мм.рт.ст.\n")
        await state.finish()

    except Exception as e:
        print(e)
        await message.reply("Проверьте правильность написания названия города.")
        await state.set_state(WeatherType.details)


@dp.message_handler(state=WeatherType.time)
async def get_time_by_city(message: types.Message, state: FSMContext):
    """Получение времени восхода и заката солнца в городе

    Args:
        message (types.Message): сообщение от пользователя c названием города
        state (FSMContext): состояние бота
    """
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data['name']
        sunrise_timestamp = data['sys']['sunrise']
        sunset_timestamp = data['sys']['sunset']

        sunrise_time = datetime.datetime.fromtimestamp(sunrise_timestamp)
        sunset_time = datetime.datetime.fromtimestamp(sunset_timestamp)

        await message.reply(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}]\n"
                            f"🌆 Город: {city}\n"
                            f"🌅 Восход солнца: {sunrise_time.strftime('%H:%M')}\n"
                            f"🌇 Закат солнца: {sunset_time.strftime('%H:%M')}\n")
        await state.finish()

    except Exception as e:
        print(e)
        await message.reply("Проверьте правильность написания названия города.")
        await state.set_state(WeatherType.time)


if __name__ == '__main__':
    executor.start_polling(dp)