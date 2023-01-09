from fastapi.testclient import TestClient
from WIAI_farmer.main import app
from WIAI_farmer.authentication import auth


def test_health_check(client):
    """
        Testing if the server is working or not
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "Ok", "detail": "Working Successfully"}

def test_password_hashing():
    """
        Testing if the password hashing is working properly or not
    """
    hashed_password = auth.get_password_hash("password")
    assert auth.verify_password("password", hashed_password) == True
    assert auth.verify_password("password_1", hashed_password) == False