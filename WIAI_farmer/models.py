from database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

class farmer(Base):
    
    __tablename__ = "farmerdb"

    user_id = Column(Integer)
    user_name = Column(String, primary_key=True, index=True, unique= True) # Considering each unique user with its phone number
    phone_number = Column(String, unique=True)
    password = Column(String)
    farmer_name = Column(String)
    state_name = Column(String)
    district_name = Column(String)
    village_name = Column(String)
    is_active = Column(Boolean, default=True)

