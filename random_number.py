from fastapi import APIRouter
import random

router = APIRouter()

@router.get("/random-number")
def generate_random_number():
    return {"random_number": random.randint(1, 100)}