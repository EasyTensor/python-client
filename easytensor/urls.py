from easytensor.config import get_config

BASE_URL = ""
AUTHENTICATION_URL = ""

def reload_urls():
    global BASE_URL
    global AUTHENTICATION_URL
    config= get_config()
    BASE_URL = config.get("base_url", "https://app.easytensor.com")
    AUTHENTICATION_URL = BASE_URL+"/v1/dj-rest-auth/login/"

reload_urls()
