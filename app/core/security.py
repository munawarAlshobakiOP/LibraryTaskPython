import os
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.schemas.internal_event import SecurityAuthFailed
from app.core.events import publish_internal_event


pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(password, hashed_password):
    """
    Verify a plain password against its hashed version.
    Args:
        password (str): The plain password to verify.
        hashed_password (str): The hashed password to compare against.
    Returns:
        bool: True if the password matches the hash, False otherwise.
    """

    return pwd.verify(password, hashed_password)


def get_password_hash(password):
    """
    Hash a plain password.
    Args:
        password (str): The plain password to hash.
    Returns:
        str: The hashed password.
    """
    return pwd.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Create a JWT access token.
    Args:
        data (dict): The data to encode in the token.
        expires_delta (timedelta | None): The token expiration time delta.
    Returns:
        str: The encoded JWT token.
    """
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


api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)


def validate_api_key(token: str) -> bool:
    """
    Validate the provided API key.
    Args:
        token (str): The API key to validate.
    Returns:
        bool: True if the API key is valid, False otherwise.
    """

    expected_key = os.getenv("API_KEY")
    if not expected_key:
        raise HTTPException(
            status_code=500,
            detail="API_KEY not configured on server",
        )
    return token == expected_key


def require_api_key(x_api_key: str | None = Security(api_key_header)):
    """
    Require a valid API key.
    Args:
        x_api_key (str | None): The API key provided in the request header.
    Raises:
        HTTPException: If the API key is missing or invalid.
    """
    if not x_api_key or not validate_api_key(x_api_key):
        publish_internal_event(SecurityAuthFailed(reason="Invalid or missing API key"))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Get the current user from the JWT token.
    Args:
        token (str): The JWT token provided in the request.
    Returns:
        dict: The payload of the JWT token.
    """
    secret = os.getenv("JWT_SECRET")
    algorithm = os.getenv("JWT_ALGORITHM", "HS256")

    if not secret:
        raise HTTPException(
            status_code=500,
            detail="JWT_SECRET not configured on server",
        )

    try:
        payload = jwt.decode(token, secret, algorithms=[algorithm])
        username: str = payload.get("sub")
        if username is None:
            publish_internal_event(
                SecurityAuthFailed(
                    reason="Could not validate credentials - missing username in token"
                )
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
    except JWTError:
        publish_internal_event(SecurityAuthFailed(reason="Invalid or malformed token"))
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
        publish_internal_event(
            SecurityAuthFailed(
                reason="Token expired", user_identifier=str(payload.get("sub"))
            )
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )

    return payload


def require_api_key_and_jwt(
    _: None = Depends(require_api_key),
    current_user=Depends(get_current_user),
):
    """
    Require both a valid API key and a valid JWT token.
    Args:
        _ (None): Placeholder for API key dependency.
        current_user: The current user obtained from the JWT token.
    Returns:
        dict: The payload of the JWT token.
    """
    return current_user
