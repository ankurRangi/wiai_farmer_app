from pydantic import BaseModel

class FarmerExport(BaseModel):
    farmer_name: str
    state_name: str
    district_name: str
    village_name: str