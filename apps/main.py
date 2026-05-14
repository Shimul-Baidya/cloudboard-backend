from fastapi import FastAPI
from apps.database import engine
from sqlalchemy import text
from contextlib import asynccontextmanager
from apps.routers.others import router as others_router
from apps.routers.user import router as user_router
from apps.routers.auth import router as auth_router
from apps import config
import logging

logger = logging.getLogger(__name__)


# TODO: I need to reflect on what I have accomplished so far to internalize the knowledge
# with Session(engine) as session:
#     spongebob = user.User(
#         email="spongebob@krustykrab.com",
#         hashed_password="spongebob",
#         role="user"
#     )
#     session.add(spongebob)
#     session.commit()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        logger.info('Database connection successful')
    except Exception as e:
        logger.error("Database connection failed")
        logger.exception(e)

    yield  


app = FastAPI(lifespan=lifespan)

app.include_router(others_router)
app.include_router(user_router)
app.include_router(auth_router)

