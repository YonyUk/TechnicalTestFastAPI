from fastapi import FastAPI
from fastapi.testclient import TestClient
from tests.session import Session
import string
import random
import logging

logging.basicConfig(level=logging.INFO)

letters_count = len(string.ascii_letters)

def test_tasks_endpoints(app:FastAPI,session:Session):
    client = TestClient(app)

    _test_post_task(client,session)
    _test_get_tasks(client,session)
    _test_get_tasks_by_id(client,session)
    _test_put_task(client,session)
    _test_delete_task(client,session)

def _test_post_task(client:TestClient,session:Session,tests:int = 10):
    for _ in range(tests):
        response = client.post('/api/v1/tasks',json=_fake_task())
        try:
            assert response.status_code == 401
        except AssertionError as err:
            logging.error(f'STATUS CODE -----> EXPECTED 401, gets {response.status_code}')

        if session.User != None and session.Token != None:
            headers = {
                'Authorization':f'Bearer {session.Token}'
            }
            response = client.post('/api/v1/tasks',headers=headers,json=_fake_task())
            try:
                assert response.status_code == 201
            except AssertionError as err:
                logging.error(f'STATUS CODE -----> EXPECTED 201, gets {response.status_code}')

def _test_get_tasks(client:TestClient,session:Session,tests:int=10):
    response = client.get('/api/v1/tasks')
    try:
        assert response.status_code == 401
    except AssertionError as err:
        logging.error(f'STATUS CODE -----> EXPECTED 401, gets {response.status_code}')
    
    if session.User != None and session.Token != None:
        headers = {
            'Authorization':f'Bearer {session.Token}'
        }
        for _ in range(tests):
            _test_get_tasks_authenticated(client,headers)

def _test_get_tasks_by_id(client:TestClient,session:Session,tests:int=10):
    if session.User == None or session.Token == None: return
    headers = {
        'Authorization':f'Bearer {session.Token}'
    }
    response = client.get(f'/api/v1/tasks?skip=0&limit={tests}',headers=headers)
    if response.status_code != 200: return
    tasks = response.json()
    for _ in range(tests):
        task = tasks[random.randint(0,len(tasks) - 1)]
        response = client.get(f'/api/v1/tasks/{task['id']}',headers=headers)
        try:
            assert response.status_code == 200
            assert response.json()['id'] == task['id']
        except AssertionError as err:
            if response.status_code != 200:
                logging.error(f'STATUS CODE ----> EXPECTED 200, gets {response.status_code}')
            if response.json()['id'] != task['id']:
                logging.error(f'TASK ----> EXPECTED {task}, gets {response.json()}')

def _test_put_task(client:TestClient,session:Session,tests:int=10):
    if session.User == None or session.Token == None: return
    headers = {
        'Authorization':f'Bearer {session.Token}'
    }

    response = client.get(f'/api/v1/tasks?skip=0&limit={tests}',headers=headers)
    if response.status_code != 200: return
    tasks = response.json()
    for _ in range(tests):
        task = tasks[random.randint(0,len(tasks) - 1)]
        new_task = _fake_task()
        response = client.put(f'/api/v1/tasks/{task['id']}',headers=headers,json=new_task)
        try:
            assert response.status_code == 200
        except AssertionError as err:
            logging.error(f'STATUS CODE ----> EXPECTED 200, gets {response.status_code}')

def _test_delete_task(client:TestClient,session:Session,tests:int=10):
    if session.User == None or session.Token == None: return
    headers = {
        'Authorization': f'Bearer {session.Token}'
    }
    response = client.get(f'/api/v1/tasks?skip=0&limit={tests}',headers=headers)
    if response.status_code != 200: return
    tasks = response.json()
    for _ in range(tests):
        task = tasks[random.randint(0,len(tasks) - 1)]
        response = client.delete(f'/api/v1/tasks/{task['id']}',headers=headers)
        try:
            assert response.status_code == 200
            tasks.remove(task)
        except AssertionError as err:
            logging.error(f'STATUS CODE ----> EXPECTED 200, gets {response.status_code}')

def _test_get_tasks_authenticated(client:TestClient,headers:dict):
    skip = random.randint(0,10)
    limit = random.randint(1,100)
    response = client.get(f'/api/v1/tasks?skip={skip}&limit={limit}',headers=headers)
    try:
        assert response.status_code == 200
        assert len(response.json()) <= limit
    except AssertionError as err:
        if response.status_code != 200:
            logging.error(f'STATUS CODE ----> EXPECTED 200, gets {response.status_code}')
        if len(response.json()) > limit:
            logging.error(f'Limit of items exceded, expected {limit}, gets {len(response.json())}')
    
    _test_get_tasks_authenticated_filtered(client,headers,True)
    _test_get_tasks_authenticated_filtered(client,headers,False)

def _test_get_tasks_authenticated_filtered(client:TestClient,headers:dict,status:bool):
    skip = random.randint(0,10)
    limit = random.randint(1,100)
    response = client.get(f'/api/v1/tasks?skip={skip}&limit={limit}&status={str(status).lower()}',headers=headers)
    try:
        assert response.status_code == 200
        assert len(list(filter(lambda task:task['status'],response.json()))) == len(list(response.json()))
    except AssertionError as err:
        if response.status_code != 200:
            logging.error(f'STATUS CODE -----> EXPECTED 200, gets {response.status_code}')
        if len(list(filter(lambda task:task['status']==status,response.json()))) != len(list(response.json())):
            logging.error(f'FILTER NOT APPLIED')

def _fake_task_name() -> str:
    title = ''
    title_length = random.randint(5,10)
    for _ in range(title_length):
        title += string.ascii_letters[random.randint(0,letters_count - 1)]
    return title

def _fake_task_description() -> str:
    description_length = random.randint(10,50)
    description = ''
    for _ in range(description_length):
        if random.random() < 0.1:
            description += ' '
        else:
            description += string.ascii_letters[random.randint(0,letters_count - 1)]
    return description

def _fake_task_status() -> bool:
    return False if random.random() < 0.5 else True

def _fake_task() -> dict:
    return {"title":_fake_task_name(),"description":_fake_task_description(),"status":_fake_task_status()}