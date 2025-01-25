from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, CheckConstraint
from sqlalchemy.orm import declarative_base, relationship
from pgvector.sqlalchemy import Vector

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    registration_number = Column(String(255), unique=True, nullable=True)  
    email = Column(String(255), unique=True, nullable=False)  
    name = Column(String(255), nullable=False) 
    mobile_number = Column(String(10), unique=True, nullable=True) 
    preference_embedding = Column(Vector(300))  
 
    registrations = relationship('UserEventRegistration', back_populates='user')
    search_history = relationship('UserSearchHistory', back_populates='user')
    notifications = relationship('Notification', back_populates='user')  
    
    __table_args__ = (
        CheckConstraint(
            r"registration_number ~ '^\d{2}[A-Z]{3}\d{4}$'", 
            name='check_registration_number_format'
        ),
        CheckConstraint(
            r"email ~ '^[a-zA-Z0-9._%+-]+@vit\.ac\.in$'", 
            name='check_email_domain'
        ),
        CheckConstraint(
            r"mobile_number ~ '^\d{10}$'", 
            name='check_mobile_number_format'
        ),
    )


class Club(Base):
    __tablename__ = 'clubs'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    
    events = relationship('Event', back_populates='club')


class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    event_date = Column(TIMESTAMP, nullable=False)
    location = Column(String(255))
    event_type = Column(String(255))  
    participants = Column(Integer)
    event_status = Column(String(255))
    registration_deadline = Column(TIMESTAMP, nullable=True)
    event_embedding = Column(Vector(300))  # Adjust the dimension as needed
    club_id = Column(Integer, ForeignKey('clubs.id'), nullable=True)  # Club association
    
    registrations = relationship('UserEventRegistration', back_populates='event')
    club = relationship('Club', back_populates='events')


class UserEventRegistration(Base):
    __tablename__ = 'user_event_registrations'
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    event_id = Column(Integer, ForeignKey('events.id', ondelete='CASCADE'), primary_key=True)
    registration_date = Column(TIMESTAMP, nullable=False)
    feedback = Column(Text, nullable=True)  
    
    user = relationship('User', back_populates='registrations')
    event = relationship('Event', back_populates='registrations')


class UserSearchHistory(Base):
    __tablename__ = 'user_search_history'
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    search_query = Column(Text, primary_key=True)
    search_timestamp = Column(TIMESTAMP, primary_key=True)

    user = relationship('User', back_populates='search_history')


class Notification(Base):
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    message = Column(Text, nullable=False)
    event_id = Column(Integer, ForeignKey('events.id', ondelete='SET NULL'), nullable=True)
    timestamp = Column(TIMESTAMP, nullable=False)

    user = relationship('User', back_populates='notifications')
    event = relationship('Event')

