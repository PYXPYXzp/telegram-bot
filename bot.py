import os
import datetime

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging_bot

from openweather_api import CurrentOpenWeatherApi, ForecastOpenWeatherApi
from currency import Currency

TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = '149548428'

updater = Updater(token=TOKEN)

time = datetime.time(8)

dispatcher = updater.dispatcher


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


def current_weather(bot, update):
	weather = CurrentOpenWeatherApi().get_current_weather()
	bot.send_message(chat_id=update.message.chat_id, text=weather)


def get_currency(bot, update):
    average_currency = Currency().get_average_currency()
    bot.send_message(chat_id=update.message.chat_id, text=average_currency)


def forecast_weather(bot, update):
    forecast = ForecastOpenWeatherApi().get_forecast_weather()
    bot.send_message(chat_id=update.message.chat_id, text=forecast)


def unknown(bot, update):
    print(update.message)
    bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")

start_handler = CommandHandler('start', start)
current_weather_handler = CommandHandler('weather', current_weather)
forecast_weather_handler = CommandHandler('forecast', forecast_weather)
currency_handler = CommandHandler('currency', get_currency)
unknown_handler = MessageHandler(Filters.command, unknown)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(current_weather_handler)
dispatcher.add_handler(forecast_weather_handler)
dispatcher.add_handler(currency_handler)
dispatcher.add_handler(unknown_handler)

def weather_queue(bot, job):
    weather = CurrentOpenWeatherApi().get_current_weather()
    forecast = ForecastOpenWeatherApi().get_forecast_weather()
    bot.send_message(chat_id=CHAT_ID, text=weather + '\n' + forecast)

def currency_queue(bot, job):
    average_currency = Currency().get_average_currency()
    bot.send_message(chat_id=CHAT_ID, text=average_currency)


job_queue = updater.job_queue
job_queue.run_daily(weather_queue, time)
job_queue.run_daily(currency_queue, time)


updater.start_polling()