from fastapi import APIRouter

router = APIRouter()


@router.get("/")
@router.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}
