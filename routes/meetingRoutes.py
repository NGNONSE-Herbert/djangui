
from typing import List
from fastapi import Depends, APIRouter, HTTPException,status
from sqlalchemy.orm import Session
import utils.utils as utils, models.model as model
from utils.utils import get_db
from schemas import schemas
from models.model import Cotisation, Fund, Meeting

meeting_router = APIRouter(
    prefix= '/meeting',
    tags=['meeting']
)
# Liste de tous les utilisateurs
@meeting_router.get("/", response_model=list[schemas.Meeting])
def read_meetings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        items = utils.get_meetings(db, skip=skip, limit=limit)
        return items
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=" not found data ")
    
@meeting_router.get("/{meeting_id}/", response_model=schemas.Meeting)
def read_one_user(meeting_id: int, db: Session = Depends(get_db)):
    try:
        meeting =db.query(Meeting).filter(Meeting.id== meeting_id).first()
        return meeting
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=" not found data ")


        
#liste des funds
@meeting_router.get("/{meeting_id}/fund/", response_model=list[schemas.Fund])
def read_funds(meeting_id: int, db: Session = Depends(get_db)):
    try:
        meetingId = utils.get_meeting(db=db, meeting_id=meeting_id)
        if meetingId:
            items = utils.get_all_fund(meeting_id = meeting_id, db=db)
            return items
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=" id doesn't exist ")
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=" id doesn't exist ")

#rechercher un fond par grace a son id
@meeting_router.get("/fund/{fund_id}", response_model= schemas.Fund)
def read_fund_for_id(fund_id: int, db : Session = Depends(get_db)):
    try:
        fund =db.query(Fund).filter(Fund.id== fund_id).first()
        return fund
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=" not found data ")


#creer un meeting
@meeting_router.post("/{meeting_id}/fund/", response_model=schemas.Fund)
def create_fund_for_meeting(meeting_id: int, fund: schemas.FundsCreate, db: Session = Depends(get_db)):
    try:
        meeting = utils.get_meeting(db=db, meeting_id=meeting_id)
        if meeting:
            fun = utils.get_fund_by_fundName(db=db, fundName=fund.fundName)
            if not fun:
                Fund = utils.create_meeting_fund(db=db, fund=fund, meeting_id=meeting_id)
                return Fund
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail=" this name is bad")
        elif meeting is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail=" id unknow ")
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail=" incorrect data entry")

@meeting_router.put("/{meeting_id}/", response_model=schemas.Meeting) 
def update_user(meeting_id: int,meeting: schemas.MeetingUpdate, db: Session = Depends(get_db)):
    try:
        meeting_update=db.query(Meeting).filter(Meeting.id== meeting_id).first()
        if meeting.meetingName:
            meeting_update.meetingName =meeting.meetingName
        if meeting.description:
            meeting_update.description=meeting.description
        if meeting.rules:
            meeting_update.rules=meeting.rules
        if meeting.picture:
            meeting_update.picture = meeting.picture
        db.add(meeting_update)
        db.commit()
        db.refresh(meeting_update)
        return meeting_update
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=" not found data ")


#liste des cotisations  
@meeting_router.get("/{fund_id}/cotisation/", response_model=list[schemas.Cotisation])
def read_cotisations(fund_id: int, db: Session = Depends(get_db)):
    try:
        fundId = utils.get_fund(db=db, fund_id=fund_id)
        if fundId:
            items = utils.get_all_cotisations(fund_id=fund_id, db=db)
            return items
        else:
           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=" id doesn't exist ") 
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=" id doesn't exist ")

#rechercher une cotisation grace a son id
@meeting_router.get("/cotisation/{fund_id}/", response_model= schemas.Cotisation)
def read_cotisation_for_id(cotisation_id: int, db : Session = Depends(get_db)):
    try:
        cotisation =db.query(Cotisation).filter(Cotisation.id== cotisation_id).first()
        if cotisation:
            return cotisation
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=" not found data ")

    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=" not found data ")


#creer une cotisation
@meeting_router.post("/fund/{fund_id}/cotisation", response_model=schemas.Cotisation)
def create_cotisation_for_fund(fund_id: int, cotisation: schemas.CotisationCreate , db: Session = Depends(get_db)):
    try:
        fund = utils.get_fund(db=db, fund_id=fund_id)
        if fund:
            print(cotisation)
            Cotisation = utils.create_fund_cotisation(db=db, fund_id=fund_id, cotisation=cotisation)
            return Cotisation
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail=" unknow id ")
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail=" incorrect data entry")