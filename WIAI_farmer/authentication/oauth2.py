from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from ..authentication import auth

from ..utility import createObj, database
from .. import schemas
from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(access_token: str = Depends(oauth2_scheme), 
    db: Session = Depends(database.get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = auth.verify_token(access_token, credentials_exception)
    farmer = createObj.get_farmer(token_data.username, db)
    if farmer is None:
        raise credentials_exception
    return farmer

async def get_current_active_user(
    farmer: schemas.FarmerDetail = Depends(get_current_user),
):
    if not farmer:
        raise HTTPException(status_code=400, detail="User does not exist")
    return farmer

def authenticate_user(db: Session, username: str, password: str):
    farmer = createObj.get_farmer(username, db)
    if not farmer:
        return False
    if not auth.verify_password(password, farmer.password):
        return False
    return farmer