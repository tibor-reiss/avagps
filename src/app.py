import datetime
import json
import logging
import os
import requests
import threading
import time
import timeout_decorator
from flask import Flask, jsonify, Response


TIMEOUT = 4


class MissingJsonFields(Exception):
    pass


def heartbeat():
    return f'Alive @{datetime.datetime.now()}'


def heartbeat_task(app):
    while True:
        msg = heartbeat()
        app.logger.info(msg)
        time.sleep(3)


@timeout_decorator.timeout(TIMEOUT, use_signals=False)
def get_time_now():
    time_now = datetime.datetime.now().strftime('%Y%M%dT%H%M%S')
    return time_now


@timeout_decorator.timeout(TIMEOUT, use_signals=False)
def get_vip_coord(coord):
    url = 'http://localhost:8088/v1/coords/' + str(coord)
    resp = requests.get(url)
    return resp


def set_app_logger(app):
    pid = os.getpid()
    handler = logging.FileHandler('avagps.log')
    formatter = logging.Formatter(f'%(levelname)s {pid} - %(message)s')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    set_app_logger(app)

    @app.route('/ping')
    def ping():
        return heartbeat()

    @app.route('/v1/now')
    def time_now():
        try:
            dt_now = get_time_now()
            return jsonify({'now': dt_now})
        except timeout_decorator.timeout_decorator.TimeoutError:
            app.logger.error('Error when querying now!')
            return 'TIMEOUT'

    @app.route('/v1/VIP/<coord>')
    def vip_coord(coord):
        try:
            resp = get_vip_coord(coord)
            if resp.status_code == 200:
                try:
                    json_received = json.loads(resp.text)
                    if 'latitude' not in json_received or 'longitude' not in json_received:
                        raise MissingJsonFields()
                    json_vip = {
                        'source': 'vip-db',
                        'gpsCoords': {
                            'lat': json_received['latitude'],
                            'long': json_received['longitude']
                        }
                    }
                    return json_vip, 200
                except (TypeError, json.decoder.JSONDecodeError):
                    app.logger.error(f'Error when processing json: malformed. Returned from db: {resp.text}')
                    return 'ERROR', 501
                except MissingJsonFields:
                    app.logger.error(f'Error when processing json: missing fileds. Returned from db: {rep.text}')
                    return 'ERROR', 501
            else:
                app.logger.error(f'Error in db when querying {coord}!')
                return 'ERROR', 500
        except timeout_decorator.timeout_decorator.TimeoutError:
            app.logger.error(f'Timeout when querying {coord}!')
            return 'TIMEOUT', 503
        

    if app.config.get('HEARTBEAT'):
        t2 = threading.Thread(target=heartbeat_task, args=(app,))
        t2.start()

    return app


if __name__ == '__main__':
    app = create_app()
    app.logger.info('Starting flask app...')
    app.run()
