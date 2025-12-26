from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import create_access_token, verify_password, get_password_hash
from app.schemas.auth import Token, LoginRequest

router = APIRouter(tags=["authentication"])

MOCK_USERS = {
    "admin": {
        "username": "admin",
        "password_hash": get_password_hash("password123"),
        "user_id": "1",
    }
}


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = MOCK_USERS.get(form_data.username)
    if not user or not verify_password(form_data.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user["username"], "user_id": user["user_id"]}
    )
    return {"access_token": access_token, "token_type": "bearer"}
