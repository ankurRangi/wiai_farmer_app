from fastapi import APIRouter, Depends, UploadFile, File

from ..authentication import oauth2

from ..utility import createObj, database
from .. import schemas
from sqlalchemy.orm import Session


import csv, codecs

router = APIRouter(
    tags=['Upload'],
)

@router.post("/upload")
async def upload_farmer_data_using_csv(
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db),
    farmer: schemas.FarmerDetail = Depends(oauth2.get_current_active_user),
):
    """
    API to upload farmers data via a CSV file to the database from an authenticated login
    """
    # Reading the file uploaded
    csvReader = csv.DictReader(codecs.iterdecode(file.file, "utf-8"))

    # Looping over each entry provided
    for rows in csvReader:
        db_farmer = schemas.FarmerDetail(
            username=rows["phone_number"],
            farmer_name=rows["farmer_name"],
            state_name=rows["state_name"],
            district_name=rows["district_name"],
            village_name=rows["village_name"],
        )
        # Adding the data to the db, with conditions
        createObj.create_farmer_csv(db, db_farmer)

    file.file.close()

    # Added successfully
    data = {"status": "ok", "detail": "file data uploaded successfully"} # add status for better visuals
    return data