from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.security import create_access_token, verify_password
from app.repositories.user_repository_impl import SQLUserRepository
from app.schemas.auth import Token
from app.schemas.user import UserCreate, User as UserSchema
from app.services.user_service import UserService

router = APIRouter(tags=["authentication"])


def get_user_service(db: Session = Depends(get_db)):
    """
    Get an instance of the UserService with a database session.
    Args:
        db (Session): The database session.
    Returns:
        UserService: An instance of UserService.
    """
    return UserService(SQLUserRepository(db))


@router.post(
    "/register", response_model=UserSchema, status_code=status.HTTP_201_CREATED
)
async def register(request: UserCreate, svc: UserService = Depends(get_user_service)):
    """
    Register a new user.
    Args:
        request (UserCreate): The user data to create.
        svc (UserService): The user service instance.
    Returns:
        The created user.
    """
    if svc.get_user_by_username(request.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    return svc.create_user(request.username, request.password)


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    svc: UserService = Depends(get_user_service),
):
    """
    Authenticate a user and provide an access token.
    Args:
        form_data (OAuth2PasswordRequestForm): The login form data.
        svc (UserService): The user service instance.
    Returns:
        A token containing the access token and token type.
    """
    user = svc.get_user_by_username(form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.username, "user_id": str(user.id)}
    )
    return {"access_token": access_token, "token_type": "bearer"}
