from fastapi import APIRouter, Depends, HTTPException, UploadFile, File

from ..authentication import auth, oauth2

from ..utility import createObj, database, googleTranslate
from .. import schemas, models
from sqlalchemy.orm import Session


router = APIRouter(
    tags=['Translate'],
)

@router.get("/farmers/{language}", response_model=list[schemas.FarmerPhone])
async def farmer_data_language(
    language: str = "hi",
    db: Session = Depends(database.get_db),
    farmer: schemas.FarmerDetail = Depends(oauth2.get_current_active_user),
):

    # fetching all the data here
    farmers = createObj.get_farmers_all(db)

    # going through every row of data fetched
    for i in farmers:
        # combining the rows to translate it altogether
        translated_data = await googleTranslate.join_farmer_data(i, language)
        
        print(translated_data)
        # changing the data to the translated data
        i.farmer_name = translated_data[0].strip()
        i.state_name = translated_data[1].strip()
        i.district_name = translated_data[2].strip()
        i.village_name = translated_data[3].strip()

    # returning the list with translated data
    return farmers

@router.get("/translate", response_model=schemas.Message)
async def translate_a_string(
    language: str = "hi",
    text: str = "Sonpari Ai Ai Ai",
    farmer: schemas.FarmerDetail = Depends(oauth2.get_current_active_user),
):

    # calling the helper function to translate the text
    translated_text = await googleTranslate.translate_text(text, language)
    translated_text = translated_text["translatedText"]

    # returning ok status after successful translation
    data = {
        "status": "ok",
        "details": translated_text,
        "language": language,
    }
    return data