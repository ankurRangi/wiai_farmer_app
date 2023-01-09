from passlib.context import CryptContext
from ..utility import createObj
from .. import schemas
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta

import keys


SECRET_KEY = keys.SECRET_KEY
ALGORITHM = keys.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = keys.ACCESS_TOKEN_EXPIRE_MINUTES


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def authenticate_user(db: Session, username: str, password: str):
    farmer = createObj.get_farmer(username, db)
    if not farmer:
        return False
    if not verify_password(password, farmer.password):
        return False
    return farmer


def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(access_token: str, credentials_exception):
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        access_token_data = schemas.FarmerBase(username=username)
        return access_token_data
    except JWTError:
        raise credentials_exception
        