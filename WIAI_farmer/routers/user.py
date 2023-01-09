from fastapi import APIRouter, Depends, HTTPException, status, Response
from WIAI_farmer.authentication import auth, oauth2
from ..utility import createObj, database
from .. import schemas
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta


router = APIRouter(
    tags=['User'],
)


@router.post("/authenticate", response_model=schemas.Token)
async def user_login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):
    """
    API for user login
    """

    # Legit user or not (Exists in database or not)
    farmer = createObj.get_farmer(form_data.username, db)

    # If not a user/farmer in the database, rasie
    if not farmer:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User does not exist, Need signup",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Else authenticate and login
    farmer = auth.authenticate_user(
        db, form_data.username, form_data.password
    )

    # if it fails, raise the exception with wrong credentials
    if not farmer:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect Password, Try 'temp@123' for first time user.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Access token time limit
    access_token_expires = timedelta(minutes=int(auth.ACCESS_TOKEN_EXPIRE_MINUTES))

    # Generating new access token
    access_token = auth.create_access_token(data={"sub": farmer.username}, expires_delta=access_token_expires)

    # Access token as response
    access_token = {
        "access_token": access_token,
        "access_token_type": "bearer",
    }
    return access_token


@router.post("/signup", response_model=schemas.FarmerDetail)
async def user_signup(
    signupitem: schemas.FarmerSignUp, 
    db: Session = Depends(database.get_db)
):
    """
    API for user signup and add data to the db
    """
    # Duplicate checks, if it already exists
    farmer = createObj.get_farmer(signupitem.username, db)

    # If user/farmer already, rasie
    if farmer:
        raise HTTPException(
            status_code=400,
            detail=f"Farmer with {signupitem.username} already exists",
        )

    # Else add the new user/farmer to the database
    farmer = createObj.create_farmer(db, signupitem)
    return farmer