import pytest
from flask import Flask
from flask.testing import FlaskClient

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_hello_world(client: FlaskClient):
    response = client.get('/')
    assert response.status_code == 200
    assert response.data == b'Hello World!'

if __name__ == '__main__':
    # Run tests and generate report
    pytest.main(['-v', '--junitxml=report.xml'])
    # Run Flask application
    app.run()
