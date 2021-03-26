"""
A module that helps upload tensorflow models to EasyTensor.
The only requirement for a model is that it is exported to disk.
Tensorflow models are packaged in a tar file and uploaded directly.
"""
import tarfile
import tempfile
import logging
from easytensor.upload import (
    create_query_token,
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
    model_address, model_size = upload_archive(archive_lcoation)
    model_id = create_model_object(
        model_address, model_name, model_size, Framework.TENSORFLOW
    )
    if not create_token:
        return model_id, None
    return model_id, create_query_token(model_id)
