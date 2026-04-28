from fastapi import status


def test_attach_resource_to_goal_success(client, seed_goal, seed_resource):
    response = client.post(f"/goals/{seed_goal.id}/resources/{seed_resource.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT

    list_response = client.get(f"/goals/{seed_goal.id}/resources")
    assert list_response.status_code == status.HTTP_200_OK
    assert [resource["id"] for resource in list_response.json()] == [seed_resource.id]


def test_attach_resource_to_goal_rejects_unknown_goal(client, seed_resource):
    response = client.post(f"/goals/9999/resources/{seed_resource.id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Goal not found"


def test_attach_resource_to_goal_rejects_unknown_resource(client, seed_goal):
    response = client.post(f"/goals/{seed_goal.id}/resources/9999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Resource not found"


def test_attach_resource_to_goal_is_idempotent(client, seed_goal, seed_resource):
    first = client.post(f"/goals/{seed_goal.id}/resources/{seed_resource.id}")
    second = client.post(f"/goals/{seed_goal.id}/resources/{seed_resource.id}")

    assert first.status_code == status.HTTP_204_NO_CONTENT
    assert second.status_code == status.HTTP_204_NO_CONTENT

    list_response = client.get(f"/goals/{seed_goal.id}/resources")
    assert [resource["id"] for resource in list_response.json()] == [seed_resource.id]


def test_list_resources_for_goal_success(client, seed_goal, seed_resource):
    client.post(f"/goals/{seed_goal.id}/resources/{seed_resource.id}")

    response = client.get(f"/goals/{seed_goal.id}/resources")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]["id"] == seed_resource.id


def test_list_resources_for_goal_not_found(client):
    response = client.get("/goals/9999/resources")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Goal not found"


def test_remove_resource_from_goal_success(client, seed_goal, seed_resource):
    client.post(f"/goals/{seed_goal.id}/resources/{seed_resource.id}")

    response = client.delete(f"/goals/{seed_goal.id}/resources/{seed_resource.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    list_response = client.get(f"/goals/{seed_goal.id}/resources")
    assert list_response.json() == []


def test_remove_resource_from_goal_rejects_unknown_goal(client, seed_resource):
    response = client.delete(f"/goals/9999/resources/{seed_resource.id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Goal not found"


def test_remove_resource_from_goal_rejects_unknown_resource(client, seed_goal):
    response = client.delete(f"/goals/{seed_goal.id}/resources/9999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Resource not found"