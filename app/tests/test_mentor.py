# """
# Tests for /mentors CRUD endpoints.
# One test per operation: Create, Read, Update, Delete.
# """
# import pytest
# from app.tests.conftest import make_mentor, make_mentee


# class TestMentorsCreate:
#     def test_create_mentor_success(self, client):
#         resp = client.post("/mentors/", json={
#             "name": "Carol",
#             "email": "carol@gmail.com",
#             "role": "mentor",
#             "department": "HR",
#             "skills": ["Python", "Sql"]
#         })
#         assert resp.status_code == 201
#         data = resp.json()
#         assert data["email"] == "carol@gmail.com"
#         assert data["role"] == "mentor"
#         assert "id" in data

#     def test_create_mentor_duplicate_email(self, client):
#         make_mentor(client)
#         resp = client.post("/mentors/", json={
#             "name": "Bob",
#             "email": "bob@gmail.com",
#             "role": "mentor",
#         })
#         assert resp.status_code == 400
#         assert "Email already registered" in resp.json()["detail"]

#     def test_create_mentor_invalid_role(self, client):
#         resp = client.post("/mentors/", json={
#             "name": "Dave",
#             "email": "dave@gmail.com",
#             "role": "supermentor",
#         })
#         assert resp.status_code == 422  # validation error


# class TestMentorsRead:

#     def test_get_mentor(self, client):
#         created = client.post("/mentors", json={
#             "name": "Carol",
#             "email": "carol@test.com",
#             "role": "mentor",
#             "skills": ["Python", "Sql"]
#         }).json()

#         r = client.get(f"/mentors/{created['id']}")
#         assert r.status_code == 200
#         assert r.json()["id"] == created["id"]

#     def test_list_mentors_empty(self, client):
#         resp = client.get("/mentors/")
#         assert resp.status_code == 200
#         assert resp.json() == []

#     def test_list_mentors_returns_all(self, client):
#         make_mentor(client)
#         make_mentee(client)
#         resp = client.get("/mentors/")
#         assert resp.status_code == 200
#         assert len(resp.json()) == 1

#     def test_get_mentor_by_id(self, client):
#         mentor = make_mentor(client)
#         resp = client.get(f"/mentors/{mentor['id']}")
#         assert resp.status_code == 200
#         assert resp.json()["id"] == mentor["id"]

#     def test_get_mentor_not_found(self, client):
#         resp = client.get("/mentors/9999")
#         assert resp.status_code == 404


# class TestMentorsUpdate:
#     def test_update_mentor_name(self, client):
#         mentor = make_mentor(client)
#         resp = client.patch(f"/mentors/{mentor['id']}", json={"name": "Updated Name"})
#         assert resp.status_code == 200
#         assert resp.json()["name"] == "Updated Name"

#     def test_update_mentor_not_found(self, client):
#         resp = client.patch("/mentors/9999", json={"name": "Ghost"})
#         assert resp.status_code == 404


# class TestMentorsDelete:
#     def test_delete_mentor(self, client):
#         mentor = make_mentor(client)
#         resp = client.delete(f"/mentors/{mentor['id']}")
#         assert resp.status_code == 204
#         # Confirm gone
#         assert client.get(f"/mentors/{mentor['id']}").status_code == 404

#     def test_delete_mentor_not_found(self, client):
#         resp = client.delete("/mentors/9999")
#         assert resp.status_code == 404