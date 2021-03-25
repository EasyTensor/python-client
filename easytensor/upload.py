import os
import tarfile
import tempfile
import uuid
import logging
import requests
from easytensor.urls import UPLOAD_URL_REQUEST_URL, MODELS_URL, QUERY_TOKEN_URL
from easytensor.auth import get_auth_token, needs_auth
from easytensor.constants import Framework

LOGGER = logging.getLogger(__name__)


@needs_auth
def get_upload_url(model_name: str):
    """
    Requests a valid upload URL to uplaod the model to.
    """
    auth_token = get_auth_token()
    response = requests.post(
        UPLOAD_URL_REQUEST_URL,
        json={"filename": model_name, "contentType": "tar"},
        headers={"Authorization": "Bearer {}".format(auth_token)},
    )
    response.raise_for_status()
    res = response.json()
    return res["url"], res["method"]


@needs_auth
def upload_archive(model_name, filename, create_token=True):
    """
    Uplaods the archive and returns the ID of the model that was uploaded.
    """
    if not os.path.isfile(filename):
        LOGGER.error("Can not find file %s", filename)
        return
    size = os.path.getsize(filename)
    with open(filename, "rb") as fin:
        model = fin.read()
    model_address = str(uuid.uuid4())
    upload_url, upload_method = get_upload_url(model_address)
    LOGGER.info("Uploading ...")
    response = requests.request(
        method=upload_method,
        url=upload_url,
        data=model,
        headers={"Content-Type": "application/octet-stream"},
    )
    response.raise_for_status()
    return model_address, size


@needs_auth
def create_model_object(address: str, name: str, size: int, framework: Framework):
    """
    Creates a model object in EasyTensor backend.
    address: the remote address of the model.
    name: the display name of the model.
    size: the size of the file on disk.
    """
    assert isinstance(framework, Framework)
    auth_token = get_auth_token()
    response = requests.post(
        MODELS_URL,
        json={
            "address": address,
            "name": name,
            "size": size,
            "framework": framework.value,
        },
        headers={"Authorization": "Bearer {}".format(auth_token)},
    )

    response.raise_for_status()
    res = response.json()
    return res["id"]


@needs_auth
def create_query_token(model_id):
    auth_token = get_auth_token()
    response = requests.post(
        QUERY_TOKEN_URL,
        json={"model": model_id},
        headers={"Authorization": "Bearer {}".format(auth_token)},
    )
    response.raise_for_status()
    res = response.json()
    return res["id"]
