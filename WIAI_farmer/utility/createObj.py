from ..authentication import auth
from .. import schemas, models
from sqlalchemy.orm import Session
from fastapi import HTTPException
from enum import Enum

class MyEnums(str, Enum):
    English = "en"
    Hindi = "hi"
    Marathi = "mr"
    Telugu = "te"
    Punjabi = "pa"


def create_farmer(db: Session, farmer: schemas.FarmerSignUp):
    db_farmer = models.Farmer(
        username=farmer.username,
        password=auth.get_password_hash(farmer.password),
        phone_number=farmer.username,
        farmer_name=farmer.farmer_name,
        state_name=farmer.state_name,
        district_name=farmer.district_name,
        village_name=farmer.village_name,
        is_active=True,
    )

    db.add(db_farmer)
    db.commit()
    db.refresh(db_farmer)
    return db_farmer


def get_farmer(username: str, db: Session):
    return db.query(models.Farmer).filter(models.Farmer.username == username).first()

def get_farmers(db: Session, skip: int = 0, limit: int = 5):
    return db.query(models.Farmer).offset(skip).limit(limit).all()

def get_farmers_all(db: Session):
    return db.query(models.Farmer).all()

def delete_farmer(username: str, db: Session):
    farmer = get_farmer(username, db)
    if not farmer:
        raise HTTPException(status_code=404, detail=f"User with {username} does not exists")
    db.delete(farmer)
    db.commit()

def create_farmer_csv(db: Session, farmer: schemas.FarmerSignUp):
    db_farmer = models.Farmer(
        username=farmer.username,
        phone_number=farmer.username,

        # Using "temp@123" as the password for all the famrers added through CSV
        password=auth.get_password_hash("temp@123"),
        farmer_name=farmer.farmer_name,
        state_name=farmer.state_name,
        district_name=farmer.district_name,
        village_name=farmer.village_name,
        is_active=True,
    )

    each_farmer = get_farmer(db_farmer.username, db)

    # Checking if it exists or not
    if not each_farmer:
        db.add(db_farmer)
        db.commit()
        db.refresh(db_farmer)
        return db_farmer

    return each_farmer

def update_details(
    db: Session,
    new_farmer: schemas.FarmerUpdate,
    curr_farmer: schemas.FarmerDetail,
):
    farmer_data = new_farmer.dict(exclude_unset=True)
    for key, pair in farmer_data.items():
        if pair != "string" and pair != "":
            if key == "password":
                setattr(curr_farmer, key, auth.get_password_hash(pair))
            else:
                setattr(curr_farmer, key, pair)

    db.add(curr_farmer)
    db.commit()
    db.refresh(curr_farmer)
    return curr_farmer