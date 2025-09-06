import os
from fastapi import FastAPI
from fastapi.testclient import TestClient
import random
import string
import re
import logging
from ..session import Session

logging.basicConfig(level=logging.INFO)

letters_count = len(string.ascii_letters)
email_pattern = r'\w*@\w*\.com'

def test_users_endpoints(app:FastAPI,session:Session):
    '''
    tests the users endpoints
    '''
    _test_register_endpoint(app,session)

def _test_register_endpoint(app:FastAPI,session:Session):
    '''
    tests the POST resgister endpoint
    '''
    client = TestClient(app)
    # create a username
    username = _fake_username()
    # create a valid email
    email = _fake_email(False)
    # create a no-valid email
    invalid_email = _fake_email(True)
    # create a password
    password = _fake_username()
    # create a valid data
    valid_data = {
        "username":username,
        "email":email,
        "password":password
    }
    # create an inavalid data
    invalid_data = {
        "username":username,
        "email":invalid_email,
        "password":password
    }
    errors_list = []
    _check_response(valid_data,client,errors_list)
    # try to get an access token
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
    '''
    tests the login endpoint and try to get an access token

    param: expected_code:int -> the expected status code for this operation
    '''
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
    '''
    tests the register endpoint
    '''
    response = client.post('/api/v1/register',json=data)
    expected_status_code = 422 if re.fullmatch(email_pattern,data['email']) == None else 201
    try:
        assert response.status_code == expected_status_code
    except AssertionError as err:
        errors.append(data)
        logging.error(f'STATUS CODE ------> EXPECTED {expected_status_code}, gets: {response.status_code}')

def _fake_username() -> str:
    '''
    returns a random username
    '''
    username_length = random.randint(5,15)
    username = ''
    for _ in range(username_length):
        username += string.ascii_letters[random.randint(0,letters_count - 1)]
    return username

def _fake_email(bad:bool) -> str:
    '''
    returns a random email

    param: bad:bool:
        if true, returns an invalid email, else returns a valid email
    '''
    head_length = random.randint(5,10)
    email = ''
    for _ in range(head_length):
        email += string.ascii_letters[random.randint(0,letters_count - 1)]
    if not bad:
        email += "@"
    for _ in range(head_length):
        email += string.ascii_letters[random.randint(0,letters_count - 1)]
    if not bad:
        email += "."
    email += 'com'
    return email
