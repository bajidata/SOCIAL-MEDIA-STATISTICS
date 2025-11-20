from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
# Importing your existing controller
from controller.SocialMedia_Controller import SocialMedia_Controller 

# Create the router instance
router = APIRouter(
    prefix="/api",
    tags=["Social Media Statistics"]
)

# Define what input we expect from the user
class StatsRequest(BaseModel):
    platform: str
    brand: str
    date: str

# Initialize your controller
controller = SocialMedia_Controller()

@router.get("/")
async def get_root():
    return {"message": "Social Media API is running"}


#send post request to our controller
@router.post("/stats")
async def get_stats(request: StatsRequest):
    # 1. Extract data from Request
    # 2. Pass it to Controller
    # 3. Return whatever the Controller gives us
    return controller.process_stats(
        platform=request.platform, 
        brand=request.brand, 
        date=request.date
    )