# """
# Tests for /goals and /progress-logs CRUD endpoints.
# """
# from app.tests.conftest import make_mentee


# def make_goal(client, mentee_id, title="Learn FastAPI"):
#     resp = client.post("/goals/", json={
#         "mentee_id": mentee_id,
#         "title": title,
#         "description": "Complete FastAPI tutorial",
#         "status": "not_started",
#     })
#     assert resp.status_code == 201, resp.text
#     return resp.json()


# class TestGoalsCRUD:
#     def test_create_goal(self, client):
#         mentee = make_mentee(client)
#         resp = client.post("/goals/", json={
#             "mentee_id": mentee["id"],
#             "title": "Learn SQL",
#             "status": "not_started",
#         })
#         assert resp.status_code == 201
#         assert resp.json()["title"] == "Learn SQL"

#     def test_list_goals_all(self, client):
#         mentee = make_mentee(client)
#         make_goal(client, mentee["id"], "Goal A")
#         make_goal(client, mentee["id"], "Goal B")
#         resp = client.get("/goals/")
#         assert resp.status_code == 200
#         assert len(resp.json()) == 2

#     def test_list_goals_filter_by_mentee(self, client):
#         mentee = make_mentee(client)
#         make_goal(client, mentee["id"])
#         resp = client.get(f"/goals/?mentee_id={mentee['id']}")
#         assert resp.status_code == 200
#         assert all(g["mentee_id"] == mentee["id"] for g in resp.json())

#     def test_get_goal_by_id(self, client):
#         mentee = make_mentee(client)
#         goal = make_goal(client, mentee["id"])
#         resp = client.get(f"/goals/{goal['id']}")
#         assert resp.status_code == 200
#         assert resp.json()["id"] == goal["id"]

#     def test_get_goal_not_found(self, client):
#         assert client.get("/goals/9999").status_code == 404

#     def test_update_goal_status(self, client):
#         mentee = make_mentee(client)
#         goal = make_goal(client, mentee["id"])
#         resp = client.patch(f"/goals/{goal['id']}", json={"status": "in_progress"})
#         assert resp.status_code == 200
#         assert resp.json()["status"] == "in_progress"

#     def test_delete_goal(self, client):
#         mentee = make_mentee(client)
#         goal = make_goal(client, mentee["id"])
#         resp = client.delete(f"/goals/{goal['id']}")
#         assert resp.status_code == 204
#         assert client.get(f"/goals/{goal['id']}").status_code == 404


# class TestProgressLogsCRUD:
#     def test_create_progress_log(self, client):
#         mentee = make_mentee(client)
#         goal = make_goal(client, mentee["id"])
#         resp = client.post("/progress-logs/", json={
#             "goal_id": goal["id"],
#             "progress_percent": 50,
#             "update_text": "Halfway there!",
#         })
#         assert resp.status_code == 201
#         assert resp.json()["progress_percent"] == 50

#     def test_create_progress_log_invalid_percent(self, client):
#         mentee = make_mentee(client)
#         goal = make_goal(client, mentee["id"])
#         resp = client.post("/progress-logs/", json={
#             "goal_id": goal["id"],
#             "progress_percent": 150,
#         })
#         assert resp.status_code == 400

#     def test_list_progress_logs_for_goal(self, client):
#         mentee = make_mentee(client)
#         goal = make_goal(client, mentee["id"])
#         client.post("/progress-logs/", json={"goal_id": goal["id"], "progress_percent": 25})
#         client.post("/progress-logs/", json={"goal_id": goal["id"], "progress_percent": 75})
#         resp = client.get(f"/progress-logs/goal/{goal['id']}")
#         assert resp.status_code == 200
#         assert len(resp.json()) == 2

#     def test_delete_progress_log(self, client):
#         mentee = make_mentee(client)
#         goal = make_goal(client, mentee["id"])
#         log = client.post("/progress-logs/", json={"goal_id": goal["id"], "progress_percent": 10}).json()
#         resp = client.delete(f"/progress-logs/{log['id']}")
#         assert resp.status_code == 204
