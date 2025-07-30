import pytest
from fastapi.testclient import TestClient
from dotenv import load_dotenv
from src.api.api import app 
load_dotenv() 




client = TestClient(app)

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjc1ZDI1NTktZmE0Ny00MDJkLThjMTYtZTViNmUyYjg4YWNmIiwiZXhwIjoxNzgzNTQzODc2fQ.3RG3A1wap_KZ6esSQelQLBSF0id6Bg91t2bx1vc13TA"


def get_auth_headers():
    return {"Authorization": f"Bearer {token}"}


# def test_create_chat():
#     with TestClient(app) as client:
#         response = client.post(
#             "/chats/secure/create",
#             headers=get_auth_headers()
#         )

#         assert response.status_code == 201
  
#         assert "chatId" in response.json()


def test_collection():
    with TestClient(app) as client:
        response = client.get("/chats/secure/collection", headers=get_auth_headers())
        
        assert response.status_code == 200

def test_update():
    with TestClient(app) as client:
        res = client.put("/chats/secure/update/d338e452-4059-47a8-a62a-883b5481f23b",
            headers=get_auth_headers(),
            json={
                "title": "Upadated chat title"
            }
        )

        assert res.status_code == 200
        assert res.json()["detail"] == "Chat updated"