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

@router.get("/farmers", response_model=list[schemas.FarmerPhone])
async def fetch_all_farmer(
    db: Session = Depends(database.get_db),
    farmer: schemas.FarmerDetail = Depends(oauth2.get_current_active_user),
):
    """
    Endpoint to get the list of all the farmers from the database
    """
    # Retriving the data from db
    farmers = createObj.get_farmers_all(db)
    return farmers


@router.post("/signup", response_model=schemas.FarmerDetail)
async def user_signup(
    signupitem: schemas.FarmerSignUp, db: Session = Depends(database.get_db)
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


@router.post("/login", response_model=schemas.Token)
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

    # Saving the token details in cookie for future use
    response.set_cookie(key="access_token", value=f"Bearer {access_token}")

    # Access token as response
    access_token = {
        "access_token": access_token,
        "access_token_type": "bearer",
    }
    return access_token

@router.patch("/update/{username}", response_model=schemas.FarmerDetail)
async def update_farmer_data(
    username: str,
    new_farmer: schemas.FarmerUpdate,
    farmer: schemas.FarmerDetail = Depends(oauth2.get_current_active_user),
    db: Session = Depends(database.get_db),
):
    """
    APi to update the details for the authenticated user in the database 
    """
    # User can change details for themselves only and not for other users
    if username != farmer.username:
        raise HTTPException(
            status_code=401,
            detail="Not authorised to change details for a diferent user, check your details and try again",
        )
        # detail=f"Not authorised to change details for a diferent user - {username}, check your id - {farmer.username} and try again",
        # Need to change it for testing purpose

    # Otherwise, just update it
    return createObj.update_details(db, new_farmer, farmer)

@router.delete("/delete")
async def user_login(
    username: str,
    db: Session = Depends(database.get_db),
    farmer: schemas.FarmerDetail = Depends(oauth2.get_current_active_user),
):  
    """
    API to delete the entry for a particular authenticated user from the database using the phone_number/username
    & cannot delete entry for any other user
    """

    # User can delete for themselves only and not for other users
    if username != farmer.username:
        raise HTTPException(
            status_code=401,
            detail=f"Not authorised to delete details for a diferent user - {username}, check your id - {farmer.username} and try again",
        )
    # Delete the user from database
    createObj.delete_farmer(username, db)
    return {"Status": "Yes", "Details": f"User with {username} is successfully deleted"}


