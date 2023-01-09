from fastapi import status
from fastapi.testclient import TestClient
from WIAI_farmer.routers import translate
from WIAI_farmer import main


# Testing the API without Login/Authentication for translate.py

def test_fetch_all_farmers_hindi_WOLOGIN(client):
    """
        Testing to fetch all the details of users in HINDI from the db WITHOUT login/authentication 
    """
    response = client.get("/farmers/hi")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}

# Testing the API without Login/Authentication for translate.py

def test_fetch_farmers_in_punjabi_LOGIN(client, token_headers):
    """
        Testing to fetch all the details of users in HINDI from the db after the login/authentication
    """
    response = client.get("/farmers/hi", headers=token_headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]["username"] == "string"    
    # Username is not converting (type =string) since we are considering it as a phone number
    assert response.json()[0]["farmer_name"] == "डोरी"
    assert response.json()[0]["state_name"] == "डोरी"
    assert response.json()[0]["district_name"] == "डोरी"
    assert response.json()[0]["village_name"] == "डोरी"
    assert response.json()[0]["phone_number"] == "string"

