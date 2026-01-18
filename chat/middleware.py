from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from channels.db import database_sync_to_async
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

class JwtCookieAuthMiddleware:
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        headers = dict(scope["headers"])
        
        if b"cookie" in headers:
            cookies = headers[b"cookie"].decode()
            cookies = dict(
                item.split("=") for item in cookies.split("; ")
            )
            access_token = cookies.get("access_token")
            
            if access_token:
                try:
                    jwt_auth = JWTAuthentication()
                    # Token validation is sync-safe (no DB calls)
                    validated_token = jwt_auth.get_validated_token(access_token)
                    # User retrieval requires DB access - must be async
                    scope["user"] = await self.get_user_from_validated_token(validated_token)
                except (InvalidToken, TokenError) as e:
                    print(f"Token validation error: {e}")
                    scope["user"] = AnonymousUser()
            else:
                scope["user"] = AnonymousUser()
        else:
            scope["user"] = AnonymousUser()
        
        return await self.app(scope, receive, send)
    
    @database_sync_to_async
    def get_user_from_validated_token(self, validated_token):
        """
        Get user from validated token - requires database access
        """
        try:
            jwt_auth = JWTAuthentication()
            user = jwt_auth.get_user(validated_token)
            return user
        except Exception as e:
            print(f"Error getting user: {e}")
            return AnonymousUser()