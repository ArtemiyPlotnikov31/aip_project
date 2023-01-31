import pytest
from unittest.mock import AsyncMock
import aiogram
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

import tg_bot


@pytest.mark.asyncio
async def test_start_command():
    # клавиатура
    button_temperature = KeyboardButton(text='/Temperature')
    button_details = KeyboardButton(text='/Details')
    button_time = KeyboardButton(text='/Time')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(button_temperature)
    keyboard.add(button_details)
    keyboard.add(button_time)
    # мокаем бота
    state = AsyncMock()
    message = AsyncMock()
    message.text = "/start"
    # запускаем тест
    await tg_bot.start_command(message, state)
    # проверяем
    message.reply.assert_called_once_with(
        "Привет, я помогу тебе узнать погоду в твоем городе! ⛈️\n\n\
        🌡️ Чтобы узнать температуру в своем городе нажми /Temperature\n\
        📝 Чтобы узнать подробный прогноз, нажми /Details\n\
        🕑 Чтобы узнать продолжительность дня, нажми /Time",
        reply_markup=keyboard)


@pytest.mark.asyncio
async def test_temperature_command():
    # мокаем бота
    state = AsyncMock()
    message = AsyncMock()
    message.text = "/Temperature"
    aiogram.bot.Bot.send_message = AsyncMock()
    # запускаем тест
    await tg_bot.get_weather(message, state)
    # проверяем
    aiogram.bot.Bot.send_message.assert_called_once_with(
        message.chat.id,
        "🌆 Введите название города:")


@pytest.mark.asyncio
async def test_details_command():
    # мокаем бота
    state = AsyncMock()
    message = AsyncMock()
    message.text = "/Details"
    aiogram.bot.Bot.send_message = AsyncMock()
    # запускаем тест
    await tg_bot.get_details(message, state)
    # проверяем
    aiogram.bot.Bot.send_message.assert_called_once_with(
        message.chat.id,
        "🌆 Введите название города:")


@pytest.mark.asyncio
async def test_time_command():
    # мокаем бота
    state = AsyncMock()
    message = AsyncMock()
    message.text = "/Time"
    aiogram.bot.Bot.send_message = AsyncMock()
    # запускаем тест
    await tg_bot.get_time(message, state)
    # проверяем
    aiogram.bot.Bot.send_message.assert_called_once_with(
        message.chat.id,
        "🌆 Введите название города:")


@pytest.mark.asyncio
async def test_get_temp_by_city():
    # мокаем бота
    state = AsyncMock()
    message = AsyncMock()
    message.text = "Moscow"
    aiogram.bot.Bot.send_message = AsyncMock()
    # запускаем тест
    await tg_bot.get_temp_by_city(message, state)
    # проверяем
    message.reply.assert_called_once()


@pytest.mark.asyncio
async def test_get_temp_by_city_bad():
    # мокаем бота
    state = AsyncMock()
    message = AsyncMock()
    message.text = "123456"
    aiogram.bot.Bot.send_message = AsyncMock()
    # запускаем тест
    await tg_bot.get_temp_by_city(message, state)
    # проверяем
    message.reply.assert_called_once_with("Проверьте правильность написания названия города.")


@pytest.mark.asyncio
async def test_get_details_by_city():
    # мокаем бота
    state = AsyncMock()
    message = AsyncMock()
    message.text = "Moscow"
    aiogram.bot.Bot.send_message = AsyncMock()
    # запускаем тест
    await tg_bot.get_details_by_city(message, state)
    # проверяем
    message.reply.assert_called_once()


@pytest.mark.asyncio
async def test_get_details_by_city_bad():
    # мокаем бота
    state = AsyncMock()
    message = AsyncMock()
    message.text = "123456"
    aiogram.bot.Bot.send_message = AsyncMock()
    # запускаем тест
    await tg_bot.get_details_by_city(message, state)
    # проверяем
    message.reply.assert_called_once_with("Проверьте правильность написания названия города.")


@pytest.mark.asyncio
async def test_get_time_by_city():
    # мокаем бота
    state = AsyncMock()
    message = AsyncMock()
    message.text = "Moscow"
    aiogram.bot.Bot.send_message = AsyncMock()
    # запускаем тест
    await tg_bot.get_time_by_city(message, state)
    # проверяем
    message.reply.assert_called_once()


@pytest.mark.asyncio
async def test_get_time_by_city_bad():
    # мокаем бота
    state = AsyncMock()
    message = AsyncMock()
    message.text = "123456"
    aiogram.bot.Bot.send_message = AsyncMock()
    # запускаем тест
    await tg_bot.get_time_by_city(message, state)
    # проверяем
    message.reply.assert_called_once_with("Проверьте правильность написания названия города.")