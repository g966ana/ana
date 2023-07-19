from fastapi import FastAPI
from src.controllers import azure_wrapper

app = FastAPI()

app.include_router(azure_wrapper.router)