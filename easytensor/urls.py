from easytensor.config import get_config

BASE_URL = ""
AUTHENTICATION_URL = ""
REFRESH_TOKEN_URL = ""
UPLOAD_URL_REQUEST_URL = ""
MODELS_URL = ""
QUERY_TOKEN_URL = ""


def reload_urls():
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
