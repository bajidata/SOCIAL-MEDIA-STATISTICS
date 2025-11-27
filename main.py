import uvicorn
import asyncio
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routers import social_routes
from controller.core import base_router

# Import bot module
from bot.telegram_bot import run_telegram_bot   # <-- HERE


app = FastAPI(title="Social Media Statistics API")

app.include_router(base_router.router)
app.include_router(social_routes.router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(run_telegram_bot())   # run bot in background


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
