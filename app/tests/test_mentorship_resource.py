from fastapi import status


def test_recommend_resource_to_mentorship_success(client, seed_mentorship, seed_resource):
    response = client.post(f"/mentorship/{seed_mentorship.id}/resources/{seed_resource.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT

    list_response = client.get(f"/mentorship/{seed_mentorship.id}/resources")
    assert list_response.status_code == status.HTTP_200_OK
    assert [resource["id"] for resource in list_response.json()] == [seed_resource.id]


def test_recommend_resource_to_mentorship_rejects_unknown_mentorship(client, seed_resource):
    response = client.post(f"/mentorship/9999/resources/{seed_resource.id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Mentorship not found"


def test_recommend_resource_to_mentorship_rejects_unknown_resource(client, seed_mentorship):
    response = client.post(f"/mentorship/{seed_mentorship.id}/resources/9999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Resource not found"


def test_recommend_resource_to_mentorship_is_idempotent(client, seed_mentorship, seed_resource):
    first = client.post(f"/mentorship/{seed_mentorship.id}/resources/{seed_resource.id}")
    second = client.post(f"/mentorship/{seed_mentorship.id}/resources/{seed_resource.id}")

    assert first.status_code == status.HTTP_204_NO_CONTENT
    assert second.status_code == status.HTTP_204_NO_CONTENT

    list_response = client.get(f"/mentorship/{seed_mentorship.id}/resources")
    assert [resource["id"] for resource in list_response.json()] == [seed_resource.id]


def test_list_resources_for_mentorship_success(client, seed_mentorship, seed_resource):
    client.post(f"/mentorship/{seed_mentorship.id}/resources/{seed_resource.id}")

    response = client.get(f"/mentorship/{seed_mentorship.id}/resources")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]["id"] == seed_resource.id


def test_list_resources_for_mentorship_not_found(client):
    response = client.get("/mentorship/9999/resources")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Mentorship not found"


def test_remove_resource_from_mentorship_success(client, seed_mentorship, seed_resource):
    client.post(f"/mentorship/{seed_mentorship.id}/resources/{seed_resource.id}")

    response = client.delete(f"/mentorship/{seed_mentorship.id}/resources/{seed_resource.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    list_response = client.get(f"/mentorship/{seed_mentorship.id}/resources")
    assert list_response.json() == []


def test_remove_resource_from_mentorship_rejects_unknown_mentorship(client, seed_resource):
    response = client.delete(f"/mentorship/9999/resources/{seed_resource.id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Mentorship not found"


def test_remove_resource_from_mentorship_rejects_unknown_resource(client, seed_mentorship):
    response = client.delete(f"/mentorship/{seed_mentorship.id}/resources/9999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Resource not found"
