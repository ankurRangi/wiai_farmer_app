from WIAI_farmer.authentication import auth
from fastapi import status
import json
# _______________________________________________________________
# Testing the API BEFORE Login/Authentication

def test_fetch_all_farmer_WOLOGIN(client):
    """
        Test to fetch all the farmers list without login
    """
    response = client.get("/farmers")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}

def test_login_wouser_WOLOGIN(client):
    """
        Test to login into server when the user does not exist in the database

    """
    test_data = {"username": "000000000F", "password": "temp@123",}
    response = client.post("/login", data=test_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == { "detail": "User does not exist, Need signup"}


def test_update_details_WOLOGIN(client):
    """
        Testing to update the details for the user without LOGIN/AUTHENTICATION
    """
    new_data = {
        "password": "updated_string",
        "farmer_name": "string",
        "state_name": "string",
        "district_name": "string",
        "village_name": "string",
    }
    response = client.patch("/update/test", data=json.dumps(new_data))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}

# _______________________________________________________________
# Testing the API AFTER Login/Authentication

def test_fetch_all_farmers_LOGIN(client, token_headers):
    """
        Test to fetch all the farmers list after user logged-in
    """
    response = client.get("/farmers", headers=token_headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]["username"] == "string"
    assert response.json()[0]["farmer_name"] == "string"
    assert response.json()[0]["state_name"] == "string"
    assert response.json()[0]["district_name"] == "string"
    assert response.json()[0]["village_name"] == "string"
    assert response.json()[0]["phone_number"] == "string"

def test_update_details_Otheruser_LOGIN(client, token_headers):
    """
        Testing to update the details for different user {updated_string} after LOGIN/AUTHENTICATION

    """
    updated_farmer = {
        "farmer_name": "updated_string",
        "state_name": "updated_string",
        "district_name": "updated_string",
        "village_name": "updated_string",
        "password": "updated_string",
    }
    response = client.patch("/update/updated_string", data=json.dumps(updated_farmer), headers=token_headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Not authorised to change details for a diferent user, check your details and try again"}


def test_login(client, token_headers):
    data = {"username": "string", "password": "string",}
    response = client.post("/login", data=data)
    assert response.status_code == status.HTTP_200_OK
    token = response.json()["access_token"]
    assert token_headers == {"Authorization": f"Bearer {token}"}

