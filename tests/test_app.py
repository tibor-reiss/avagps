import json
import pytest
import time

from src.app import create_app, TIMEOUT


@pytest.fixture
def mock_heartbeat(mocker):
    mocker.patch('src.config.HEARTBEAT')


@pytest.fixture()
def app(mock_heartbeat):
    _app = create_app()
    yield _app


@pytest.fixture()
def client(app):
    yield app.test_client()


def test_ping(client):
    response = client.get('/ping')
    assert response.status_code == 200
    assert b'Alive' in response.data


def test_now(client):
    response = client.get('/v1/now')
    assert response.status_code == 200


def test_vip_correct_json(client, mocker):
    mocker.patch(
        'src.app.get_vip_coord',
        return_value=type(
            'testclass',
            (object, ),
            {
                'status_code': 200,
                'text': '{"latitude": 1, "longitude": 2}'
            }
        )()
    )
    response = client.get('/v1/VIP/1')
    assert response.status_code == 200
    assert json.loads(response.data) == json.loads('{"gpsCoords":{"lat":1,"long":2},"source":"vip-db"}')


def test_vip_missing_field(client, mocker):
    mocker.patch(
        'src.app.get_vip_coord',
        return_value=type(
            'testclass',
            (object, ),
            {
                'status_code': 200,
                'text': '{latit: 1, "longitude": 2}'
            }
        )()
    )
    response = client.get('/v1/VIP/1')
    assert response.status_code == 501


def test_vip_malformed_json(client, mocker):
    mocker.patch(
        'src.app.get_vip_coord',
        return_value=type(
            'testclass',
            (object, ),
            {
                'status_code': 200,
                'text': '{latitude: 1, "longitude": 2}'
            }
        )()
    )
    response = client.get('/v1/VIP/1')
    assert response.status_code == 501


def test_vip_db_error(client, mocker):
    mocker.patch(
        'src.app.get_vip_coord',
        return_value=type(
            'testclass',
            (object, ),
            {
                'status_code': 599,
                'text': '{latitude: 1, "longitude": 2}'
            }
        )()
    )
    response = client.get('/v1/VIP/1')
    assert response.status_code == 500


def test_vip_timeout(client, mocker):
    def time_sleep(_):
        import time
        time.sleep(TIMEOUT + 1)
    mocker.patch('src.app.requests.get', time_sleep)
    response = client.get('/v1/VIP/1')
    assert response.status_code == 503
