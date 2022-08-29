from operator import index
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship

from config.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    firstName = Column(String, index=True)
    lastName = Column(String, index=True)
    email = Column(String, index=True)
    bio = Column(String, index=True)
    picture = Column(String, index=True)
    country = Column(String,index=True)
    city = Column(String, index=True)
    password = Column(String, index=True)
    created_date = Column(DateTime, index=True)

    meetings = relationship("Meeting", back_populates="owner")
 

class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True, index=True)
    meetingName = Column(String, index=True)
    rules = Column(Text, index=True)
    description = Column(String, index=True)
    picture = Column(String, index=True)
    created_date = Column(DateTime, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="meetings")
    funds = relationship("Fund", back_populates= "owner")
  

class Fund(Base):
    __tablename__ = "funds"
    id = Column(Integer, primary_key=True, index=True)
    fundName = Column(String, index=True)
    description = Column(String, index=True)
    created_date = Column(DateTime, index=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id"))

    owner = relationship("Meeting", back_populates="funds")
    cotisations = relationship("Cotisation", back_populates= "owner")
    
    
class Cotisation(Base):
    __tablename__ = "cotisations"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    created_date = Column(DateTime, index=True)
    fund_id = Column(Integer, ForeignKey("funds.id"))

    owner = relationship("Fund", back_populates="cotisations")
    
    
