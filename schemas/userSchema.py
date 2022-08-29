from  schemas.meetingSchema  import Meeting
from datetime import datetime
from typing import Optional, Union
import config.access as access
from pydantic import BaseModel, EmailStr

# class Token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Union[str, None] = None

# models d'enregistrement d'un utilisateur
class UserBase(BaseModel):
    firstName : str
    lastName : str
    email: EmailStr
    bio : Optional[str]
    picture: Optional[str]
    country : Optional[str]
    city : Optional[str]
    

class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    created_date: datetime
    meetings: list[Meeting] = []

    class Config:
        orm_mode = True

# model de connexion d'un utilisateur*
class UserSignIn(BaseModel):
    email: EmailStr
    password: str
    
class userUpdate(BaseModel):
    email : Optional[EmailStr]
    firstName: Optional[str]
    lastName: Optional[str]
    picture: Optional[str]
    bio: Optional[str]
