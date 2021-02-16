import os
import uuid
import logging
import requests
from easytensor.urls import UPLOAD_URL_REQUEST_URL, MODELS_URL
from easytensor.auth import get_auth_token, needs_auth

LOGGER = logging.getLogger(__name__)


@needs_auth
def get_upload_url(model_name: str):
    """
    Requests a valid upload URL to uplaod the model to.
    """
    auth_token = get_auth_token()
    response = requests.post(
        UPLOAD_URL_REQUEST_URL,
        json={
            "filename": model_name,
            "contentType": "tar"
        },
        headers={
            "Authorization": "Bearer {}".format(auth_token)
        }
    )
    response.raise_for_status()
    res = response.json()
    return res["url"], res["method"]


def upload_model(filename):
    if not os.path.isfile(filename):
        LOGGER.error("Can not find file %s", filename)
        return
    auth_token = get_auth_token()

    size = os.path.getsize(filename)
    with open(filename, "rb") as fin:
        model = fin.read()
    model_id = str(uuid.uuid4())
    LOGGER.debug("model id: %s", model_id)
    upload_url, upload_method = get_upload_url(model_id)
    LOGGER.info("Uploading ...")
    response = requests.request(
        method=upload_method,
        url=upload_url,
        data=model,
        headers={"Content-Type": "application/octet-stream"}
    )
    response.raise_for_status()
    response = requests.post(
        MODELS_URL,
        json={
            "address": model_id,
            "name": filename.split("/")[-1],
            "size": size,
        },
        headers={"Authorization": "Bearer {}".format(auth_token)}
    )

    response.raise_for_status()
    print(response)