#!/usr/bin/env python
# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
import argparse
import json
import os
import sys

from urlparse import urlparse

# DEFAULT_OPTIONS is a dictionary of string keys and values representing
# defaultable commandline options.
DEFAULT_OPTIONS = {
  'dark_sky_api_uri': 'https://api.darksky.net/forecast',
  'dark_sky_api_key' : '',
  'scrape_interval': 600,
  'endpoint_port': 9265,
  'cities': 'nyc,tokyo,lima,london,shanghai',
  'geocode_timeout': 10,
  'units': 'us'
}

# PARSER is an instance of argparse.ArgumentParser.
PARSER = argparse.ArgumentParser(
  description='Prometheus exporter for weather reports from https://darksky.net')

# We add default options and enforce their type based on the default
# values in DEFAULT_OPTIONS
for option, default_val in DEFAULT_OPTIONS.iteritems():
  option_type = type(default_val)
  PARSER.add_argument("--{0}".format(option), type=option_type, help="default value: {0}".format(default_val))


# config files are a special case with no default value, so we add the
# commandline option manually
PARSER.add_argument("--config", type=argparse.FileType('r'))

def get():
  '''
  Fetches options from file, environment, and commandline
  commandline options are given priority, then environment, then file
  ```
  #> cat '{"foo": "c"}' > conf.json
  #> weather_exporter --config=conf.json
  // foo is 'c'

  #> env FOO=b
  #> weather_exporter --config=conf.json
  // foo is 'b'

  #> env FOO=b
  #> weather_exporter --config=conf.json --foo=a
  // foo is 'a'
  ```
  '''

  # fetch out environment options
  env_options = {k: os.getenv(k.upper()) for k in DEFAULT_OPTIONS.iterkeys()}
  # clear env options with null values
  env_options = {k: v for k, v in env_options.iteritems() if v}

  # fetch out commandline options
  cmdline_options = vars(PARSER.parse_args(sys.argv[1:]))
  # clear commandline options with null values
  cmdline_options = {k: v for k, v in cmdline_options.iteritems() if v}

  # fetch file options
  file_options = {}
  if 'config' in cmdline_options.keys():
    file_options = json.load(cmdline_options['config'])

  # merge down defaults < file < env < commandline
  final_options = DEFAULT_OPTIONS.copy()

  final_options.update(file_options)
  final_options.update(env_options)
  final_options.update(cmdline_options)

  if not final_options['dark_sky_api_key']:
    print "ERROR; NO API KEY FOUND. make sure to set your api key. See readme"
    exit(1)

  dark_sky_uri = urlparse(final_options['dark_sky_api_uri'])
  api_path = dark_sky_uri[2].strip()
  if api_path[-1] != '/':
    api_path += '/'

  final_options['dark_sky_api_url'] = "{0}://{1}{2}{3}".format(
                                        dark_sky_uri[0],
                                        dark_sky_uri[1],
                                        api_path,
                                        final_options['dark_sky_api_key'])

  return final_options
