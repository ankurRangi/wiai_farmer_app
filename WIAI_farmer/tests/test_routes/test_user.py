from WIAI_farmer.authentication import auth
from fastapi import status
import json
# _______________________________________________________________
# Testing the API BEFORE Login/Authentication

def test_login_WOuser_WOLOGIN(client):
    """
        Test to login into server when the user does not exist in the database

    """
    test_data = {"username": "000000000F", "password": "temp@123",}
    response = client.post("/authenticate", data=test_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == { "detail": "User does not exist, Need signup"}

def test_login_incorrect_pass(client, token_headers):
    """
    Testing to login the already user with incorrect password
    """
    data = {
        "username": "string",
        "password": "notstring",
    }
    response = client.post("/authenticate", data=data)
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect Password, Try 'temp@123' for first time user."}

# _______________________________________________________________
# Testing the API AFTER Login/Authentication

def test_authenticate(client, token_headers):
    """
    Testing to check auth token
    """
    data = {"username": "string", "password": "string",}
    response = client.post("/authenticate", data=data, headers=token_headers)
    assert response.status_code == status.HTTP_200_OK
    token = response.json()["access_token"]
    assert token_headers == {"Authorization": f"Bearer {token}"}

def test_signup_dublicate(client, token_headers):
    """
    Testing for dublicate user sign up
    """
    new_farmer = {
        "farmer_name": "string",
        "state_name": "string",
        "district_name": "string",
        "village_name": "string",
        "username": "string",
        "password": "string",
    }
    response = client.post("/signup", data=json.dumps(new_farmer),headers=token_headers)
    assert response.status_code == 400
    assert response.json() == {"detail": f"Farmer with {new_farmer['username']} already exists"}