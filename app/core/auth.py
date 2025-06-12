from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def verify_password(plain_password, hashed_password):
    """Verifies if the provided password matches the hashed one."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """Hashes the given password."""
    return pwd_context.hash(password)


def create_access_token(data: dict):
    """Generates a JWT token with expiry."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str):
    """Decodes a JWT token to extract user identity."""
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload.get("sub")
    except JWTError:
        return None


def get_current_user(token: str = Depends(oauth2_scheme)):
    """FastAPI dependency to get current user email from token."""
    user_email = decode_token(token)
    if not user_email:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user_email
