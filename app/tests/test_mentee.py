from fastapi import status


def test_create_mentee_success(client):
    response = client.post(
        "/mentees/",
        json={
            "name": "New Mentee",
            "email": "new.mentee@example.com",
            "role": "mentee",
            "department": "Engineering",
            "skills": ["python", "AI"],
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    body = response.json()
    assert body["name"] == "New Mentee"
    assert body["email"] == "new.mentee@example.com"
    assert body["role"] == "mentee"
    assert body["department"] == "Engineering"
    assert body["skills"] == ["python", "AI"]


def test_create_mentee_duplicate_email(client, seed_mentee):
    response = client.post(
        "/mentees/",
        json={
            "name": "Duplicate",
            "email": seed_mentee.email,
            "role": "mentee",
            "department": "Engineering",
            "skills": ["python", "AI"],
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Email already registered"


def test_list_mentees(client, seed_mentee):
    response = client.get("/mentees/")

    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert len(body) == 1
    assert body[0]["email"] == seed_mentee.email


def test_get_mentee_success(client, seed_mentee):
    response = client.get(f"/mentees/{seed_mentee.id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == seed_mentee.id


def test_get_mentee_not_found(client):
    response = client.get("/mentees/9999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "mentee not found"


def test_update_mentee_success(client, seed_mentee):
    response = client.patch(
        f"/mentees/{seed_mentee.id}",
        json={"name": "Updated Mentee", "department": "Product", "Skils": ["python", "AI"]},
    )

    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert body["name"] == "Updated Mentee"
    assert body["department"] == "Product"
    assert body["email"] == seed_mentee.email
    assert body["skills"] == ["python", "AI"]


def test_update_mentee_not_found(client):
    response = client.patch("/mentees/9999", json={"name": "Ghost"})

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "mentee not found"


def test_delete_mentee_success(client, seed_mentee):
    response = client.delete(f"/mentees/{seed_mentee.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    follow_up = client.get(f"/mentees/{seed_mentee.id}")
    assert follow_up.status_code == status.HTTP_404_NOT_FOUND


def test_delete_mentee_not_found(client):
    response = client.delete("/mentees/9999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "mentee not found"
