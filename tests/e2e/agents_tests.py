import pytest
from fastapi.testclient import TestClient
from src.api.api import app
from dotenv import load_dotenv
load_dotenv() 

client = TestClient(app)

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjc1ZDI1NTktZmE0Ny00MDJkLThjMTYtZTViNmUyYjg4YWNmIiwiZXhwIjoxNzgzNTQzODc2fQ.3RG3A1wap_KZ6esSQelQLBSF0id6Bg91t2bx1vc13TA"

# def test_create_agent_success():
#     with TestClient(app) as client:
#         payload = {
#             "agentName": "deleteAgent",
#             "agentDescription": "tesitng create agents"
#         }

#         res = client.post("/agents/secure/create",
#             headers={"Authorization": f"Bearer {token}"},
#             json=payload
#         )
#         assert res.status_code == 201
#         assert res.json()["detail"] == "Agent created"


def test_create_agent_missing_fields():
    with TestClient(app) as client:
        payload = {
            "agentDescription": "testing agents missing fields"
        }

        res = client.post("/agents/secure/create",
            headers={"Authorization": f"Bearer {token}"},
            json=payload
        )
        assert res.status_code == 422


def test_secure_resource():
    with TestClient(app) as client:
        res = client.get(
            "/agents/secure/resource/350d96d8-700a-42fc-9c0a-699bbf504256",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert res.status_code == 200
      
def test_secure_resource_not_found():
    with TestClient(app) as client:
        res = client.get(
            "/agents/secure/resource/350d96d8-700a-42fc-9c0a-699bbf504257",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert res.status_code == 404
        assert res.json()["detail"] == "Agent not found"
      

def test_secure_collection():
    with TestClient(app) as client:
        res = client.get(
            "/agents/secure/collection",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert res.status_code == 200
      
def test_update_agent():
    with TestClient(app) as client:
        payload = {
            "agentName": "Updated agent name",
            "agentDescription": "Updated agent description"
        }

        res = client.put(
            "/agents/secure/350d96d8-700a-42fc-9c0a-699bbf504256",
            json=payload,
            headers={"Authorization": f"Bearer {token}"}
        )
        assert res.status_code == 200
        assert res.json()["detail"] == "Agent updated"



# def test_delete_agent():
#     with TestClient(app) as client:
#         res = client.delete(
#             "/agents/secure/9d51b2b4-5061-4866-a820-d020c08ab821",
#             headers={"Authorization": f"Bearer {token}"}
#         )
#         assert res.status_code == 200
#         assert res.json()["detail"] == "Agent deleted"
