from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel
from schemas.cotisationSchema import Cotisation

# Model de création de fund
class FundBase(BaseModel):
    fundName: str
    description: Union[str, None] = None
    
class FundsCreate(FundBase):
    pass


class Fund(FundBase):
    id: int
    created_date: datetime
    meeting_id: int
    cotisations: list[Cotisation] = []
    
    class Config:
        orm_mode = True
