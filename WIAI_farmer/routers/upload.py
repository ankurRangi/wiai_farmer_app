from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from .. import schemas, database, models, createObj, auth, oauth2
from sqlalchemy.orm import Session


import csv, codecs

router = APIRouter(
    tags=['Upload'],
)

# API to upload CSV to database
@router.post("/upload")
async def upload_farmer_data_using_csv(
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db),
    farmer: schemas.FarmerDetail = Depends(oauth2.get_current_active_user),
):
    csvReader = csv.DictReader(codecs.iterdecode(file.file, "utf-8"))

    for rows in csvReader:
        db_farmer = schemas.FarmerDetail(
            username=rows["phone_number"],
            farmer_name=rows["farmer_name"],
            state_name=rows["state_name"],
            district_name=rows["district_name"],
            village_name=rows["village_name"],
        )
        # Saving the data to the Database
        createObj.create_farmer_csv(db, db_farmer)

    file.file.close()

    # Status - Added successfully
    data = {"status": "ok", "detail": "file uploaded successfully"} # add status for better visuals
    return data