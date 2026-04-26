from fastapi import status


def test_create_mentor_success(client):
    response = client.post(
        "/mentors/",
        json={
            "name": "New Mentor",
            "email": "new.mentor@example.com",
            "role": "mentor",
            "department": "Platform",
            "skills": ["DevOps", "python", "GKE"],
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    body = response.json()
    assert body["name"] == "New Mentor"
    assert body["role"] == "mentor"
    assert body["skills"] == ["DevOps", "python", "GKE"]


def test_create_mentor_duplicate_email(client, seed_mentor):
    response = client.post(
        "/mentors/",
        json={
            "name": "Duplicate Mentor",
            "email": seed_mentor.email,
            "role": "mentor",
            "department": "Platform",
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Email already registered"


def test_list_mentors(client, seed_mentor):
    response = client.get("/mentors/")

    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert len(body) == 1
    assert body[0]["email"] == seed_mentor.email


def test_get_mentor_success(client, seed_mentor):
    response = client.get(f"/mentors/{seed_mentor.id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == seed_mentor.id


def test_get_mentor_not_found(client):
    response = client.get("/mentors/9999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "mentor not found"


def test_update_mentor_success(client, seed_mentor):
    response = client.patch(
        f"/mentors/{seed_mentor.id}",
        json={"name": "Updated Mentor", "department": "Data", "skills": ["DevOps", "python", "GKE"],},
    )

    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert body["name"] == "Updated Mentor"
    assert body["department"] == "Data"
    assert body["skills"]== ["DevOps", "python", "GKE"]


def test_update_mentor_not_found(client):
    response = client.patch("/mentors/9999", json={"name": "Ghost"})

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "mentor not found"


def test_delete_mentor_success(client, seed_mentor):
    response = client.delete(f"/mentors/{seed_mentor.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    follow_up = client.get(f"/mentors/{seed_mentor.id}")
    assert follow_up.status_code == status.HTTP_404_NOT_FOUND


def test_delete_mentor_not_found(client):
    response = client.delete("/mentors/9999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "mentor not found"
