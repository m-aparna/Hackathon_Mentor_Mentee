import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

os.environ.setdefault("DATABASE_URL", "sqlite:///./test_bootstrap.db")

from app.database import Base, get_db
from app.main import app
from app.models import goal, mentee, mentor, mentorship, resource
from app.models.goal import Goal, ProgressLog
from app.models.mentee import Mentee, UserRole as MenteeRole
from app.models.mentor import Mentor, UserRole as MentorRole
from app.models.mentorship import Mentorship
from app.models.resource import Resource

TEST_DATABASE_URL = "sqlite://"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
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
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client():
    original_startup = list(app.router.on_startup)
    app.router.on_startup.clear()
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    app.router.on_startup[:] = original_startup


@pytest.fixture(scope="function")
def seed_mentor(db_session):
    mentor_obj = Mentor(
        name="Seed Mentor",
        email="seed.mentor@example.com",
        role=MentorRole.mentor,
        department="Engineering",
        skills=["python", "ai"],
    )
    db_session.add(mentor_obj)
    db_session.commit()
    db_session.refresh(mentor_obj)
    return mentor_obj


@pytest.fixture(scope="function")
def seed_mentee(db_session):
    mentee_obj = Mentee(
        name="Seed Mentee",
        email="seed.mentee@example.com",
        role=MenteeRole.mentee,
        department="Engineering",
        skills=["python", "sql"],
    )
    db_session.add(mentee_obj)
    db_session.commit()
    db_session.refresh(mentee_obj)
    return mentee_obj


@pytest.fixture(scope="function")
def seed_mentorship(db_session, seed_mentor, seed_mentee):
    shared_skills = sorted(set(seed_mentor.skills or []).intersection(seed_mentee.skills or []))
    mentorship_obj = Mentorship(
        mentor_id=seed_mentor.id,
        mentee_id=seed_mentee.id,
        department=seed_mentor.department,
        skills=shared_skills,
    )
    db_session.add(mentorship_obj)
    db_session.commit()
    db_session.refresh(mentorship_obj)
    return mentorship_obj


@pytest.fixture(scope="function")
def seed_goal(db_session, seed_mentorship):
    goal_obj = Goal(
        mentorship_id=seed_mentorship.id,
        title="Ship API tests",
        description="Cover the goal endpoints",
    )
    db_session.add(goal_obj)
    db_session.commit()
    db_session.refresh(goal_obj)
    return goal_obj


@pytest.fixture(scope="function")
def seed_progress_log(db_session, seed_goal):
    progress_log = ProgressLog(goal_id=seed_goal.id, progress_percent=25, update_text="Started")
    db_session.add(progress_log)
    db_session.commit()
    db_session.refresh(progress_log)
    return progress_log


@pytest.fixture(scope="function")
def seed_resource(db_session):
    resource_obj = Resource(
        title="FastAPI Docs",
        link="https://fastapi.tiangolo.com/tutorial/",
        description="Primary reference",
    )
    db_session.add(resource_obj)
    db_session.commit()
    db_session.refresh(resource_obj)
    return resource_obj