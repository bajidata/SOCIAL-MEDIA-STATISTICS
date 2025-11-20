from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import date, timedelta
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
    today = date.today()

    yesterday = today - timedelta(days=1) # Yesterday Date
    first_day_of_month = today.replace(day=1) # First Date of Month
    yesterday_date = yesterday.strftime("%d-%m-%Y")
    if request.date == "Daily":
        date_range = [
            (first_day_of_month + timedelta(days=i)).strftime("%d-%m-%Y")
            for i in range((yesterday - first_day_of_month).days + 1)
        ]
    elif request.date == "Weekly":
        start_date = yesterday - timedelta(days=6)
        start_date = max(start_date, first_day_of_month)

        date_range = [
            (start_date + timedelta(days=i)).strftime("%d-%m-%Y")
            for i in range((yesterday - start_date).days + 1)
        ]
    
    else:
        date_range = [
            (first_day_of_month + timedelta(days=i)).strftime("%d-%m-%Y")
            for i in range((yesterday - first_day_of_month).days + 1)
        ]

    return controller.process_stats(
        platform=request.platform, 
        brand=request.brand,
        yesterday_date=yesterday_date, 
        date=date_range
    )
