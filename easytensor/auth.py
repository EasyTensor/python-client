import getpass
import requests
from easytensor.config import get_config, update_config
from easytensor.urls import AUTHENTICATION_URL


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
    return resp["access_token"]


def authenticate():
    config = get_config()
    if "auth_token" not in config:
        username, password = ask_credentials()
        auth_token = attempt_auth(username, password)
        update_config({"auth_token": auth_token})
        return auth_token
    return config["auth_token"]
