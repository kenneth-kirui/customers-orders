
from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session
import jwt
from jwt.exceptions import InvalidTokenError

from app.schemas.token import TokenData
from ..config import settings

from ..database import get_session
from .. utilities.services import verify_password
from ..schemas.token import Token
from ..crud.customercrud import get_customer
from ..schemas.customer import Customer
from ..config import settings

SessionDep = Annotated[Session, Depends(get_session)]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY=settings.secret_key
ALGORITHM=settings.algorithm
router = APIRouter()

def authenticate_user(session, username:str, password:str):
  user = get_customer(email=username, session=session)
  if not user:
    return False
  if not verify_password(password, user.password):
    return False
  return user

def create_access_token(data:dict, expires_delta: timedelta |None=None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.now(timezone.utc) + expires_delta
  else:
    expire = datetime.now(timezone.utc) + timedelta(munitues=30)
  to_encode.update({"exp":expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt

async def get_current_user(token: Annotated[str,Depends(oauth2_scheme)], session:SessionDep):
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate":"Bearer"}
  )
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    if username is None:
      raise credentials_exception
    token_data = TokenData(username=username)
  except InvalidTokenError:
    raise credentials_exception
  user = get_customer(session=session, email= token_data.username)
  if user is None:
    raise credentials_exception
  return user
  
async def get_current_active_user(
      current_user: Annotated[Customer, Depends(get_current_user)]
  ):
    if current_user.disable:
      raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
    
@router.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session:SessionDep) -> Token:
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")