from fastapi.testclient import TestClient
from app.main import app  # adjust if your FastAPI app file has a different name

client = TestClient(app)


def test_create_resource():
    """CREATE"""
    response = client.post(
        "/resources",
        json={
            "title": "Docker Basics",
            "link": "https://example.com/docker",
            "description": "Beginner docker guide"
        }
    )

    assert response.status_code == 200 or response.status_code == 201
    data = response.json()
    assert data["title"] == "Docker Basics"
    assert "id" in data


def test_get_resource():
    """READ"""
    # First create a resource
    create_resp = client.post(
        "/resources",
        json={
            "title": "Kubernetes",
            "link": "https://example.com/k8s"
        }
    )
    resource_id = create_resp.json()["id"]

    response = client.get(f"/resources/{resource_id}")
    assert response.status_code == 200
    assert response.json()["id"] == resource_id


def test_update_resource():
    """UPDATE"""
    # Create first
    create_resp = client.post(
        "/resources",
        json={
            "title": "Old Title",
            "link": "https://example.com/old"
        }
    )
    resource_id = create_resp.json()["id"]

    # Update
    response = client.patch(
        f"/resources/{resource_id}",
        json={
            "title": "New Title"
        }
    )

    assert response.status_code == 200
    assert response.json()["title"] == "New Title"


def test_delete_resource():
    """DELETE"""
    # Create first
    create_resp = client.post(
        "/resources",
        json={
            "title": "Delete Me",
            "link": "https://example.com/delete"
        }
    )
    resource_id = create_resp.json()["id"]

    response = client.delete(f"/resources/{resource_id}")
    assert response.status_code == 204 or response.status_code == 200

    # Verify it is gone
    get_resp = client.get(f"/resources/{resource_id}")
    assert get_resp.status_code == 404