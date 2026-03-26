from fastapi import FastAPI
from apps.database import engine, Base
from sqlalchemy import text
from contextlib import asynccontextmanager
from apps.models import user
from sqlalchemy.orm import Session

Base.metadata.create_all(engine)

with Session(engine) as session:
    spongebob = user.User(
        email="spongebob@krustykrab.com",
        hashed_password="spongebob",
        role="user"
    )
    session.add(spongebob)
    session.commit()

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


@app.get("/health")
def health():
    return {"status": "Okay"}

