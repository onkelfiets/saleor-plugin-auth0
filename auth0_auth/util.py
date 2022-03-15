from typing import Optional
from django.core.handlers.wsgi import WSGIRequest


def get_token_auth_header(request: WSGIRequest) -> Optional[str]:
    """Obtains the Access Token from the Authorization Header"""
    auth_header = request.headers.get("Authorization", None)
    if not auth_header:
        print("No valid Authorization header found")
        return None

    header_parts = auth_header.split()

    if header_parts[0].lower() != "bearer":
        print("Authorization header must start with Bearer")
        return None

    elif len(header_parts) == 1:
        print("Token not found")
        return None

    elif len(header_parts) > 2:
        print("Token invalid")
        return None

    token = header_parts[1]
    return token
