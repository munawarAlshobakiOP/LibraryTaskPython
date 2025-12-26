import os
from fastapi import Header, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(password, hashed_password):
    return pwd.verify(password, hashed_password)


def get_password_hash(password):
    return pwd.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})

    secret = os.getenv("JWT_SECRET")
    algorithm = os.getenv("JWT_ALGORITHM")

    if not secret:
        raise HTTPException(
            status_code=500,
            detail="JWT_SECRET not configured on server",
        )

    encoded_jwt = jwt.encode(to_encode, secret, algorithm=algorithm)
    return encoded_jwt


def require_api_key(x_api_key: str | None = Header(default=None, alias="X-API-KEY")):
    expected_key = os.getenv("API_KEY")

    if not expected_key:
        raise HTTPException(
            status_code=500,
            detail="API_KEY not configured on server",
        )

    if not x_api_key or x_api_key != expected_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    secret = os.getenv("JWT_SECRET")
    algorithm = os.getenv("JWT_ALGORITHM", "HS256")

    if not secret:
        raise HTTPException(
            status_code=500,
            detail="JWT_SECRET not configured on server",
        )

    try:
        payload = jwt.decode(token, secret, algorithms=[algorithm])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or malformed token",
        )

    exp = payload.get("exp")
    if not exp:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing expiration",
        )

    if datetime.now(timezone.utc).timestamp() > exp:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )

    return payload


def require_api_key_and_jwt(
    _: None = Depends(require_api_key),
    current_user=Depends(get_current_user),
):
    return current_user
