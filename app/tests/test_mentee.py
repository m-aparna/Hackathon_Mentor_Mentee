"""
Tests for /mentees CRUD endpoints.
One test per operation: Create, Read, Update, Delete.
"""
import pytest
from app.tests.conftest import make_mentor, make_mentee


class TestMenteeCreate:
    def test_create_mentee_success(self, client):
        resp = client.post("/mentees/", json={
            "name": "Carol",
            "email": "carol@gmail.com",
            "role": "mentee",
            "department": "HR",
        })
        assert resp.status_code == 201
        data = resp.json()
        assert data["email"] == "carol@gmail.com"
        assert data["role"] == "mentee"
        assert "id" in data

    def test_create_mentee_duplicate_email(self, client):
        make_mentee(client)
        resp = client.post("/mentees/", json={
            "name": "Alice2",
            "email": "alice@gmail.com",
            "role": "mentee",
        })
        assert resp.status_code == 400
        assert "Email already registered" in resp.json()["detail"]

    def test_create_mentee_invalid_role(self, client):
        resp = client.post("/mentees/", json={
            "name": "Dave",
            "email": "dave@yahoo.com",
            "role": "supermentee",
        })
        assert resp.status_code == 422  # validation error


class TestMenteesRead:
    def test_list_mentees_empty(self, client):
        resp = client.get("/mentees/")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_list_mentees_returns_all(self, client):
        make_mentor(client)
        make_mentee(client)
        resp = client.get("/mentees/")
        assert resp.status_code == 200
        assert len(resp.json()) == 2

    def test_get_mentee(client):
        created = client.post("/mentees", json={
            "name": "Mentee Two",
            "email": "mentee2@test.com",
            "role": "mentee",
            "skills": []
        }).json()

        r = client.get(f"/mentees/{created['id']}")
        assert r.status_code == 200
        assert r.json()["id"] == created["id"]


    def test_get_mentee_by_id(self, client):
        mentee = make_mentor(client)
        resp = client.get(f"/mentees/{mentee['id']}")
        assert resp.status_code == 200
        assert resp.json()["id"] == mentee["id"]

    def test_get_mentee_not_found(self, client):
        resp = client.get("/mentees/9999")
        assert resp.status_code == 404


class TestMenteesUpdate:
    def test_update_mentee_name(self, client):
        mentee = make_mentor(client)
        resp = client.patch(f"/mentees/{mentee['id']}", json={"name": "Updated Name"})
        assert resp.status_code == 200
        assert resp.json()["name"] == "Updated Name"

    def test_update_mentee_not_found(self, client):
        resp = client.patch("/mentees/9999", json={"name": "Ghost"})
        assert resp.status_code == 404


class TestMenteesDelete:
    def test_delete_mentee(self, client):
        mentee = make_mentor(client)
        resp = client.delete(f"/mentees/{mentee['id']}")
        assert resp.status_code == 204
        # Confirm gone
        assert client.get(f"/mentees/{mentee['id']}").status_code == 404

    def test_delete_mentee_not_found(self, client):
        resp = client.delete("/mentees/9999")
        assert resp.status_code == 404
