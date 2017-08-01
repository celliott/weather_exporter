#!/usr/bin/env python

import os

def get():
  dark_sky_api_uri = os.getenv('DARK_SKY_API_URI', 'https://api.darksky.net/forecast')
  dark_sky_api_key = os.getenv('DARK_SKY_API_KEY')
  if not dark_sky_api_key:
    print "Unable to start; make sure to export your api key. See readme"
    exit(1)

  return {
    'dark_sky_api_url': "{0}/{1}".format(dark_sky_api_uri,dark_sky_api_key),
    'scrape_interval': int(os.getenv('SCRAPE_INTERVAL', 600)),
    'endpoint_port': int(os.getenv('ENDPOINT_PORT', 9265)),
    'cities': os.getenv('CITIES', "nyc,tokyo,vancouver,lima,london,shanghai"),
    'geocode_timeout': int(os.getenv('GEOCODE_TIMEOUT', 10)),
  }