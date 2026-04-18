from fastapi import FastAPI
from apps.database import engine
from sqlalchemy import text
from contextlib import asynccontextmanager
from apps.routers import others
from apps.routers import user as user_router


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
        print("Database connection successful")
    except Exception as e:
        print("Database connection failed")
        print(e)

    yield  


app = FastAPI(lifespan=lifespan)

app.include_router(others.router)
app.include_router(user_router.router)

