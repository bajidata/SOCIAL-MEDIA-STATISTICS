import uvicorn
from fastapi import FastAPI
from routers import social_routes

# Initialize the App
app = FastAPI(title="Social Media Statistics API")

# Include the router we created in Step 2
app.include_router(social_routes.router)

# This allows you to run the file directly with `python main.py`
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)