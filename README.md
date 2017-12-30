# weather_exporter

A docker container for running a prometheus weather_exporter using Dark Sky API. It exports current weather for a list of cities. [Demo](https://github.com/celliott/telemetry)

## Grafana Dashboard
[Weather](https://grafana.com/dashboards/2441)

## Usage

### Configuration

`weather_exporter` can be configured via json file, environment, and/or commandline.
Configuration option names are the same across all methods. Environment variables _MUST BE CAPITALIZED_.

#### Configuration Options

 - `config`: path to a json config file.
 - `dark_sky_api_key`: API key to query with. _REQUIRED_.
 - `dark_sky_api_uri`: URL of the darksky.net api (version as of 10/10/2017). Defaults to `https://api.darksky.net/forecast`.
 - `scrape_interval`: how often to poll darksky.net for data in seconds. Defaults to `600` seconds.
 - `endpoint_port`: what port to expose `weather_exporter` on. Defaults to `9265`.
 - `cities`: comma-separated list of cities as understood by [`Nominatim`](https://wiki.openstreetmap.org/wiki/Nominatim). Defaults to "`nyc,tokyo,lima,london,shanghai`".
 - `geocode_timeout`: timeout in seconds on api calls to [`Nominatim`](https://wiki.openstreetmap.org/wiki/Nominatim). Defaults to `10` seconds.
 - `units`: unit of the weather data. See [Dark Sky API Docs](https://darksky.net/dev/docs#forecast-request) for a list of valid units. Defaults to `us` (imperial units).

### Simple Setup and Go

#### Export DARK_SKY_API_KEY
```
$ export DARK_SKY_API_KEY=<dark_ski_api_key>
```

#### Set Env Vars in .env
```
# ENV Variables
ENDPOINT_PORT=9265
CITIES=nyc,portland or,london
SCRAPE_INTERVAL=10000
```

#### Run container
```bash
$ make up
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

#### To build and push container to docker hub
```bash
$ make push
```

### Helm chart

#### Deploy

```bash
$ export DARK_SKY_API_KEY=<dark_ski_api_key>
$ make deploy
```

```
$ export POD_NAME=$(kubectl get pods --namespace weather-exporter -l "app=weather-exporter,release=weather-exporter" -o jsonpath="{.items[0].metadata.name}")

$ kubectl port-forward --namespace weather-exporter $POD_NAME 9265:9265
```

In a browser, open `127.0.0.1:9265`

#### Delete

```bash
$ make delete
```
