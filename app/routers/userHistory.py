from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Event, UserEventRegistration
from datetime import datetime

router = APIRouter()

from pydantic import BaseModel
from datetime import datetime

class EventHistory(BaseModel):
    event_id: int
    title: str
    event_date: datetime
    club_name: str
    feedback_status: str  # Status based on the feedback in the user_event_registrations table

    class Config:
        orm_mode = True

@router.get('/event-history', response_model=list[EventHistory])
def event_history(request: Request, db: Session = Depends(get_db)):
    # Get the authenticated user's ID from the session (replace this with actual authentication logic)
    user_info = request.session.get('user')

    if not user_info:
        raise HTTPException(status_code=401, detail="User not authenticated")

    user_id = user_info.get('id')

    # Fetch events that the user has attended using the UserEventRegistration model
    registrations = db.query(UserEventRegistration).filter(UserEventRegistration.user_id == user_id).all()

    event_history = []
    for registration in registrations:
        event = registration.event  # Access the Event related to the registration

        # Check if feedback exists (feedback is part of the UserEventRegistration model)
        feedback_status = "Reviewed" if registration.feedback else "Not Reviewed"
        
        event_history.append(EventHistory(
            event_id=event.id,
            title=event.title,
            event_date=event.event_date,
            club_name=event.club.name,  # Assuming event has a 'club' relationship
            feedback_status=feedback_status
        ))

    return event_history
