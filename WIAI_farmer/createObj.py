from . import schemas, models, auth
from sqlalchemy.orm import Session

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


def get_farmer(db: Session, username: str):
    return db.query(models.Farmer).filter(models.Farmer.username == username).first()

def get_farmers(db: Session, skip: int = 0, limit: int = 5):
    return db.query(models.Farmer).offset(skip).limit(limit).all()



