import os
import tarfile
import tempfile
import uuid
import logging
import requests
from easytensor.urls import UPLOAD_URL_REQUEST_URL, MODELS_URL, QUERY_TOKEN_URL
from easytensor.auth import get_auth_token, needs_auth
from easytensor.upload import (
    create_query_token,
    get_upload_url,
    create_model_object,
    upload_archive,
)
from easytensor.constants import Framework

LOGGER = logging.getLogger(__name__)


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
    model_address, model_size = upload_archive(model_name, archive_lcoation)
    model_id = create_model_object(
        model_address, model_name, model_size, Framework.TENSORFLOW
    )
    if not create_token:
        return model_id, None
    return model_id, create_query_token(model_id)
