import pytest

from src.app import create_app


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
