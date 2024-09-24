from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from app.database import get_db
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app import schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schemas.Token)
# def login(user_credentials:schemas.UserLogin, db: Session = Depends(get_db)):
def login(user_credentials:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    # create a token
    access_token = oauth2.create_access_token(data={"user_id":user.id})

    #return token
    return{"access_token": access_token, "token_type": "bearer"}





