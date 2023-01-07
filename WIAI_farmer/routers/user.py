from fastapi import APIRouter, Depends, HTTPException, status, Response
from .. import schemas, database, models, createObj, oauth2, auth
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta



router = APIRouter(
    tags=['User'],
)

@router.get("/farmers", response_model=list[schemas.FarmerPhone])
async def fetch_all_farmer_data(
    db: Session = Depends(database.get_db),
    farmer: schemas.FarmerDetail = Depends(oauth2.get_current_active_user),
):
    farmers = createObj.get_farmers_all(db)
    return farmers

@router.post("/signup", response_model=schemas.FarmerDetail)
async def user_signup(
    signupitem: schemas.FarmerSignUp, db: Session = Depends(database.get_db)
):
    # Duplicate checks
    farmer = createObj.get_farmer(signupitem.username, db)

    # If user/farmer already exists
    if farmer:
        raise HTTPException(
            status_code=400,
            detail=f"Farmer with {signupitem.username} already exists",
        )

    # Else create the new user/farmer
    farmer = createObj.create_farmer(db, signupitem)
    return farmer

# User login API/endpoint
@router.post("/login", response_model=schemas.Token)
async def user_login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):

    # Legit user or not (Exists in database or not)
    farmer = createObj.get_farmer(db, form_data.username)

    # Error if not
    if not farmer:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Your details doesn't exist, please signup first",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # iElse authenticate 
    farmer = auth.authenticate_user(
        db, form_data.username, form_data.password
    )

    # if it fails, raise the exception with wrong credentials
    if not farmer:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong Password, If you are trying for first time, password is your phone-number.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Access token time limit
    access_token_expires = timedelta(
        minutes=int(auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    # Generating new access token
    access_token = auth.create_access_token(
        data={"sub": farmer.username}, expires_delta=access_token_expires
    )

    # Saving the token details in cookie for future use
    response.set_cookie(key="access_token", value=f"Bearer {access_token}")

    # returning the access token as response
    access_token = {
        "access_token": access_token,
        "access_token_type": "bearer",
    }
    return access_token
