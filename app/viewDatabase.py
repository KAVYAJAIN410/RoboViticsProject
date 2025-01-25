from faker import Faker
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func  
from random import choice, randint
from models import Event, Club  

fake = Faker()

def create_random_event(session: Session):
    # Generate random event data
    title = fake.sentence(nb_words=5)
    description = fake.paragraph(nb_sentences=3)
    event_date = fake.date_this_year(after_today=True)
    location = fake.city()
    event_type = choice(['Sports', 'Workshop', 'Seminar', 'Meetup', 'Conference'])
    participants = randint(10, 200)
    event_status = choice(['Scheduled', 'Completed', 'Cancelled'])
    registration_deadline = event_date - timedelta(days=randint(1, 10)) if event_status != 'Cancelled' else None
    event_embedding = [randint(0, 10) for _ in range(300)]  # Example random embedding (you can use a more sophisticated approach for this)

    # Optional: Choose a random club (if you have clubs in the database)
    club = session.query(Club).order_by(func.random()).first()

    # Create an event object
    event = Event(
        title=title,
        description=description,
        event_date=event_date,
        location=location,
        event_type=event_type,
        participants=participants,
        event_status=event_status,
        registration_deadline=registration_deadline,
        event_embedding=event_embedding,
        club=club
    )

    # Add and commit the event to the session
    session.add(event)
    session.commit()

# Usage
def add_random_events_to_db(session: Session, num_events: int):
    for _ in range(num_events):
        create_random_event(session)

# Example usage in the script or interactive shell
with Session() as session:
    add_random_events_to_db(session, 10)  # Adds 10 random events to the database
