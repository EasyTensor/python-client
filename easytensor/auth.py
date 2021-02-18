import logging
import functools
import getpass
import requests
from datetime import datetime, time, timedelta
from easytensor.config import get_config, update_config
from easytensor.urls import AUTHENTICATION_URL, REFRESH_TOKEN_URL

LOGGER = logging.getLogger(__name__)
DATETIME_STR_FORMAT = "%m/%d/%Y, %H:%M:%S"
TOKEN_EXPIRE_DELTA = timedelta(hours=24)


def check_auth():
    config = get_config()
    if "access_token" not in config:
        return False
    if "token_expire" not in config:
        return False
    token_expire = datetime.strptime(
        config["token_expire"], DATETIME_STR_FORMAT)
    if token_expire < datetime.now():
        return False
    return True


def ask_credentials():
    """
    Asks the user for username and password, and returns the JWT token
    used to access the account.
    """
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    return username, password


def attempt_auth(username: str, password: str):
    response = requests.post(
        url=AUTHENTICATION_URL,
        json={
            "username": username,
            "password": password
        }

    )
    resp = response.json()
    assert "access_token" in resp
    return resp["access_token"], resp["refresh_token"]


def get_auth_token():
    config = get_config()
    if not check_auth():
        username, password = ask_credentials()
        auth_token, refresh_token = attempt_auth(username, password)
        token_expire = (
            datetime.now() + TOKEN_EXPIRE_DELTA
        ).strftime(DATETIME_STR_FORMAT)
        update_config(
            {
                "access_token": auth_token,
                "token_expire": token_expire,
                "refresh_token": refresh_token,
            }
        )
        return auth_token
    return config["access_token"]


def refresh_auth():
    """
    Attemppts to refresh the authentication token using the refresh token.
    Returns False if refresh was not successful.
    Returns True if the refresh was successful.
    """
    config = get_config()
    if "refresh_token" not in config:
        return False
    response = requests.post(
        REFRESH_TOKEN_URL,
        json={
            "refresh": config["refresh_token"]
        }
    )

    if response.status_code == 401:
        LOGGER.debug("Refresh token expired.")
        return False
    response.raise_for_status()
    update_config({"access_token": response["access"]})
    return True


def needs_auth(func):
    """
    A decorator used to check authentication before performing
    the passed in function. If authentication is invalid or expired,
    the user is asked to provide credentials and is authenticated again.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not check_auth() and not refresh_auth():
            print("Access token is expired. Please reauthenticate.")
            # get_auth_token()
        return func(*args, **kwargs)
    return wrapper
