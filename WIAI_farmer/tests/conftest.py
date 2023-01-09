from typing import Any
from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import sys
import os

from WIAI_farmer.utility import database, createObj
from WIAI_farmer import main, schemas, models


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
#this is to include backend dir in sys.path so that we can import from db,main.py

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# Use connect_args parameter only with sqlite
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)

database.Base.metadata.create_all(bind=engine)

@pytest.fixture()
def client() -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """
    def _get_test_db():
        try:
            db_session = SessionTesting()
            yield db_session
        finally:
            pass

    main.app.dependency_overrides[database.get_db] = _get_test_db
    with TestClient(main.app) as client:
        yield client

@pytest.fixture
def token_headers(client: TestClient):
    new_farmer = schemas.FarmerSignUp(
        username="string",
        password="string",
        farmer_name="string",
        state_name="string",
        district_name="string",
        village_name="string",
    )
    db = SessionTesting()
    farmer = db.query(models.Farmer).filter(models.Farmer.username == new_farmer.username).first()
    if not farmer:
        createObj.create_farmer(db, new_farmer)
    data = {"username": new_farmer.username,"password": new_farmer.password,}
    response = client.post("/authenticate", data=data)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}