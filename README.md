# weather_exporter

A docker container for running a prometheus weather_exporter using Dark Sky API. It exports current weather for a list of cities. [Demo](https://github.com/celliott/telemetry)

## Grafana Dashboard
[Weather](https://grafana.com/dashboards/2441)

## Usage

#### Export DARK_SKY_API_KEY
```
$ export DARK_SKY_API_KEY=<dark_ski_api_key>
```

#### Set Env Vars in .env
```
# ENV Variables
ENDPOINT_PORT=9265
CITIES="nyc,portland"
DARK_SKY_API_INTERVAL=10000
```

#### Run container
```bash
$ make run
```

#### Prometheus Endpoint

http://localhost:9265

#### Prometheus config
```yaml
scrape_configs:
          
  - job_name: weather_exporter
    metrics_path: /
    static_configs:

      - targets:
        - '172.17.0.1:9265'
        labels:
          alias: 'weather-exporter'
 ```

#### To build and push container docker hub
```bash
$ make build && make push
```
