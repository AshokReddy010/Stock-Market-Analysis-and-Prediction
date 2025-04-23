from fastapi import APIRouter, Depends # type: ignore
from app.dependencies.auth import get_current_user

router = APIRouter()

@router.get("/user-profile")
def user_dashboard(current_user=Depends(get_current_user)):
    return {"message": f"Hello {current_user.username}, welcome to your dashboard!"}
