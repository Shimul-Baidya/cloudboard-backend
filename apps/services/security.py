# hashing + JWT
from datetime import timedelta, datetime, timezone
from dotenv import load_dotenv
from pwdlib import PasswordHash
import jwt
import os
import logging
from apps.config import SECRET_KEY

logger = logging.getLogger(__name__)

load_dotenv()

ALGORITHM = "HS256"

password_hash = PasswordHash.recommended()

DUMMY_HASH = password_hash.hash("dummypassword")

def get_password_hash(password):
    logger.info('Password hash created')
    return password_hash.hash(password)

def verify_password(plain_password, hashed_password):
    logger.info('Password verifying...')
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    logger.info('Access Token created')
    return encoded_jwt