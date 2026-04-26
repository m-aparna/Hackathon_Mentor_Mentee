"""
conftest.py  –  shared test fixtures.

Uses SQLite in-memory so tests run without a real MySQL instance.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.models import resource, mentor, mentee, mentorship, goal

TEST_DATABASE_URL = "sqlite://"  # pure in-memory

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function", autouse=True)
def setup_db():
    """Create all tables before each test, drop after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client():
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


# ── Reusable helpers ───────────────────────────────────────────────────────────

def make_mentee(client, name="Alice", email="alice2@gmail.com"):
    resp = client.post("/users/", json={"name": name, "email": email, "role": "mentor", "department": "Engineering"})
    assert resp.status_code == 201, resp.text
    return resp.json()


def make_mentor(client, name="Bob", email="bob@gmail.com"):
    resp = client.post("/users/", json={"name": name, "email": email, "role": "mentor", "department": "Design"})
    assert resp.status_code == 201, resp.text
    return resp.json()


def make_skill(client, name="Python"):
    resp = client.post("/skills/", json={"name": name})
    assert resp.status_code == 201, resp.text
    return resp.json()


def make_mentorship(client, mentor_id, mentee_id):
    resp = client.post("/mentorships/", json={"mentor_id": mentor_id, "mentee_id": mentee_id})
    assert resp.status_code == 201, resp.text
    return resp.json()
