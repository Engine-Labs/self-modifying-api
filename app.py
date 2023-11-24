from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

import healthcheck
import endpoints

app.include_router(healthcheck.router)
app.include_router(endpoints.router)

import random_number

app.include_router(random_number.router)
