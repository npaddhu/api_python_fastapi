# Pytest uses this conftest.py module, which will can have all the fixtures. 
# We no need to import all the fixtures in any of the module in the tests directory as Pytest will import automatically the fixtures within the conftest.py module.

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from jose import jwt
#from sqlalchemy.ext.declarative import declarative_base
import pytest
from app.main import app
from app import schemas
from app.config import settings
from app.database import get_db
from app.database import Base
#from app.config import settings
from app.oauth2 import create_access_token
from app import models


SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:postgres@localhost/fastapi_test'   # this is for test purpose
#SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    print("my session fixture ran")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user2(client):
    user_data = {"email": "nooka1@gmail.com", "password": "testclient", "phone_numer": 90045646654}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


#####fixtures for users
@pytest.fixture
def test_user(client):
    user_data = {"email": "nooka2@gmail.com", "password": "testclient", "phone_numer": 903224352133}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


#####fixtures for posts
@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client


@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [{
        "title": "mother",
        "content": "mothers love",
        "owner_id": test_user['id']
    }, {
        "title": "father",
        "content": "fathers love",
        "owner_id": test_user['id']

    }, {
        "title": "parents",
        "content": "parents love",
        "owner_id": test_user2['id']

    }]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)
    '''
    session.add_all([
        models.Post(title="first title", content="first content", owner_id=test_user["id"]),
        models.Post(title="2nd title", content="2nd content", owner_id=test_user["id"]),
        models.Post(title="3rd title", content="3rd content", owner_id=test_user["id"])
    ])
    '''

    session.commit()

    posts = session.query(models.Post).all()
    return posts