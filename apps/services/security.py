# hashing + JWT

from pwdlib import PasswordHash

SECRET_KEY = "7e6eca543daca05da7bf972edc276c7cde8340060730cb0d4bb6c329cefbfba8"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 

password_hash = PasswordHash.recommended()

DUMMY_HASH = password_hash.hash("dummypassword")

def get_password_hash(password):
    return password_hash.hash(password)

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)