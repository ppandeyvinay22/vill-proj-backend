from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.core.database import get_database
from app.domain.models.user import UserCreate, UserResponse, UserInDB, Token
from app.auth.security import get_password_hash, verify_password, create_access_token
from app.api.deps import get_current_user
from datetime import timedelta
from app.core.config import settings

router = APIRouter()

@router.post("/signup", response_model=UserResponse)
async def signup(user_in: UserCreate):
    db = get_database()
    existing_user = await db.users.find_one({"email": user_in.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this username already exists in the system.",
        )
    
    hashed_password = get_password_hash(user_in.password)
    new_user = {
        "email": user_in.email,
        "name": user_in.name,
        "hashed_password": hashed_password
    }
    
    result = await db.users.insert_one(new_user)
    return UserResponse(id=str(result.inserted_id), email=user_in.email, name=user_in.name)


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = get_database()
    user = await db.users.find_one({"email": form_data.username})
    
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
        
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
async def login_test_token(current_user: UserResponse = Depends(get_current_user)):
    return current_user
