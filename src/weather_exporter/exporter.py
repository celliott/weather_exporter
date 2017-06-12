#!/usr/bin/python

import requests, re, time, os
from prometheus_client import start_http_server, Gauge
from geopy.geocoders import Nominatim

class WeatherExporter:
  def __init__(self):
    self.get_options()
    self.guages={}
    self.weather={}

  def get_options(self):
    dark_sky_api_key = os.getenv('DARK_SKY_API_KEY')
    if not dark_sky_api_key:
      print "Unable to start; make sure to export your api key. See readme"
      exit(1)
    dark_sky_api_uri = os.getenv('DARK_SKY_API_URI', 'https://api.darksky.net/forecast')
    self.options = {
      'dark_sky_api_url': "{}/{}".format(dark_sky_api_uri,dark_sky_api_key),
      'dark_sky_api_interval': int(os.getenv('DARK_SKY_API_INTERVAL', 600)),
      'endpoint_port': int(os.getenv('ENDPOINT_PORT', 9265)),
      'cities': os.getenv('CITIES', "nyc,tokyo,vancouver,lima,london"),
    }

  def get_location(self,city):
    geolocator = Nominatim()
    return geolocator.geocode(city)

  def get_weather(self,city):
    location = self.get_location(city)
    url = "{0}/{1},{2}".format(self.options['dark_sky_api_url'],location.latitude,location.longitude)
    response = requests.get(url).json()
    self.weather["{}".format(city)] = response

  def camel_to_snake(self,str):
    return re.sub("([A-Z])", "_\\1", str).lower().lstrip("_")

  def set_guages(self,city,latest_weather):
    try:
      for key, value in latest_weather.iteritems():
        name = self.camel_to_snake(key)
        self.guages["{}".format(key)] = Gauge("weather_{}".format(name), "Current Weather {}".format(name), ['city'])
    except: pass

  def get_metrics(self,city):
    try:
      latest_weather = self.weather["{}".format(city)]
      self.set_guages(city,latest_weather['currently'])
      for key, value in latest_weather['currently'].iteritems():
        if type(value) == int or type(value) == float:
          self.guages["{}".format(key)].labels(city).set(value)
    except: pass

if __name__ == "__main__":
  exporter = WeatherExporter()
  start_http_server(exporter.options['endpoint_port'])
  while True:
    for city in exporter.options['cities'].split(','):
      exporter.weather["{}".format(city)] = {}
      exporter.get_weather(city)
      exporter.get_metrics(city)
    time.sleep(exporter.options['dark_sky_api_interval'])
