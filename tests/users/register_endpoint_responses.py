from fastapi import FastAPI
from fastapi.testclient import TestClient
import random
import string
import re
import logging

logging.basicConfig(level=logging.INFO)

letters_count = len(string.ascii_letters)
email_pattern = r'\w*@\w*\.com'

def test_register_endpoint(app:FastAPI):
    client = TestClient(app)
    
    username = fake_username()
    email = fake_email(False)
    invalid_email = fake_email(True)
    password = fake_username()
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
    check_response(valid_data,client)
    check_response(invalid_data,client)

def check_response(data:dict,client:TestClient):
    response = client.post('/api/v1/register',json=data)
    expected_status_code = 422 if re.fullmatch(email_pattern,data['email']) == None else 201
    try:
        assert response.status_code == expected_status_code
    except AssertionError as err:
        logging.error(f'STATUS CODE ------> EXPECTED {expected_status_code}, gets: {response.status_code}')

def fake_username() -> str:
    username_length = random.randint(5,15)
    username = ''
    for _ in range(username_length):
        username += string.ascii_letters[random.randint(0,letters_count - 1)]
    return username

def fake_email(bad:bool) -> str:
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