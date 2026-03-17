from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from pydantic import ValidationError
from app.core.config import settings
from app.core.database import get_database
from app.domain.models.user import TokenData, UserResponse
from bson import ObjectId

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except (jwt.PyJWTError, ValidationError):
        raise credentials_exception
        
    db = get_database()
    user = await db.users.find_one({"email": token_data.email})
    if user is None:
        raise credentials_exception
        
    return UserResponse(id=str(user["_id"]), email=user["email"], name=user["name"])
