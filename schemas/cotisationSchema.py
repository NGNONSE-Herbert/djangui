from datetime import datetime
from typing import Union
from pydantic import BaseModel


# Model de création de fund
class CotisationBase(BaseModel):
    description: str
    
class CotisationCreate(CotisationBase):
    pass


class Cotisation(CotisationBase):
    id: int
    created_date: datetime
    fund_id: int
    
    
    class Config:
        orm_mode = True
