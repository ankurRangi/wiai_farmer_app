# Making a database connection

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Creating an engine
SQLALCHEMY_DATABASE_URL = "sqlite:///./farmerdb.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db" 

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args = {"check_same_thread" : False} 
    # echo (agr) = true, signifies it is in memory
)
# Creating a session
SessionLocal = sessionmaker(bind = engine, autocommit=False, autoflush=False)

# Declare a mapping
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()  

