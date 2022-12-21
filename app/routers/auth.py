

from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import models, schemas
from app import utils, oauth2
from app.database import get_db

router = APIRouter(
    tags=["Authtentication"]
)

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm=Depends(), db: Session = Depends(get_db)):

    # user_credentials structure - {"username": "fhghg", "password": "asfdf"}
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Invalid credentials")
    
    hashed_password = user.password
    #Validate the credetials like password
    if not utils.verify_password(user_credentials.password, hashed_password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid credentials")

    #create and return token 
    access_token = oauth2.create_access_token(data={"user_id": user.id})    # We can pass whatever the info into data to create token. here, we are passing only user id.

    return {"access_token": access_token, "token_type": "bearer"}   #need to configure this in front-end
    