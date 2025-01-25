from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from pydantic import EmailStr
from typing import Optional

from pydantic import BaseModel

class ProfileUpdate(BaseModel):
    name: Optional[str] = None  
    email: Optional[EmailStr] = None  

router = APIRouter()

@router.put('/profile/edit')
async def update_profile(profile: ProfileUpdate, request: Request, db: Session = Depends(get_db)):
    
    
    user_info = request.session.get('user')
    
    if not user_info:
        raise HTTPException(status_code=401, detail="User not authenticated")

    user_id = user_info.get('id')


    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    
    if profile.name:
        user.name = profile.name
    

    if profile.email:
        user.email = profile.email

  
    db.commit()
    
    return {"message": "Profile updated successfully!"}
