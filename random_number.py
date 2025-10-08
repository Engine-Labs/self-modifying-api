import random

from fastapi import APIRouter

router = APIRouter()


@router.get("/random-number")
def generate_random_number():
    return {"random_number": random.randint(1, 100)}
