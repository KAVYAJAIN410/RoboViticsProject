from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models import Event
from app.models import Club
from datetime import datetime


 
router = APIRouter()

class EventCard(BaseModel):
    id: int
    title: str
    club_name: str
    date: datetime
    venue: str
    description: str
    registration_status: str

@router.get('/event/{event_id}', response_model=EventCard)
def event_details(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    club=db.query(Club).filter(Club.id==Event.club_id).first()
    clubName=club.name if club else "No club associated"
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    return EventCard(
        id=event.id,
        title=event.title,
        club_name=clubName,
        date=event.event_date,
        venue=event.location,
        description=event.description,
        registration_status="N/A"
    )



