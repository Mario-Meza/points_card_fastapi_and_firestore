from fastapi import FastAPI
from routers import tarjetas_lealtad
from db.client import get_database, close_firebase
app = FastAPI()
app.include_router(tarjetas_lealtad.router)
app.add_event_handler("startup", get_database)
app.add_event_handler("shutdown", close_firebase)

@app.get("/")
async def root():
    return {"message": "Hello World"}
