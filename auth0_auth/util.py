from typing import Optional
import requests
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


def extract_user_details_from_token_payload(payload: any, namespace: str):
    data = payload
    user_mail = (
        data[f"{namespace}/email"] if f"{namespace}/email" in data.keys() else None
    )
    first_name = (
        data[f"{namespace}/firstname"]
        if f"{namespace}/firstname" in data.keys()
        else None
    )
    last_name = (
        data[f"{namespace}/lastname"]
        if f"{namespace}/lastname" in data.keys()
        else None
    )

    return user_mail, first_name, last_name


def fetch_user_details_from_auth0(token: str, domain: str):
    data = requests.get(
        f"https://{domain}/userinfo", headers={"Authorization": f"Bearer {token}"}
    ).json()

    user_mail = data["email"] if "email" in data.keys() else None
    first_name = data[f"given_name"] if f"given_name" in data.keys() else None
    last_name = data[f"family_name"] if f"family_name" in data.keys() else None

    return user_mail, first_name, last_name
