import os
from fastapi import FastAPI
from fastapi.testclient import TestClient
import random
import string
import re
import logging
from tests.session import Session

logging.basicConfig(level=logging.INFO)

letters_count = len(string.ascii_letters)
email_pattern = r'\w*@\w*\.com'

def test_users_endpoints(app:FastAPI,session:Session):
    _test_register_endpoint(app,session)

def _test_register_endpoint(app:FastAPI,session:Session):
    client = TestClient(app)
    
    username = _fake_username()
    email = _fake_email(False)
    invalid_email = _fake_email(True)
    password = _fake_username()
    valid_data = {
        "username":username,
        "email":email,
        "password":password
    }
    invalid_data = {
        "username":username,
        "email":invalid_email,
        "password":password
    }
    errors_list = []
    _check_response(valid_data,client,errors_list)
    token = _test_token_endpoint(client,{
        "username":username,
        "password":password
    },200,errors_list)
    _check_response(invalid_data,client,errors_list)
    _test_token_endpoint(client,{
        "username":username
    },422,errors_list)
    _test_token_endpoint(client,{
        "username":username+'@',
        "password":password
    },401,errors_list)
    _test_token_endpoint(client,{
        "username":username,
        "password":password+'@'
    },401,errors_list)
    if len(errors_list) == 0:
        session.authenticate(username,token)

def _test_token_endpoint(client:TestClient,data:dict,expected_code:int,errors:list) -> str:
    response = client.post("/api/v1/token",data=data)
    try:
        assert response.status_code == expected_code
        if expected_code == 200:
            return response.json()['access_token']
        return None # type: ignore
    except AssertionError as err:
        errors.append(data)
        logging.error(f'STATUS CODE ------> EXPECTED {expected_code}, gets: {response.status_code}\n{response.json()}')
        return None # type: ignore

def _check_response(data:dict,client:TestClient,errors:list):
    response = client.post('/api/v1/register',json=data)
    expected_status_code = 422 if re.fullmatch(email_pattern,data['email']) == None else 201
    try:
        assert response.status_code == expected_status_code
    except AssertionError as err:
        errors.append(data)
        logging.error(f'STATUS CODE ------> EXPECTED {expected_status_code}, gets: {response.status_code}')

def _fake_username() -> str:
    username_length = random.randint(5,15)
    username = ''
    for _ in range(username_length):
        username += string.ascii_letters[random.randint(0,letters_count - 1)]
    return username

def _fake_email(bad:bool) -> str:
    prob = 0.25
    head_length = random.randint(5,10)
    email = ''
    for _ in range(head_length):
        email += string.ascii_letters[random.randint(0,letters_count - 1)]
    if random.random() <= prob or not bad:
        email += "@"
    for _ in range(head_length):
        email += string.ascii_letters[random.randint(0,letters_count - 1)]
    if random.random() <= prob or not bad:
        email += "."
    email += 'com'
    return email
