from fastapi.testclient import TestClient

import main

client = TestClient(main.app)


def test_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"greating": "Hello FastAPI"}
