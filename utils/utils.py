from turtle import mode
from schemas.schemas import Token, TokenData
import schemas.schemas as schema
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import models.model as model
from fastapi import Depends,HTTPException, status
from jose import JWTError, jwt
from typing import Union
from config.access import SECRET_KEY, ALGORITHM
from fastapi.security import OAuth2PasswordBearer
from config.database import SessionLocal

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




# Création de Token
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



# Decodage d'un token reçu
def get_current_user( db : Session, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(db , email=token_data.email)
    Email = token_data.email
    if user is None:
        raise credentials_exception
    return Email




#comparaison des password hashé
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)



# hashage de password
def get_password_hash(password):
   return pwd_context.hash(password)



# Vérification lors de l'inscription
def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.password):
      return False
    return user



#Recherche d'un utilisateur par son id
def get_user(db: Session, user_id: int):
    user=db.query(model.User).filter(model.User.id == user_id).first()
    return user 



# Recherche d'un utilisateur par son email
def get_user_by_email(db: Session, email: str):
    return db.query(model.User).filter(model.User.email == email).first()



# Recherche de tous les utilisateur
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.User).offset(skip).limit(limit).all()

#rechercher un utilisateur 
def get_one_user(db:Session, user_id: int):
    return db.query(model.User).filter(model.User.id == user_id ) 


# Creation d'un utilisateur
def create_user(db: Session, user: schema.UserCreate):
    hashed_password = get_password_hash(user.password)
    new_user = model.User(firstName = user.firstName,
                         lastName = user.lastName,
                         email=user.email, 
                         bio = user.bio,
                         picture = user.picture,
                         country = user.country,
                         city = user.city,
                         created_date = datetime.utcnow(),
                         password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



#Recherche de toutes les tontines
def get_meetings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.Meeting).offset(skip).limit(limit).all()


#Verification de l'existence d'une tontine
def get_meeting(db: Session, meeting_id: int):
    meeting=db.query(model.Meeting).filter(model.Meeting.id == meeting_id).first()
    return meeting 

#rechercher un meeting
def get_meeting_by_meetingName(db: Session, meetingName: str):
    return db.query(model.Meeting).filter(model.Meeting.meetingName == meetingName).first()

#Creation d'une tontine
def create_user_meeting(db: Session, meeting: schema.MeetingCreate, user_id: int):
    new_meeting = model.Meeting(**meeting.dict(), owner_id=user_id, created_date = datetime.utcnow())
    db.add(new_meeting)
    db.commit()
    db.refresh(new_meeting)
    return new_meeting

#verifier si un fond existe
def get_fund(db: Session, fund_id: int):
    fund=db.query(model.Fund).filter(model.Fund.id == fund_id).first()
    return fund 

#lister les funds
def get_all_fund(meeting_id: int, db: Session):
    return db.query(model.Fund).filter(model.Fund.meeting_id==meeting_id).all()

#Creation d'une caisse
def create_meeting_fund(db: Session, fund: schema.FundsCreate, meeting_id: int):
    new_funds = model.Fund(**fund.dict(), meeting_id=meeting_id, created_date = datetime.utcnow())
    db.add(new_funds)
    db.commit()
    db.refresh(new_funds)
    return new_funds

#rechercher un fund
def get_fund_by_fundName(db: Session, fundName: str):
    return db.query(model.Fund).filter(model.Fund.fundName == fundName).first()

# Recherches de toutes les caisses d'une reunion
def get_funds(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.Meeting).offset(skip).limit(limit).all()

#lister des cotisations 
def get_all_cotisations(fund_id: int, db: Session):
    return db.query(model.Cotisation).filter(model.Cotisation.fund_id==fund_id).all()

#Creation d'une caisse
def create_fund_cotisation(db: Session, cotisation: schema.CotisationCreate , fund_id: int):
    print("hello")
    new_cotisation = model.Cotisation(**cotisation.dict(), fund_id=fund_id, created_date = datetime.utcnow())
    print(new_cotisation)
    print("hello")
    db.add(new_cotisation)
    db.commit()
    db.refresh(new_cotisation)
    return new_cotisation
