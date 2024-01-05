import telebot
import requests
from telebot import types
import json
from dotenv import load_dotenv
import os
load_dotenv()
bot = telebot.TeleBot(os.getenv('TOKEN'))
API = '5f11ae1f44349681d43e4a87f565e906'

@bot.message_handler(commands = ['start'])
def start (message):
    markup  = types.ReplyKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Сегодня")
    markup.row(btn1)
    btn2 = types.InlineKeyboardButton("Завтра")
    markup.row(btn2)
    btn3 = types.InlineKeyboardButton("На 5 дней")
    markup.row(btn3)
    bot.send_message(message.chat.id, 'Приветствую,'
                                      'на какой день вас интересует прогноз погоды?'
                     ,reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "Сегодня")
def get_weather_today(message):
    bot.send_message(message.chat.id,'Напишите название города')



@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric&lang=ru')
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data["main"]["temp"]
        feel_temp = data["main"]["feels_like"]
        des = data['weather'][0]['description']
        bot.reply_to(message, f'На улице {des}, температура {temp}°C, ощущается как {feel_temp}°C.')
        if 'облачно с прояснениями' in des or 'небольшая облачность' in des:
            image_path = 'foggy-day.png'  # Путь к изображению
            image = open(image_path, 'rb')
            bot.send_photo(message.chat.id, image)
        elif 'пасмурно' in des or 'переменная облачность' in des:
            image_path = 'cloudy-day.png'
            image = open(image_path, 'rb')
            bot.send_photo(message.chat.id, image)
        elif 'дождь' in des:
            image_path = 'rain-drops.png'
            image = open(image_path, 'rb')
            bot.send_photo(message.chat.id, image)
        elif 'ясно' in des:
            image_path = 'sun.png'
            image = open(image_path, 'rb')
            bot.send_photo(message.chat.id, image)
        elif 'небольшой снег' in des:
            image_path = 'snowfall.png'
            image = open(image_path, 'rb')
            bot.send_photo(message.chat.id, image)


    else:
        bot.reply_to(message, 'Не удалось получить данные о погоде. Проверьте название города.')


bot.polling(none_stop=True)
