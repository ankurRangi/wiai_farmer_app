from .utility.database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

class Farmer(Base):
    
    __tablename__ = "farmerdb"

    # user_id = Column(Integer)
    username = Column(String, primary_key=True, index=True, unique= True) # Considering each unique user by its phone number as username
    phone_number = Column(String)
    password = Column(String)
    farmer_name = Column(String)
    state_name = Column(String)
    district_name = Column(String)
    village_name = Column(String)
    is_active = Column(Boolean, default=True)

