FROM python:2.7
MAINTAINER celliott

# install python dependencies
ADD ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# add json config
ADD ./config/sample.json /etc/weather_exporter/config.json

# add weather_exporter script
ADD ./src/weather_exporter /opt/weather_exporter
RUN chmod +x /opt/weather_exporter/*

ENTRYPOINT ["/opt/weather_exporter/exporter.py", "--config=/etc/weather_exporter/config.json"]
