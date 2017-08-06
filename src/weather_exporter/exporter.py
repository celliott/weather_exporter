#!/usr/bin/env python
# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2

import requests, re, time, options
from prometheus_client import start_http_server, Gauge
from geopy.geocoders import Nominatim
try:
  from functools import lru_cache
except ImportError:
  from backports.functools_lru_cache import lru_cache

@lru_cache()
def get_location(city):
  location = Nominatim(timeout=options['geocode_timeout']).geocode(city)
  return location

class WeatherExporter:
  def __init__(self,options):
    self.guages={}
    self.weather={}

  def get_weather(self,city):
    location = get_location(city)
    url = "{0}/{1},{2}".format(options['dark_sky_api_url'],location.latitude,location.longitude)
    try:
      response = requests.get(url).json()
      self.weather["{}".format(city)] = response
    except requests.exceptions.RequestException as e:
      print e

  def to_underscore(self,str):
    return re.sub("([A-Z])", "_\\1", str).lower().lstrip("_")

  def add_guage(self,latest_weather):
    for key, value in latest_weather.iteritems():
      name = self.to_underscore(key)
      self.guages["{}".format(key)] = Gauge("weather_{}".format(name), "Current Weather {}".format(name), ['city'])

  def report_metrics(self,city):
    self.weather["{}".format(city)] = {}
    self.get_weather(city)
    latest_weather = self.weather["{}".format(city)]
    try:
      self.add_guage(latest_weather['currently'])
    except: pass

    try:
      for key, value in latest_weather['currently'].iteritems():
        if type(value) == int or type(value) == float:
          self.guages["{}".format(key)].labels(city).set(value)
    except: pass

if __name__ == "__main__":
  options = options.get()
  exporter = WeatherExporter(options)
  start_http_server(options['endpoint_port'])
  while True:
    for city in options['cities'].split(','):
      exporter.report_metrics(city)
    time.sleep(options['scrape_interval'])
