from fastapi import FastAPI
from contextlib import asynccontextmanager

from fastapi.responses import JSONResponse
from src.database import engine, Base
from src.api import task, user
import logging
from scalar_fastapi import get_scalar_api_reference,Layout  # pyright: ignore[reportPrivateImportUsage]

# alembic migrations
from alembic.config import Config
from alembic import command
import os

# logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_migrations():
    '''
    runs the migrations
    '''
    path_config = os.path.join(os.getcwd(),'alembic.ini')
    alembic_cfg = Config(path_config)
    command.upgrade(alembic_cfg,'head')

@asynccontextmanager
async def lifespan(app: FastAPI):
    # apply migrations before start
    run_migrations()
    # Crear tablas al iniciar (en desarrollo)
    # En producción, usar migraciones con Alembic
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    yield
    logger.info("Shutting down...")

app = FastAPI(
    title="Todo API",
    description="API for manage tasks TODO with FastAPI y PostgreSQL",
    version="1.0.0",
    lifespan=lifespan,
    docs_url=None
)

# adds routers
app.include_router(user.router, prefix="/api/v1", tags=["users"])
app.include_router(task.router, prefix="/api/v1", tags=["tasks"])

@app.get("/")
async def root():
    return {"message": "Bienvenido a la Todo API"}

# global error manage
@app.exception_handler(404)
async def not_found_exception_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": "Recurso no encontrado"},
    )

@app.exception_handler(500)
async def internal_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"message": "Error interno del servidor"},
    )

# adds documentation with scalar-fastapi
@app.get("/docs",include_in_schema=False)
async def scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url, # type: ignore
        title='TODO API Documentation',
        layout=Layout.MODERN,
        dark_mode=True,
        show_sidebar=True,
        default_open_all_tags=True,
        hide_download_button=False,
        hide_models=False,
        servers=[{'url':'http://localhost:8000','description':'local server'}]
    )