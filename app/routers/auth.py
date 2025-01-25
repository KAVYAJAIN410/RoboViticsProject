from fastapi import APIRouter, Depends, HTTPException
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth, OAuthError
from sqlalchemy.orm import Session
from app.models import User  # Import User model
from app.database import get_db  # Import the get_db session dependency
import os
from dotenv import load_dotenv



# Load environment variables
load_dotenv()
CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID', None)
CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET', None)

router = APIRouter()


oauth = OAuth()
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    client_kwargs={
        'scope': 'email openid profile',
        'redirect_url': 'http://localhost:8000/auth'
    }
)

@router.get("/")
def index(request: Request):
    user = request.session.get('user')
    if user:
        return RedirectResponse('welcome')

@router.get('/welcome')
def welcome(request: Request):
    user = request.session.get('user')
    if not user:
        return RedirectResponse('/')
    return {"message": "Welcome"}

@router.get("/login")
async def login(request: Request):
    url = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, url)

@router.get('/auth')
async def auth(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        return {"message": "OAuth error occurred"}

    user_info = token.get('userinfo')
    if user_info:
        # Extract necessary user info from Google
        email = user_info['email']
        name = user_info['name']
        # Check if user already exists in the database
        user = db.query(User).filter(User.email == email).first()

        if not user:
            # Create new user if not exists
            user = User(
                name=name,
                email=email
            )
            db.add(user)
            db.commit()

        # Save the user information in session
        request.session['user'] = dict(user_info)

    return RedirectResponse('/welcome')

@router.get('/logout')
def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse('/')
