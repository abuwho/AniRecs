from pydantic import BaseModel
from passlib.context import CryptContext
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer
from fastapi.exceptions import RequestValidationError
from datetime import datetime, timedelta
from jose import jwt


blacklisted_tokens = set()

def blacklist_token(token: str):
    blacklisted_tokens.add(token)

def check_blacklist(token: str):
    return token in blacklisted_tokens

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(BaseModel):
    username: str
    password: str

class UserInDB(User):
    hashed_password: str

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)



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




app = FastAPI()

# Mock database
db = {}

@app.post("/register", tags= ["auth"])
async def register(user: User):
    if user.username in db:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = hash_password(user.password)
    db[user.username] = UserInDB(**user.dict(), hashed_password=hashed_password)
    return {"message": "User registered successfully"}

@app.post("/login", tags= ["auth"])
async def login(user: User):
    user_db = db.get(user.username)
    if not user_db or not verify_password(user.password, user_db.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}

@app.post("/refresh", tags= ["auth"])
async def refresh_token(refresh_token: str):
    try:
        payload = verify_token(refresh_token, credentials_exception=HTTPException(status_code=401, detail="Invalid token or expired token"))
        username = payload.get("sub")
        new_access_token = create_access_token(data={"sub": username})
        return {"access_token": new_access_token, "token_type": "bearer"}
    except RequestValidationError:
        raise HTTPException(status_code=401, detail="Invalid token or expired token")


oauth2_scheme = HTTPBearer()

@app.post("/logout", tags= ["auth"])
async def logout(token: str = Depends(oauth2_scheme)):
    token = token.credentials
    if check_blacklist(token):
        raise HTTPException(status_code=400, detail="Token already in blacklist")
    blacklist_token(token)
    return {"message": "Successfully logged out"}

@app.get("/users/me", tags= ["auth"])
async def read_users_me(token: str = Depends(oauth2_scheme)):
    token = token.credentials
    if check_blacklist(token):
        raise HTTPException(status_code=401, detail="Invalid token or expired token")
    try:
        payload = verify_token(token, credentials_exception=HTTPException(status_code=401, detail="Invalid token or expired token"))
        username = payload.get("sub")
        if username is None or username not in db:
            raise HTTPException(status_code=404, detail="User not found")
        user = db[username]
        return {"username": user.username}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token or expired token")

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
