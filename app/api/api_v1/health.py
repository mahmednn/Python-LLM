from fastapi import APIRouter, status

router = APIRouter()

@router.get("/check")
def health():
    return {"status": status.HTTP_200_OK}
