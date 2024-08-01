from fastapi.testclient import TestClient
from qna_api.main import app

client = TestClient(app)

def test_redirect_to_swagger():
    """Tests redirect to Swagger endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.url.path.endswith("/docs")

def test_init_db_not_called():
    from qna_api.core.database import init_db
    assert init_db() is None