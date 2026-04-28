from fastapi import status


def test_create_goal_success(client, seed_mentorship):
    response = client.post(
        "/goals/",
        json={
            "mentorship_id": seed_mentorship.id,
            "title": "Learn FastAPI",
            "description": "Finish the tutorial",
            "status": "not_started",
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    body = response.json()
    assert body["mentorship_id"] == seed_mentorship.id
    assert body["title"] == "Learn FastAPI"


def test_create_goal_rejects_unknown_mentorship(client):
    response = client.post(
        "/goals/",
        json={"mentorship_id": 9999, "title": "Ghost Goal"},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Mentorship not found"


def test_list_goals(client, seed_goal):
    response = client.get("/goals/")

    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert len(body) == 1
    assert body[0]["id"] == seed_goal.id


def test_list_goals_filters_by_mentorship_id(client, seed_goal):
    response = client.get(f"/goals/?mentorship_id={seed_goal.mentorship_id}")

    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert len(body) == 1
    assert body[0]["mentorship_id"] == seed_goal.mentorship_id


def test_get_goal_success(client, seed_goal):
    response = client.get(f"/goals/{seed_goal.id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == seed_goal.id


def test_get_goal_not_found(client):
    response = client.get("/goals/9999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Goal not found"


def test_update_goal_success(client, seed_goal):
    response = client.patch(
        f"/goals/{seed_goal.id}",
        json={"status": "in_progress", "description": "In flight"},
    )

    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert body["status"] == "in_progress"
    assert body["description"] == "In flight"


def test_update_goal_not_found(client):
    response = client.patch("/goals/9999", json={"status": "blocked"})

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Goal not found"


def test_delete_goal_success(client, seed_goal):
    response = client.delete(f"/goals/{seed_goal.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    follow_up = client.get(f"/goals/{seed_goal.id}")
    assert follow_up.status_code == status.HTTP_404_NOT_FOUND


def test_delete_goal_not_found(client):
    response = client.delete("/goals/9999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Goal not found"


def test_create_progress_log_success(client, seed_goal):
    response = client.post(
        "/progress-logs/",
        json={"goal_id": seed_goal.id, "progress_percent": 50, "update_text": "Halfway there"},
    )

    assert response.status_code == status.HTTP_201_CREATED
    body = response.json()
    assert body["goal_id"] == seed_goal.id
    assert body["progress_percent"] == 50


def test_create_progress_log_rejects_unknown_goal(client):
    response = client.post(
        "/progress-logs/",
        json={"goal_id": 9999, "progress_percent": 50},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Goal not found"


def test_create_progress_log_rejects_invalid_percent(client, seed_goal):
    response = client.post(
        "/progress-logs/",
        json={"goal_id": seed_goal.id, "progress_percent": 101},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "progress_percent must be between 0 and 100"


def test_delete_progress_log_success(client, seed_progress_log):
    response = client.delete(f"/progress-logs/{seed_progress_log.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_progress_log_not_found(client):
    response = client.delete("/progress-logs/9999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Progress log not found"