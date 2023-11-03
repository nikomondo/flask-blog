def test_hello(app):
    client = app.test_client()
    resp = client.get('/hello')
    assert resp.status_code == 200
    assert resp.data == b'Hello, World!'