from fastapi import APIRouter, Depends, HTTPException, status, Response
from .. import schemas, database, models, createObj
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm



router = APIRouter(
    tags=['User'],
)


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

# endpoint for the users to login
@router.post("/login", response_model=schemas.Token)
async def user_login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):

    # firstly checking whether the farmer exist in the database or not
    farmer = createObj.get_farmer(db, form_data.username)

    # if it does not exist, raise the exception
    if not farmer:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Your details doesn't exist, please signup first",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # if it exists, authenticate the farmer
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

    # access token time limit
    access_token_expires = timedelta(
        minutes=int(ACCESS_TOKEN_EXPIRES_MINUTES)
    )

    # creting a new access token
    access_token = auth.create_access_token(
        data={"sub": farmer.username}, expires_delta=access_token_expires
    )

    # saving the token for future api calls
    response.set_cookie(key="access_token", value=f"Bearer {access_token}")

    # returning the access token as response
    access_token = {
        "access_token": access_token,
        "access_token_type": "bearer",
    }
    return access_token
