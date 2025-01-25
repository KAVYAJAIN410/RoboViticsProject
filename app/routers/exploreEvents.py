from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models import Event, Club, User, UserEventRegistration
from datetime import datetime

router = APIRouter()
class ClubCard(BaseModel):
    id: int
    name: str
    description: str
    

class EventCard(BaseModel):
    id: int
    title: str
    club_name: str
    date: datetime
    venue: str
    description: str
    registration_status: str

@router.get('/explore/events', response_model=dict)
def explore_events(db: Session = Depends(get_db)):
    trending_events = db.query(Event).order_by(Event.participants.desc()).limit(5).all()
    upcoming_events = db.query(Event).order_by(Event.event_date.asc()).limit(5).all()
    popular_clubs = db.query(Club).all()

    return {
        "trending_events": [
            EventCard(
                id=event.id,
                title=event.title,
                club_name=event.club.name,
                date=event.event_date,
                venue=event.location,
                description=event.description,
                registration_status="N/A"
            ) for event in trending_events
        ],
        "upcoming_events": [
            EventCard(
                id=event.id,
                title=event.title,
                club_name=event.club.name,
                date=event.event_date,
                venue=event.location,
                description=event.description,
                registration_status="N/A"
            ) for event in upcoming_events
        ],
        "popular_clubs": [
            ClubCard(id=club.id, name=club.name, description=club.description) for club in popular_clubs
        ]
    }