from fastapi import FastAPI
from .root import test_root_endpoint
from .users import test_users_endpoints
from .session import Session
from .tasks import test_tasks_endpoints

def test_app(app:FastAPI) -> None:
    session = Session()
    test_root_endpoint(app)
    test_users_endpoints(app,session)
    test_tasks_endpoints(app,session)
    session.logout()
    test_tasks_endpoints(app,session)