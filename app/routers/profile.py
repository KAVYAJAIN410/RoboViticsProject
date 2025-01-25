from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from pydantic import BaseModel
from typing import Optional

class UserDetails(BaseModel):
    id: int
    email: str
    name: str
    registration_number: Optional[str] = None
    mobile_number: Optional[str] = None
    preference_embedding: Optional[str] = None

    class Config:
        orm_mode = True  

router = APIRouter()

@router.get('/profile', response_model=UserDetails)
def user_details(request: Request, db: Session = Depends(get_db)):

    # Get user info from the session
    user_info = request.session.get('user')
    
    if not user_info:
        raise HTTPException(status_code=401, detail="User not authenticated")
    
    email = user_info.get('email')  
    if not email:
        raise HTTPException(status_code=400, detail="Email not found in session")
    
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_data = {}
    
    if user.id is not None:
        user_data['id'] = user.id
    if user.registration_number is not None:
        user_data['registration_number'] = user.registration_number
    if user.email is not None:
        user_data['email'] = user.email
    if user.name is not None:
        user_data['name'] = user.name
    if user.mobile_number is not None:
        user_data['mobile_number'] = user.mobile_number
    if user.preference_embedding is not None:
        user_data['preference_embedding'] = user.preference_embedding

    return UserDetails(**user_data)
