import os
import tarfile
import tempfile
import uuid
import logging
import requests
from easytensor.urls import UPLOAD_URL_REQUEST_URL, MODELS_URL, QUERY_TOKEN_URL
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


def create_model_archive(model_location):
    """
    Creates a temporary archvie of the model and returns its location.
    """
    _, tar_location = tempfile.mkstemp()
    with tarfile.open(tar_location, "w:gz") as tarout:
        tarout.add(model_location, arcname="")
    return tar_location


def upload_model(model_name, model_location, create_token=True):
    """
    Returns the model ID and a query access token.
    Creates a query access token for the model by default.
    """
    archive_lcoation = create_model_archive(model_location)
    model_id = upload_archive(model_name, archive_lcoation)
    if not create_token:
        return model_id, None
    return model_id, create_query_token(model_id)


@needs_auth
def upload_archive(model_name, filename, create_token=True):
    """
    Uplaods the archive and returns the ID of the model that was uploaded.
    """
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
            "name": model_name,
            "size": size,
        },
        headers={"Authorization": "Bearer {}".format(auth_token)}
    )

    response.raise_for_status()
    res = response.json()
    return res["id"]


@needs_auth
def create_query_token(model_id):
    auth_token = get_auth_token()
    response = requests.post(
        QUERY_TOKEN_URL,
        json={
            "model": model_id
        },
        headers={"Authorization": "Bearer {}".format(auth_token)}
    )
    response.raise_for_status()
    res = response.json()
    return res["id"]
