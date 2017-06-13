FROM python:2.7
MAINTAINER celliott

# install unix dependencies
RUN apt-get update && \
  apt-get autoremove -y && \
  apt-get install -y \
    supervisor \
    python-pip

# install python dependencies
ADD ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# add supervisor config
ADD ./config/supervisor/* /etc/supervisor/conf.d/

# add weather_exporter script
ADD ./src/weather_exporter /opt/weather_exporter
RUN chmod +x /opt/weather_exporter/*

# run supervisor
CMD ["/usr/bin/supervisord", "-n"]
