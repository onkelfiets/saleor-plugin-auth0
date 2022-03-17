from typing import Optional

# from authlib.integrations.requests_client import OAuth2Session
from django.core.handlers.wsgi import WSGIRequest
from saleor.account.models import User
from saleor.core.auth import get_token_from_request
from saleor.core.jwt import get_user_from_access_payload, jwt_decode
from saleor.plugins.base_plugin import BasePlugin, ConfigurationTypeField

import jwt  # PyJWT
from jwt import PyJWKClient


from .dataclasses import Auth0AuthConfig
from .util import (
    extract_user_details_from_token_payload,
    fetch_user_details_from_auth0,
    get_token_auth_header,
)


class Auth0AuthPlugin(BasePlugin):
    PLUGIN_ID = "toastedtoast.authentication.openidauth"
    PLUGIN_NAME = "Auth0 Auth"

    DEFAULT_CONFIGURATION = [
        {"name": "domain", "value": None},
        {"name": "client_id", "value": None},
        {"name": "client_secret", "value": None},
        {"name": "audience", "value": None},
        {"name": "namespace", "value": None},
        {"name": "json_web_key_set_url", "value": None},
    ]

    CONFIG_STRUCTURE = {
        "domain": {
            "type": ConfigurationTypeField.STRING,
            "help_text": (
                "Your Auth0 domain. E.g. {name}.{region}.auth0.com. You can find it Applications > Applications > {APP} > Settings > Domain"
            ),
            "label": "Domain",
        },
        "client_id": {
            "type": ConfigurationTypeField.STRING,
            "help_text": (
                "Your Auth0 Client ID. You can find it Applications > Applications > {APP} > Settings > Client ID"
            ),
            "label": "Client ID",
        },
        "client_secret": {
            "type": ConfigurationTypeField.SECRET,
            "help_text": (
                "Your Auth0 client secret. You can find it Applications > Applications > {APP} > Settings > Client Secret"
            ),
            "label": "Client Secret",
        },
        "audience": {
            "type": ConfigurationTypeField.STRING,
            "help_text": (
                "The audience of the api configured in Auth0. Applications > APIs > {API} > Settings > Identifier"
            ),
            "label": "Audience",
        },
        "namespace": {
            "type": ConfigurationTypeField.STRING,
            "help_text": (
                "The namespace for custom token claims. Actions > Library > Custom > {Action}"
            ),
            "label": "Namespace",
        },
        "json_web_key_set_url": {
            "type": ConfigurationTypeField.STRING,
            "help_text": (
                "The JSON Web Key Set (JWKS) is a set of keys containing the public "
                "keys used to verify any JSON Web Token (JWT) issued by the "
                "authorization server and signed using the RS256 signing algorithm. This should be: https://{domain}/.well-known/jwks.json"
            ),
            "label": "JSON Web Key Set URL",
        },
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Convert to dict to easier take config elements
        configuration = {item["name"]: item["value"] for item in self.configuration}
        self.config = Auth0AuthConfig(
            domain=configuration["domain"],
            client_id=configuration["client_id"],
            client_secret=configuration["client_secret"],
            audience=configuration["audience"],
            namespace=configuration["namespace"],
            json_web_key_set_url=configuration["json_web_key_set_url"],
        )

    def authenticate_user(self, request: WSGIRequest, previous_value) -> Optional[User]:
        if not self.active:
            return previous_value

        print(request)
        token = get_token_auth_header(request)
        if not token:
            raise Exception(f"No token found: {request}")

        try:

            jwks_client = PyJWKClient(self.config.json_web_key_set_url)
            signing_key = jwks_client.get_signing_key_from_jwt(token)

        except Exception as e:
            print(e)
            raise Exception(f"Token: {token} --- {e}")

        if not signing_key:
            raise Exception(f"No signing key found: {token}")

        data = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience=self.config.audience,
        )

        if not data:
            raise Exception(f"Cannot Decode data: {data}")

        # Extract user details
        user_mail, first_name, last_name = extract_user_details_from_token_payload(
            payload=data, namespace=self.config.namespace
        )

        if not user_mail:
            user_mail, first_name, last_name = fetch_user_details_from_auth0(
                token=token, domain=self.config.domain
            )

        # get or create user.
        user, created = User.objects.get_or_create(
            email=user_mail,
            defaults={
                "first_name": first_name if first_name else "",
                "last_name": last_name if last_name else "",
                "is_active": True,
                "is_staff": False,
                "is_superuser": False,
            },
        )

        # Add sub to user when created
        if created:
            sub = data["sub"]
            user.store_value_in_metadata({"sub": sub})
            user.save()

        print(user)
        return user
