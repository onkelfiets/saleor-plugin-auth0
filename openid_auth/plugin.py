from typing import Optional

from authlib.integrations.requests_client import OAuth2Session
from django.core.handlers.wsgi import WSGIRequest
from saleor.account.models import User
from saleor.core.jwt import (
    JWT_REFRESH_TOKEN_COOKIE_NAME,
    get_token_from_request,
    get_user_from_access_token,
    jwt_decode,
)
from saleor.plugins.base_plugin import BasePlugin, ConfigurationTypeField

from .dataclasses import OpenIDAuthConfig


class OpenIDAuthPlugin(BasePlugin):
    PLUGIN_ID = "toastedtoast.authentication.openidauth"
    PLUGIN_NAME = "OpenID Auth"

    DEFAULT_CONFIGURATION = [
        {"name": "client_id", "value": None},
        {"name": "client_secret", "value": None},
        {"name": "json_web_key_set_url", "value": None},
    ]

    CONFIG_STRUCTURE = {
        "client_id": {
            "type": ConfigurationTypeField.STRING,
            "help_text": (
                "Your Client ID required to authenticate on the provider side."
            ),
            "label": "Client ID",
        },
        "client_secret": {
            "type": ConfigurationTypeField.SECRET,
            "help_text": (
                "Your client secret required to authenticate on provider side."
            ),
            "label": "Client Secret",
        },
        "json_web_key_set_url": {
            "type": ConfigurationTypeField.STRING,
            "help_text": (
                "The JSON Web Key Set (JWKS) is a set of keys containing the public "
                "keys used to verify any JSON Web Token (JWT) issued by the "
                "authorization server and signed using the RS256 signing algorithm."
            ),
            "label": "JSON Web Key Set URL",
        },
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Convert to dict to easier take config elements
        configuration = {item["name"]: item["value"] for item in self.configuration}
        self.config = OpenIDAuthConfig(
            client_id=configuration["client_id"],
            client_secret=configuration["client_secret"],
            json_web_key_set_url=configuration["json_web_key_set_url"],
        )
        self.oauth = self._get_oauth_session()

    def _get_oauth_session(self):
        scope = "openid profile email"
        if self.config.enable_refresh_token:
            scope += " offline_access"
        return OAuth2Session(
            client_id=self.config.client_id,
            client_secret=self.config.client_secret,
            scope=scope,
        )

    def authenticate_user(self, request: WSGIRequest, previous_value) -> Optional[User]:
        if not self.active:
            return previous_value
        # TODO this will be covered by tests and modified after we add Auth backend for
        #  plugins
        token = get_token_from_request(request)
        if not token:
            return None
        return get_user_from_access_token(token)
