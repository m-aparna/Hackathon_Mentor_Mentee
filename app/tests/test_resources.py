from fastapi import status


def test_create_resource_success(client):
    response = client.post(
        "/resources/",
        json={
            "title": "Docker Basics",
            "link": "https://example.com/docker",
            "description": "Beginner docker guide",
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    body = response.json()
    assert body["title"] == "Docker Basics"
    assert body["link"] == "https://example.com/docker"


def test_list_resources(client, seed_resource):
    response = client.get("/resources/")

    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert len(body) == 1
    assert body[0]["id"] == seed_resource.id


def test_get_resource_success(client, seed_resource):
    response = client.get(f"/resources/{seed_resource.id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == seed_resource.id


def test_get_resource_not_found(client):
    response = client.get("/resources/9999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Resource not found"


def test_update_resource_success(client, seed_resource):
    response = client.patch(
        f"/resources/{seed_resource.id}",
        json={"title": "Updated Title"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "Updated Title"


def test_update_resource_not_found(client):
    response = client.patch("/resources/9999", json={"title": "Ghost"})

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Resource not found"


def test_delete_resource_success(client, seed_resource):
    response = client.delete(f"/resources/{seed_resource.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    follow_up = client.get(f"/resources/{seed_resource.id}")
    assert follow_up.status_code == status.HTTP_404_NOT_FOUND


def test_delete_resource_not_found(client):
    response = client.delete("/resources/9999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Resource not found"
