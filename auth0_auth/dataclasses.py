from dataclasses import dataclass


@dataclass
class Auth0AuthConfig:
    audience: str
    domain: str
    client_id: str
    client_secret: str
    json_web_key_set_url: str
    namespace: str
