"""
from app import schemas
from app.config import settings
from jose import jwt
import pytest

def test_root(client):
    response = client.get("/")
    #print(response)
    #print(response.status_code)
    assert response.status_code == 200
    #print(response.json().get('message') == 'Welcome to FastAPI..!')
    assert response.json() == {"message": "Welcome to FastAPI..!"}


#test create user
def test_create_user(client):
    user_data = {"email": "testclient@gmail.com", "password": "testclient", "phone_numer": 9032132133}
    res = client.post("/users/", json=user_data)
    #print(res.status_code)
    #print(res.json())
    new_user = schemas.UserCreateRes(**res.json())
    assert new_user.email == 'testclient@gmail.com'
    assert res.status_code == 201


# test login user
# the data needs to be in db while testing the login user, so using test_user fixture
def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user["email"], "password": test_user["password"]})   #login data is form-data, so use data instead of json
    #print(res.status_code)
    #print(res)
    login_res = schemas.Token(**res.json())
    #print(login_res)
    #validate token
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


# For incorrect logging
@pytest.mark.parametrize("email, password, status_code", [
    ("testclient@gmail.com", "wrongpassword", 403),
    ("wrongtestclient@gmail.com", "testclient", 403),
    ("wrongtestclient@gmail.com", "wrongpassword", 403),
    (None, "testclient", 422),
    ("testclient@gmail.com", None, 422)
])
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})   
    assert res.status_code == status_code
    #assert res.json().get('detail') == "Invalid credentials"
"""

import pytest
from jose import jwt
from app import schemas

from app.config import settings


# def test_root(client):

#     res = client.get("/")
#     print(res.json().get('message'))
#     assert res.json().get('message') == 'Hello World'
#     assert res.status_code == 200


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "nooka@gmail.com", "password": "password123", "phone_numer": 9797947945})

    new_user = schemas.UserCreateRes(**res.json())
    assert new_user.email == "nooka@gmail.com"
    assert res.status_code == 201


def test_login_user(test_user, client):
    res = client.post(
        "/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token,
                         settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('nooka@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('nooka@gmail.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post(
        "/login", data={"username": email, "password": password})

    assert res.status_code == status_code
    # assert res.json().get('detail') == 'Invalid Credentials'