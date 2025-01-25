from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import RedirectResponse
from fastapi import Request

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        user = request.session.get('user')

        # Check if user is authenticated (i.e., the user exists in session)
        if not user and request.url.path not in ["/", "/login", "/auth"]:
            return RedirectResponse(url='/')

        # Continue to the next middleware or route handler
        response = await call_next(request)
        return response
