import requests
from datetime import datetime
import os

class BaseOpenWeatherApi:

	API_KEY = os.environ.get('OPENWEATHER_KEY')
	CITY_ID = '687700'
	url = 'http://api.openweathermap.org/data/2.5/{}'
	
	def __init__(self):
		self.params = {'id': self.CITY_ID, 'units':'metric', 'APPID': self.API_KEY, 'lang': 'ru'}

	def get_temp(self, json_weather):
		try:
			temp = json_weather['main']['temp']
		except KeyError:
			return 'no temperature'
		return temp

	def get_description(self, json_weather):
		try:
			description = json_weather['weather'][0]['description']
		except (KeyError, IndexError) as e:
			return e
		return description

	def get_datetime(self, json_weather):
		ts = json_weather['dt']
		return datetime.fromtimestamp(ts).time()

	def parse_weather(self, json_weather):
		temp = self.get_temp(json_weather)
		description = self.get_description(json_weather)
		return temp, description
	
	def generate_message(self):
		pass


class CurrentOpenWeatherApi(BaseOpenWeatherApi):
	CURRENT_WEATHER_URL = 'weather'
	MESSAGE = 'Температура за окном {temperature}, {description}'

	def get_current_weather(self):
		json_weather = requests.get(self.url.format(self.CURRENT_WEATHER_URL), params=self.params).json()
		if json_weather.get('cod') != 200:
			return "No weather"
		return self.generate_message(json_weather)
	
	def generate_message(self, json_weather):
		temp = self.get_temp(json_weather)
		description = self.get_description(json_weather)
		return self.MESSAGE.format(temperature=temp, description=description)


class ForecastOpenWeatherApi(BaseOpenWeatherApi):
	FORECAST_WEATHER_URL = 'forecast'
	NUMBER_OF_LINES = 4
	MESSAGE = 'В {time} ожидается {temp}, {description}'

	def __init__(self):
		super(ForecastOpenWeatherApi, self).__init__()
		self.params.update({'cnt':self.NUMBER_OF_LINES})
		self.result = []

	def get_forecast_weather(self):
		json_forecast = requests.get(self.url.format(self.FORECAST_WEATHER_URL), params=self.params).json()
		if json_forecast.get('cod') != '200':
			return "No forecast weather"
		for json_weather in json_forecast['list']:
			self.result.append(self.generate_message(json_weather))
		return '\n'.join(self.result)

	def generate_message(self, json_weather):
		temp = self.get_temp(json_weather)
		description = self.get_description(json_weather)
		time = self.get_datetime(json_weather)
		return self.MESSAGE.format(time=time, temp=temp, description=description)


