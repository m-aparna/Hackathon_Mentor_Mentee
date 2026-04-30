from fastapi import status
from app.models.mentee import Mentee, UserRole as MenteeRole


def test_create_mentorship_success(client, seed_mentor, seed_mentee):
    response = client.post(
        "/mentorships/",
        json={"mentor_id": seed_mentor.id, "mentee_id": seed_mentee.id},
    )

    assert response.status_code == status.HTTP_201_CREATED
    body = response.json()
    assert body["mentor_id"] == seed_mentor.id
    assert body["mentee_id"] == seed_mentee.id
    assert body["status"] == "active"


def test_create_mentorship_rejects_missing_mentor(client, seed_mentee):
    response = client.post(
        "/mentorships/",
        json={"mentor_id": 9999, "mentee_id": seed_mentee.id},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Mentor not found or user is not a mentor"


def test_create_mentorship_rejects_missing_mentee(client, seed_mentor):
    response = client.post(
        "/mentorships/",
        json={"mentor_id": seed_mentor.id, "mentee_id": 9999},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Mentee not found or user is not a mentee"


def test_create_mentorship_rejects_department_mismatch(client, db_session, seed_mentor):
    mentee = Mentee(
        name="Other Department Mentee",
        email="other.department@example.com",
        role=MenteeRole.mentee,
        department="Design",
        skills=["python"],
    )
    db_session.add(mentee)
    db_session.commit()
    db_session.refresh(mentee)

    response = client.post(
        "/mentorships/",
        json={"mentor_id": seed_mentor.id, "mentee_id": mentee.id},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Mentor and mentee must belong to the same department"


def test_create_mentorship_rejects_when_no_skill_overlaps(client, db_session, seed_mentor):
    mentee = Mentee(
        name="No Skill Match",
        email="no.skill.match@example.com",
        role=MenteeRole.mentee,
        department="Engineering",
        skills=["ppt", "communication"],
    )
    db_session.add(mentee)
    db_session.commit()
    db_session.refresh(mentee)

    response = client.post(
        "/mentorships/",
        json={"mentor_id": seed_mentor.id, "mentee_id": mentee.id},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Mentor and mentee must share at least one skill"


def test_create_mentorship_rejects_duplicate_active_pair(client, seed_mentorship):
    response = client.post(
        "/mentorships/",
        json={"mentor_id": seed_mentorship.mentor_id, "mentee_id": seed_mentorship.mentee_id},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Active mentorship already exists between these users"


def test_list_mentorships(client, seed_mentorship):
    response = client.get("/mentorships/")

    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert len(body) == 1
    assert body[0]["id"] == seed_mentorship.id


def test_get_mentorship_success(client, seed_mentorship):
    response = client.get(f"/mentorships/{seed_mentorship.id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == seed_mentorship.id


def test_get_mentorship_not_found(client):
    response = client.get("/mentorships/9999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Mentorship not found"


def test_update_mentorship_success(client, seed_mentorship):
    response = client.patch(
        f"/mentorships/{seed_mentorship.id}",
        json={"status": "completed"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "completed"


def test_update_mentorship_not_found(client):
    response = client.patch("/mentorships/9999", json={"status": "paused"})

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Mentorship not found"


def test_delete_mentorship_success(client, seed_mentorship):
    response = client.delete(f"/mentorships/{seed_mentorship.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    follow_up = client.get(f"/mentorships/{seed_mentorship.id}")
    assert follow_up.status_code == status.HTTP_404_NOT_FOUND


def test_delete_mentorship_not_found(client):
    response = client.delete("/mentorships/9999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Mentorship not found"