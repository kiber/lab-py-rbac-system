from fastapi import FastAPI

from . import database, models, seed_database
from .errors import register_exception_handlers
from .routers import auth_router, permission_router, role_router, user_router

models.Base.metadata.create_all(bind=database.engine)
seed_database.seed()

app = FastAPI()
register_exception_handlers(app)

app.include_router(auth_router.router)
app.include_router(permission_router.router)
app.include_router(role_router.router)
app.include_router(user_router.router)
