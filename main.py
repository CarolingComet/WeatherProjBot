import asyncio
import logging
import os

import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')


bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

def get_weather(city: str) -> dict:
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()
    return data


@dp.message(Command('start'))
async def send_welcome(message: types.Message):
    await message.answer("Привет! Отправь мне название города, чтобы узнать текущую погоду.")

@dp.message()
async def send_weather(message: types.Message):
    city = message.text
    weather_data = get_weather(city)

    if weather_data['cod'] == '404':
        await message.answer("Город не найден. Пожалуйста, попробуйте еще раз.")
    else:
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        description = weather_data['weather'][0]['description']
        response = f"Погода в {city}:\nТемпература: {temperature}°C\nВлажность: {humidity}%\nОписание: {description}"
        await message.answer(response)


async def main():
    await dp.start_polling(bot, skip_updates=True)

if __name__ == '__main__':
    asyncio.run(main())
