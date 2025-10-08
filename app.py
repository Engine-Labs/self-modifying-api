from dotenv import load_dotenv
from fastapi import FastAPI

import endpoints
import healthcheck
import random_number

load_dotenv()

app = FastAPI()

app.include_router(healthcheck.router)
app.include_router(endpoints.router)
app.include_router(random_number.router)
