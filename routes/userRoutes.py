from typing import List
from fastapi import Depends,HTTPException,status
from sqlalchemy.orm import Session
from datetime import timedelta
from models.model import Meeting, User
import utils.utils as utils
from schemas import schemas
from config.access import ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi import APIRouter
from utils.utils import get_db, get_user


user_router = APIRouter(
    prefix= '/user',
    tags=['user']
)



# Requêtes concernant les users

# Enregistrement d'un utilisateur
@user_router.post("/signup", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = utils.get_user_by_email(db, email=user.email)
        if db_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        return utils.create_user(db=db, user=user)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail=" incorrect data entry")

# connexion d'un utilisateur
@user_router.post("/signin",response_model=schemas.Token)
def signIn(user: schemas.UserSignIn, db: Session = Depends(get_db)):
    try:
        check_user = utils.authenticate_user(db, email=user.email, password=user.password)
        if not check_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="email or password incorrect")
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = utils.create_access_token(data={"sub": user.email}, 
                                                 expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}
      
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail=" incorrect data entry")



# Recuperation de tous les utilisateurs
@user_router.get("/all/{token}", response_model=list[schemas.User])
def read_users(token: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        user = utils.get_current_user(token)
        if user :
            users = utils.get_users(db, skip=skip, limit=limit)
            return users
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=" not found data ")

# Recuperation d'un seul utilisateur
@user_router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    try:
        db_user = utils.get_user(db, user_id=user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=" not found data ")
    
@user_router.put("/{user_id}", response_model=schemas.User) 
def update_user(user_id: int,user: schemas.userUpdate, db: Session = Depends(get_db)):
    try:
        user_update=db.query(User).filter(User.id== user_id).first()
        if user.email:
            user_update.email =user.email
        if user.firstName:
            print(user_update.firstName)
            user_update.firstName=user.firstName
        if user.lastName:
            user_update.lastName=user.lastName
        if user.picture:
            user_update.picture = user.picture
        if user.bio:
            user_update.bio=user.bio
        db.add(user_update)
        db.commit()
        db.refresh(user_update)
        return user_update
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=" not found data ")

    
# Creation d'une tontine par un utilisateur
@user_router.post("/{user_id}/meeting/", response_model=schemas.Meeting)
def create_meeting_for_user(user_id: int, meeting: schemas.MeetingCreate, db: Session = Depends(get_db)):
    try:
        user = utils.get_user(user_id=user_id, db = db)
        if user:
            meetin = utils.get_meeting_by_meetingName(db=db, meetingName=meeting.meetingName)
            if not meetin:
                Meeting = utils.create_user_meeting(db=db, meeting=meeting, user_id=user_id)
                return Meeting
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=" meeting name exist ")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=" id unknow ")
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail=" id unknow ")
    

#liste des metting d'un utilisateur 
@user_router.get("/{user_id}/meeting/", response_model=List[schemas.Meeting])
def read_user_meeting(user_id: int, db: Session = Depends(get_db)):
    try:
        user = utils.get_one_user(user_id=user_id, db = db)
        if user:
            meetin = db.query(Meeting).filter(Meeting.owner_id == user_id).all()
            return meetin
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail=" user_id unknow ")
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail=" user_id unknow ")
            








