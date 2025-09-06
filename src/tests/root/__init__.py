from fastapi import FastAPI
from fastapi.testclient import TestClient
from .endpoints_responses import expected_responses
import logging

logging.basicConfig(level=logging.INFO)

def test_root_endpoint(app:FastAPI):
    client = TestClient(app)

    for endpoint in expected_responses.keys():
        response = client.get(endpoint)
        try:
            assert response.status_code == 200
            assert response.json() == expected_responses[endpoint]
            logging.info(f"'{endpoint}' endpoint is working correctly")
        except AssertionError as err:
            logging.error(f"Bad working on '{endpoint}' endpoint")
            logging.error(f"STATUS CODE ----> EXPECTED: 200, gets : {response.status_code}")
            logging.error(f"BODY ----> EXPECTED : {expected_responses[endpoint]}, gets: {response.json()}")