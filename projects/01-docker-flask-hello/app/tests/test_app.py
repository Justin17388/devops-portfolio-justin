from app import app


def test_root():
    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json["message"].startswith("Hello")
