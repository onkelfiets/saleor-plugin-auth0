from dataclasses import dataclass


@dataclass
class OpenIDAuthConfig:
    client_id: str
    client_secret: str
    json_web_key_set_url: str
