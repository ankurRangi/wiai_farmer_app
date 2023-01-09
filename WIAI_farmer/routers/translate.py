from fastapi import APIRouter, Depends, Query
from ..authentication import oauth2
from ..utility import createObj, database, googleTranslate
from .. import schemas
from sqlalchemy.orm import Session



router = APIRouter(
    tags=['Translate'],
)

@router.get("/farmers/{language}", response_model=list[schemas.FarmerPhone])
async def farmer_data_language(
    language: createObj.MyEnums,
    db: Session = Depends(database.get_db),
    farmer: schemas.FarmerDetail = Depends(oauth2.get_current_active_user),
):
    """
    API to retrive the data from the db in a specifc language i.e English (Default), Hindi, Marathi, Telegu, Punjabi
    """
    # print(language.value.key)
    language = language.value

    # Retriving all the data here
    farmers = createObj.get_farmers_all(db)

    # Looping over each row
    for i in farmers:
        # Tranlating each entry for the particular row
        translated_data = await googleTranslate.join_farmer_data(i, language)
        
        # Converting the entries to send the data back in that language
        i.farmer_name = translated_data[0].strip()
        i.state_name = translated_data[1].strip()
        i.district_name = translated_data[2].strip()
        i.village_name = translated_data[3].strip()

    return farmers