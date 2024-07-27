from fastapi.testclient import TestClient
from qna_api.main import app

client = TestClient(app)

def test_redirect_to_swagger():
    """Tests redirect to Swagger endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.url.path.endswith("/docs")
