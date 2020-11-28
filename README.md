# Avast homework

This is a simple flask app with 3 endpoints:
* /ping -> returns "Alive" and current time
* /v1/now -> returns json, e.g. {'now": <time>}
* /v1/VIP/<integer> -> returns either
  * after more than 5 sec: TIMEOUT
  * if there is a db error: ERROR
  * in normal operation a json, e.g. {"gpsCoords":{"lat":77.77449,"long":106.75767},"source":"vip-db"}

## Installation
```bash
$ python3 -m venv <your_virtual_environment>
$ source <your_virual_environment>/bin/activate
$ git clone git@github.com:tibor-reiss/avagps.git .
$ python3 -m pip install -e .
```

## Start the app
Logging location: avagps.log

Development
```bash
flask run
```
Production
```bash
gunicorn -b localhost:<port> -w <workers> src.wsgi:app
```

## Usage
From browser:
* http://localhost:5000/ping
* http://localhost:5000/v1/now
* http://localhost:5000/v1/VIP/<integer>

From command line:
```bash
    curl -X GET http://localhost:5000/ping
    curl -X GET http://localhost:5000/v1/now
    curl -X GET http://localhost:5000/v1/VIP/<integer>
```

## Testing
pytest
