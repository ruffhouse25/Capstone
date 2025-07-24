import json
from flask import request
from functools import wraps
from werkzeug.exceptions import HTTPException
import os

# Simplified auth for development/testing
AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN', 'dev-example.auth0.com')
API_AUDIENCE = os.environ.get('API_AUDIENCE', 'music-label-api')

# Mock tokens for testing (in production, these come from Auth0)
MOCK_TOKENS = {
    'assistant': {
        'permissions': ['get:artists', 'get:albums']
    },
    'director': {
        'permissions': ['get:artists', 'get:albums', 'post:artists', 'patch:artists', 'delete:artists', 'patch:albums']
    },
    'executive': {
        'permissions': ['get:artists', 'get:albums', 'post:artists', 'patch:artists', 'delete:artists', 'patch:albums', 'post:albums', 'delete:albums']
    }
}

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

def get_token_auth_header():
    """Get token from Authorization header (simplified for testing)"""
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    return token

def check_permissions(permission, payload):
    """Check if permission is in payload"""
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 403)
    return True

def verify_decode_jwt(token):
    """Simplified JWT verification for testing"""
    # In production, this would verify with Auth0
    # For testing, we use mock tokens
    if token in MOCK_TOKENS:
        return MOCK_TOKENS[token]
    else:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Unable to parse authentication token.'
        }, 400)

def requires_auth(permission=''):
    """Decorator for routes that require authentication"""
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                token = get_token_auth_header()
                payload = verify_decode_jwt(token)
                check_permissions(permission, payload)
                return f(payload, *args, **kwargs)
            except AuthError as e:
                raise e
            except HTTPException as e:
                # Let HTTP exceptions (like abort(404)) pass through
                raise e
            except Exception:
                raise AuthError({
                    'code': 'invalid_header',
                    'description': 'Unable to parse authentication token.'
                }, 400)

        return wrapper
    return requires_auth_decorator
