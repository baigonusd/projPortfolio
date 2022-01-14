import os
from pydoc import cli
from sqlite3 import connect
import sys
import json
from urllib import response
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app
from db.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

def test_create_item():
    data = {"title": "William Lawson",
            "description": "Whiskey"}
    response = client.post("/users/1/items/", json.dumps(data))
    assert response.status_code == 200
    assert response.json()["title"] == "William Lawson"
    assert response.json()["description"] == "Whiskey"

def test_read_items():
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json()[0]["title"] == "William Lawson"
    assert response.json()[0]["description"] == "Whiskey"