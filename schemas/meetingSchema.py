from datetime import datetime
from typing import Optional, Union
import config.access as access
from pydantic import BaseModel, EmailStr
from schemas.fundSchema import Fund

class MeetingBase(BaseModel):
    meetingName: str
    description: Union[str, None] = None
    rules: Union[str, None] = None
    picture: Optional[str]
    


class MeetingCreate(MeetingBase):
    pass


class Meeting(MeetingBase):
    id: int
    created_date: datetime
    owner_id: int
    funds: list[Fund] = []
    
    class Config:
        orm_mode = True
        
class MeetingUpdate(BaseModel):
       meetingName: Optional[str]
       description: Optional[str]
       rules: Optional[str]
       picture: Optional[str]
       
       
class MeetingFund(BaseModel):
    funds: list[Fund] = []