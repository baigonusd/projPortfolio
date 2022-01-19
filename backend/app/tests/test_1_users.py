import json
from urllib import response
from config import settings

#json.dumps - trabslator to json (filetype: str) 
def test_create_user(client):
    data = {"email": settings.TEST_USER,
            "password": settings.TEST_PASSWORD}
    response = client.post("/users/", json.dumps(data))
    assert response.status_code == 200
    assert response.json()["email"] == settings.TEST_USER
    assert response.json()["is_active"] == True
    client.post("/users/", json.dumps({"email": "testuser2@test.com",
                                        "password": "passwordtest2"}))

def test_users(client):
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json()[0]["email"] == settings.TEST_USER
    assert response.json()[1]["email"] == "testuser2@test.com"
    assert response.json()[0]["is_active"] == True

def test_user(client):
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["email"] == settings.TEST_USER
    assert response.json()["is_active"] == True

def test_user_update(client):
    data = {"email": "changed@email.com",
            "password": "changedpassword"}
    response = client.put("/user/update/%7Bid%7D?user_id=2", json.dumps(data))
    assert response.status_code == 200
    assert response.json()["email"] == "changed@email.com"
    assert response.json()["password"] == "changedpassword"


def test_user_delete(client):
    response = client.delete("/user/delete/%7Bid%7D?user_id=2")
    assert response.status_code == 200
    assert response.json()["message"] == "User id 2 has been succesfully deleted"
    

# WRONG REQUESTS

def test_wrong_create_user(client):
    data = {"email": "testuser1@test.com",
            "password": "passwordtest1"}
    response = client.post("/users/", json.dumps(data))
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

