# """
# Tests for /mentorships CRUD endpoints.
# """
# from app.tests.conftest import make_mentor, make_mentee, make_mentorship


# class TestMentorshipsCRUD:
#     def test_create_mentorship(self, client):
#         mentor = make_mentor(client)
#         mentee = make_mentee(client)
#         resp = client.post("/mentorships/", json={
#             "mentor_id": mentor["id"],
#             "mentee_id": mentee["id"],
#         })
#         assert resp.status_code == 201
#         data = resp.json()
#         assert data["mentor_id"] == mentor["id"]
#         assert data["mentee_id"] == mentee["id"]
#         assert data["status"] == "active"

#     def test_create_mentorship_wrong_roles(self, client):
#         """mentor_id must have role=mentor, mentee_id must have role=mentee."""
#         mentor = make_mentor(client)
#         # Pass mentor as mentee – should fail
#         resp = client.post("/mentorships/", json={
#             "mentor_id": mentor["id"],
#             "mentee_id": mentor["id"],
#         })
#         assert resp.status_code == 400

#     def test_create_duplicate_active_mentorship(self, client):
#         mentor = make_mentor(client)
#         mentee = make_mentee(client)
#         make_mentorship(client, mentor["id"], mentee["id"])
#         resp = client.post("/mentorships/", json={
#             "mentor_id": mentor["id"],
#             "mentee_id": mentee["id"],
#         })
#         assert resp.status_code == 400

#     def test_list_mentorships(self, client):
#         mentor = make_mentor(client)
#         mentee = make_mentee(client)
#         make_mentorship(client, mentor["id"], mentee["id"])
#         resp = client.get("/mentorships/")
#         assert resp.status_code == 200
#         assert len(resp.json()) == 1

#     def test_get_mentorship_by_id(self, client):
#         mentor = make_mentor(client)
#         mentee = make_mentee(client)
#         m = make_mentorship(client, mentor["id"], mentee["id"])
#         resp = client.get(f"/mentorships/{m['id']}")
#         assert resp.status_code == 200
#         assert resp.json()["id"] == m["id"]

#     def test_get_mentorship_not_found(self, client):
#         assert client.get("/mentorships/9999").status_code == 404

#     def test_update_mentorship_status(self, client):
#         mentor = make_mentor(client)
#         mentee = make_mentee(client)
#         m = make_mentorship(client, mentor["id"], mentee["id"])
#         resp = client.patch(f"/mentorships/{m['id']}", json={"status": "completed"})
#         assert resp.status_code == 200
#         assert resp.json()["status"] == "completed"

#     def test_delete_mentorship(self, client):
#         mentor = make_mentor(client)
#         mentee = make_mentee(client)
#         m = make_mentorship(client, mentor["id"], mentee["id"])
#         resp = client.delete(f"/mentorships/{m['id']}")
#         assert resp.status_code == 204
#         assert client.get(f"/mentorships/{m['id']}").status_code == 404
