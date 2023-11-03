import pytest 
from flaskr import create_app

@pytest.fixture
def app():
    app = create_app()
    app.config.from_mapping('flaskr.config.TestingConfig')
    return app