from pydantic import BaseModel
from passlib.context import CryptContext
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer
from fastapi.exceptions import RequestValidationError
from datetime import datetime, timedelta
from jose import jwt

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String
from sqlalchemy.future import select

DATABASE_URL = "sqlite+aiosqlite:///./test.db"
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()

class UserInDB(Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True, index=True)
    hashed_password = Column(String)

class BlacklistedToken(Base):
    __tablename__ = "blacklisted_tokens"
    token = Column(String, primary_key=True, index=True)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await init_db()


async def blacklist_token(token: str):
    async with SessionLocal() as session:
        blacklisted = BlacklistedToken(token=token)
        session.add(blacklisted)
        await session.commit()

async def check_blacklist(token: str):
    async with SessionLocal() as session:
        result = await session.execute(select(BlacklistedToken).where(BlacklistedToken.token == token))
        return result.scalars().first() is not None

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
from pydantic import BaseModel
from datetime import datetime, timedelta
from passlib.context import CryptContext
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from fastapi.exceptions import RequestValidationError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(BaseModel):
    username: str
    password: str

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# JWT settings and functions remain unchanged


SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return payload
    except jwt.JWTError:
        raise credentials_exception

@app.post("/register", tags=["auth"])
async def register(user: User):
    async with SessionLocal() as session:
        result = await session.execute(select(UserInDB).where(UserInDB.username == user.username))
        existing_user = result.scalars().first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already registered")
        hashed_password = hash_password(user.password)
        new_user = UserInDB(username=user.username, hashed_password=hashed_password)
        session.add(new_user)
        await session.commit()
        return {"message": "User registered successfully"}


@app.post("/login", tags=["auth"])
async def login(user: User):
    async with SessionLocal() as session:
        result = await session.execute(select(UserInDB).where(UserInDB.username == user.username))
        user_db = result.scalars().first()
        if not user_db or not verify_password(user.password, user_db.hashed_password):
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        access_token = create_access_token(data={"sub": user_db.username})
        refresh_token = create_refresh_token(data={"sub": user_db.username})
        return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}



@app.post("/refresh", tags=["auth"])
async def refresh_token(refresh_token: str):
    try:
        payload = verify_token(refresh_token, credentials_exception=HTTPException(status_code=401, detail="Invalid token or expired token"))
        username = payload.get("sub")
        async with SessionLocal() as session:
            result = await session.execute(select(UserInDB).where(UserInDB.username == username))
            user_db = result.scalars().first()
            if not user_db:
                raise HTTPException(status_code=404, detail="User not found")
        new_access_token = create_access_token(data={"sub": username})
        return {"access_token": new_access_token, "token_type": "bearer"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token or expired token")



oauth2_scheme = HTTPBearer()
@app.post("/logout", tags=["auth"])
async def logout(token: str = Depends(oauth2_scheme)):
    token = token.credentials
    if await check_blacklist(token):
        raise HTTPException(status_code=400, detail="Token already in blacklist")
    await blacklist_token(token)
    return {"message": "Successfully logged out"}



@app.get("/users/me", tags=["auth"])
async def read_users_me(token: str = Depends(oauth2_scheme)):
    token = token.credentials
    if await check_blacklist(token):
        raise HTTPException(status_code=401, detail="Invalid token or expired token")
    try:
        payload = verify_token(token, credentials_exception=HTTPException(status_code=401, detail="Invalid token or expired token"))
        username = payload.get("sub")
        async with SessionLocal() as session:
            result = await session.execute(select(UserInDB).where(UserInDB.username == username))
            user = result.scalars().first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
        return {"username": user.username}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token or expired token")



# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
