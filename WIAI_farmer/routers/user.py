from fastapi import APIRouter, Depends, HTTPException
from .. import schemas, database, models, createObj
from sqlalchemy.orm import Session


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
