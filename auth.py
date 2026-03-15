import time
import requests
from threading import Lock
from typing import Optional
from TokenModel import Token
import config
from flask import current_app

_token_cache: Optional[Token] = None
_token_expires_at: float = 0.0
_lock = Lock()

def get_access_token() -> Token:
    """
    Returns a cached OAuth token if valid.
    Refreshes it only if expired.
    """
    global _token_cache, _token_expires_at

    now = time.time()

    if _token_cache and now < _token_expires_at:
        return _token_cache
    breakpoint()

    # Prevent concurrent refreshes
    with _lock:
        now = time.time()
        if _token_cache and now < _token_expires_at:
            return _token_cache

        client_id = current_app.config["CLIENT_ID"]
        client_secret = current_app.config["CLIENT_SECRET"]
        credentials = { client_id: client_secret }

        response = requests.post(
            "https://oauth.fatsecret.com/connect/token",
            auth=(client_id, client_secret),
            data={"grant_type": "client_credentials"},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=20
        )
        response.raise_for_status()
        data = response.json()

        token = Token(
            access_token=data["access_token"],
            token_type=data["token_type"],
            expires_in=int(data["expires_in"]),
        )

        # Cache with safety buffer (avoid edge expiry)
        _token_cache = token
        _token_expires_at = time.time() + token.expires_in - 60

        return token


def invalidate_token():
    global _token_cache, _token_expires_at
    _token_cache = None
    _token_expires_at = 0.0