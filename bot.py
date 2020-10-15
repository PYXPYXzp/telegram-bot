import os
import datetime

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from openweather_api import CurrentOpenWeatherApi, ForecastOpenWeatherApi
from exchange.exchanger import ExchangeRates

CHAT_ID = '149548428'
TOKEN = os.environ.get('BOT_TOKEN')

time = datetime.time(5)



def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


def current_weather(bot, update):
    weather = CurrentOpenWeatherApi().get_current_weather()
    bot.send_message(chat_id=update.message.chat_id, text=weather)


def get_currency(bot, update):
    average_currency = ExchangeRates(api='privat').get_current_exchange_rate()
    bot.send_message(chat_id=update.message.chat_id, text=average_currency)


def forecast_weather(bot, update):
    forecast = ForecastOpenWeatherApi().get_forecast_message()
    bot.send_message(chat_id=update.message.chat_id, text=forecast)


def unknown(bot, update):
    print(update.message)
    bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")


def weather_queue(bot, job):
    weather = CurrentOpenWeatherApi().get_current_weather()
    forecast = ForecastOpenWeatherApi().get_forecast_message()
    bot.send_message(chat_id=CHAT_ID, text=weather + '\n' + forecast)


def currency_queue(bot, job):
    average_currency = ExchangeRates(api='privat').get_current_exchange_rate()
    bot.send_message(chat_id=CHAT_ID, text=average_currency)


def main():
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('weather', current_weather))
    dispatcher.add_handler(CommandHandler('forecast', forecast_weather))
    dispatcher.add_handler(CommandHandler('exchange', get_currency))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    updater.start_polling()
    job_queue = updater.job_queue
    job_queue.run_daily(weather_queue, time)
    job_queue.run_daily(currency_queue, time)


if __name__ == '__main__':
    main()
