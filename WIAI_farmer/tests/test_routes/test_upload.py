from fastapi.testclient import TestClient
from WIAI_farmer.routers import upload
from WIAI_farmer import main
from fastapi import status


# Testing the APIs WITHOUT Login/Authentication

def test_csv_upload_WOLOGIN(client):
    """
        Testing to upload a csv file without Login
    """
    file = {"file": open("./test_upload.csv", "rb")}
    response = client.post("/upload", files=file)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}


# Testing the APIs WITH Login/Authentication

def test_csv_upload_LOGIN(client, token_headers):
    """
        Testing to upload a csv file after logged-in

    """
    file = {"file": open("./test_upload.csv", "rb")}
    response = client.post("/upload", files=file, headers=token_headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok", "detail": "file data uploaded successfully"}