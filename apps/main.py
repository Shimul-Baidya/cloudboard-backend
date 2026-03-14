from fastapi import FastAPI
from apps.database import engine, Base
from sqlalchemy import text
from contextlib import asynccontextmanager
from apps.models import user

Base.metadata.create_all(engine)

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

