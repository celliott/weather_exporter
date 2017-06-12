FROM celliott/base:latest
MAINTAINER celliott

# Install unix dependencies
RUN apt-get update && \
  apt-get autoremove -y && \
  apt-get install -y \
    vim \
    supervisor

# Install python dependencies
RUN pip install \
  prometheus_client \
  requests \
  redis \
  geopy

# Add supervisor config
ADD ./config/supervisor/* /etc/supervisor/conf.d/

# Add hl-site-check script
ADD ./src/weather_exporter /weather_exporter
RUN chmod +x /weather_exporter/*

CMD ["/usr/bin/supervisord", "-n"]
