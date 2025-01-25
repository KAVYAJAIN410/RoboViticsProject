import os
from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
from app.routers import auth, profile, exploreEvents, eventDetail, updateProfile, userHistory
from dotenv import load_dotenv
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import RedirectResponse

# Load environment variables from .env file
load_dotenv()

# Create FastAPI app instance
app = FastAPI()

# Load the secret key from the environment
secretKey = os.getenv('SECRET_KEY')

if not secretKey:
    raise ValueError("SECRET_KEY environment variable is missing.")

# Add the SessionMiddleware to the app first
app.add_middleware(SessionMiddleware, secret_key=secretKey)

# # Custom authentication middleware
# class AuthMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request: Request, call_next):
#         user = request.session.get('user')

#         # Check if user is authenticated (i.e., the user exists in session)
#         if not user and request.url.path not in ["/", "/login", "/auth"]:
#             return RedirectResponse(url='/')

#         # Continue to the next middleware or route handler
#         response = await call_next(request)
#         return response

# # Add the AuthMiddleware to the app (after SessionMiddleware)
# app.add_middleware(AuthMiddleware)

# Include routers for different paths
app.include_router(auth.router, prefix="", tags=["auth"])
app.include_router(profile.router, prefix="", tags=["profile"])
app.include_router(exploreEvents.router, prefix="", tags=["explore"])
app.include_router(eventDetail.router, prefix="", tags=["eventDetail"])
app.include_router(updateProfile.router, prefix="", tags=["editProfile"])
app.include_router(userHistory.router, prefix="", tags=["userHistory"])

# Root route
@app.get("/")
def read_root():
    return {"message": "Welcome to the RoboVitics"}
