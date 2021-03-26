"""
A module that exports the URLS needed for this library to work.
"""
from easytensor.config import get_config, update_config

BASE_URL = ""
AUTHENTICATION_URL = ""
REFRESH_TOKEN_URL = ""
UPLOAD_URL_REQUEST_URL = ""
MODELS_URL = ""
QUERY_TOKEN_URL = ""

# pylint: disable=global-statement


def reload_urls():
    """
    A handy method that reloads the URLS if any of them have been changed in the configuration.
    """
    global BASE_URL
    global AUTHENTICATION_URL
    global UPLOAD_URL_REQUEST_URL
    global REFRESH_TOKEN_URL
    global MODELS_URL
    global QUERY_TOKEN_URL
    config = get_config()
    BASE_URL = config.get("base_url", "https://app.easytensor.com")
    AUTHENTICATION_URL = BASE_URL + "/v1/dj-rest-auth/login/"
    REFRESH_TOKEN_URL = BASE_URL + "/v1/dj-rest-auth/token/refresh/"
    UPLOAD_URL_REQUEST_URL = BASE_URL + "/v1/model-uploads/"
    MODELS_URL = BASE_URL + "/v1/models/"
    QUERY_TOKEN_URL = BASE_URL + "/v1/query-access-token/"


reload_urls()


def set_base_url(url: str):
    """Resets the base URL. Handy for when running this library against localhost"""
    update_config({"base_url": url})
    reload_urls()
