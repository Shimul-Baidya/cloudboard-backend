from fastapi import FastAPI, Depends, HTTPException
from apps.database import SessionLocal, engine, Base
from sqlalchemy import text
from contextlib import asynccontextmanager
from apps.models import user as user_model
from apps.schemas import user as user_schema
from sqlalchemy.orm import Session


# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

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


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users", response_model=user_schema.UserResponse)
def create_user(user: user_schema.CreateUser, db: Session = Depends(get_db)):
    if db.query(user_model.User).filter(user_model.User.email == user.email).first(): # TODO: understand this syntax
        raise HTTPException(status_code=409, detail="Email already exists!")
    
    # create a new user
    new_user = user_model.User(**user.model_dump())
    # TODO: understand this syntax
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/users/{user_id}", response_model=user_schema.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(user_model.User).filter(user_model.User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/health")
def health():
    return {"status": "Okay"}

