
from jose import jwt, JWTError
from datetime import datetime, timedelta
from app import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app import models, database
from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")     # /login is the end-point in login in auth.py

'''
For creating JWT token, basically we need three parameters
1. SECRET key (It can be some string)
2. Algorithm (Specify which algorithm you want to use)
3. Expiration time (Specify till when the user can access the API. If you don't give the expiration date, then API can be accesible forever. which is not happen in real time.)
'''

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()     #create a copy for data as we don't want to change the actual data

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)     #Use utcnow() 
    to_encode.update({"exp": expire})

    #jwd.encode is used to create jwt token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")        # "user_id" is the key that we have given in login while creating the JWT token

        if id is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credentials_exception
    
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session =  Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user