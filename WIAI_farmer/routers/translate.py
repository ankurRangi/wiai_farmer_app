from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from .. import schemas, database, models, createObj, auth, oauth2, googleTranslate
from sqlalchemy.orm import Session


router = APIRouter(
    tags=['Translate'],
)

@router.get("/farmers/{language}", response_model=list[schemas.FarmerPhone])
async def farmer_data_language(
    language: str = "Hindi",
    db: Session = Depends(database.get_db),
    farmer: schemas.FarmerDetail = Depends(oauth2.get_current_active_user),
):

    # fetching all the data here
    farmers = createObj.get_farmers_all(db)

    # going through every row of data fetched
    for i in farmers:
        # combining the rows to translate it altogether
        translated_data = await googleTranslate.join_farmer_data(i, language)

        # changing the data to the translated data
        i.farmer_name = translated_data[0]
        i.state_name = translated_data[1]
        i.district_name = translated_data[2]
        i.village_name = translated_data[3]

    # returning the list with translated data
    return farmers

@router.get("/translate", response_model=schemas.Status)
async def translate_the_given_text(
    language: str = "Hindi",
    text: str = "test",
    farmer: schemas.FarmerDetail = Depends(oauth2.get_current_active_user),
):

    # calling the helper function to translate the text
    translated_text = await googleTranslate.translate_text(text, language)
    translated_text = translated_text["translatedText"]

    # returning ok status after successful translation
    data = {
        "status": "ok",
        "detail": f"You translated text is {translated_text}",
    }
    return data