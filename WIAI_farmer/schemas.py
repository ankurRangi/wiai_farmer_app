from pydantic import BaseModel
from typing import Union, Optional


class FarmerBase(BaseModel):
    username: str

class FarmerLogIn(FarmerBase):
    password: str

class FarmerDetail(FarmerBase):
    farmer_name: str
    state_name: str
    district_name: str
    village_name: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "farmer_name": "Rajesh",
                "state_name": "Haryana",
                "district_name": "Rohtak",
                "village_name": "Meham",
            }
        }
class FarmerCreate(FarmerDetail):
    password: str
    disabled: Union[bool, None] = None

class FarmerUpdate(BaseModel):
    farmer_name: Optional[str] = None
    state_name: Optional[str] = None
    district_name: Optional[str] = None
    village_name: Optional[str] = None
    password: Optional[str] = None

class FarmerPhone(FarmerDetail):
    phone_number: str

class FarmerSignUp(FarmerDetail):
    password: str
    class Config:
        orm_mode = True
        schema_extra = {
        "example": {
            "username": "9999999999",
            "password": "password",
            "farmer_name": "Rajesh",
            "state_name": "Haryana",
            "district_name": "Rohtak",
            "village_name": "Meham",

        }
    }

class Token(BaseModel):
    access_token: str
    access_token_type: str