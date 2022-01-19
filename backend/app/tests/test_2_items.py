import json
from urllib import response

def test_create_item(client, token_header):
    data = {"title": "William Lawson",
            "description": "Whiskey"}
    response = client.post("/users/1/items/", json.dumps(data), headers=token_header)
    assert response.status_code == 200
    assert response.json()["title"] == "William Lawson"
    assert response.json()["description"] == "Whiskey"

def test_read_items(client):
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json()[0]["title"] == "William Lawson"
    assert response.json()[0]["description"] == "Whiskey"

def test_read_item(client):
    response = client.get("/item/{id}?item_id=1")
    assert response.status_code == 200
    assert response.json()["title"] == "William Lawson"
    assert response.json()["description"] == "Whiskey"
    assert response.json()["id"] == 1
    assert response.json()["owner_id"] == 1

def test_update_item(client, token_header):
    data = {"title": "Coca-Cola",
            "description": "Juicy"}
    response = client.put("/item/update/{id}?item_id=1&owner_id=1", json.dumps(data), headers=token_header)
    assert response.status_code == 200
    assert response.json()["title"] == "Coca-Cola"
    assert response.json()["description"] == "Juicy"

def test_delete_item(client, token_header):
    response = client.delete("/item/delete/{id}?item_id=1", headers=token_header)
    assert response.status_code == 200
    assert response.json()["message"] == "Item id 1 has been succesfully deleted"