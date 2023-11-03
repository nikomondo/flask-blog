import os

def test_testing_config(app):
    app.config.from_object('project.config.TestingConfig')
    assert app.config['DEBUG']
    assert app.config['TESTING']
    assert not app.config['PRESERVE_CONTEXT_ON_EXCEPTION']
    assert app.config['SQLALCHEMY_DATABASE_URI'] == os.environ.get(
        'DATABASE_TEST_URL')