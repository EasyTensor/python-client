"""
A module for saving and uploading pytorch models.
A PyTorch model requires slightly more pieces of information than a TensorFlow
model to run correctly.

1. The serialized parameters (weights and biases) of the model. EasyTensor takes
care of that for you.
2. The model class, including a prediction method. You have to do this. This
model class must include a predict_single method that can take in your native
input format (e.g. text, image bytes, number array) and return a human readible
output. You can think of the predict_single method as where the preprocess,
predict, and postprocess happens.
"""
import os
import io
import tarfile
import tempfile
import importlib
import inspect
import shutil
import logging
from pyflakes.api import checkRecursive
from pyflakes.reporter import Reporter

from easytensor.auth import needs_auth
from easytensor.constants import Framework
from easytensor.upload import (
    create_query_token,
    create_model_object,
    upload_archive,
)

# pylint: disable=protected-access
LOGGER = logging.getLogger(__name__)


def create_model_archive(model_weights_file, model_class_file):
    """
    Creates a temporary archvie of the model using the weights and class
    definition.
    The created archive's location is returned.
    """
    _, tar_location = tempfile.mkstemp()
    with tarfile.open(tar_location, "w:gz") as tarout:
        tarout.add(model_weights_file, arcname="model_weights")
        tarout.add(model_class_file, arcname="model.py")
    return tar_location


def check_model_class_definition_file(model_class_definition_file):
    """
    A function that checks the model class definition file exists and
    is formatted correctly to be served.
    """

    class BadModelFile(BaseException):
        """ An exception thrown for bad model files. """

    if not os.path.isfile(model_class_definition_file):
        raise FileNotFoundError(
            "Could not find the model class definition file {}".format(
                model_class_definition_file
            )
        )

    if (
        len(model_class_definition_file) < 3
        or model_class_definition_file[-3:] != ".py"
    ):
        raise BadModelFile(
            "Model class definition file ({}) is not a .py file.".format(
                model_class_definition_file
            )
        )
    warn_stream = io.StringIO("")
    error_stream = io.StringIO("")
    reporter = Reporter(warn_stream, error_stream)
    num_errors = checkRecursive(["model.py"], reporter)
    if num_errors > 0:
        raise BadModelFile(
            f"Found {num_errors} error(s) in model file. Please fix them and try again.\n"
            + warn_stream.getvalue()
        )

    module = importlib.import_module(model_class_definition_file[:-3])
    classes = [
        clas[1]
        for clas in inspect.getmembers(
            module,
            lambda member: inspect.isclass(member)
            and member.__module__ == module.__name__,
        )
    ]
    if len(classes) > 1:
        raise BadModelFile(
            "Expected only one class definition in the model class file. "
            "Found multiple: {}. Please include only your model's class definition.".format(
                classes
            )
        )

    if len(classes) < 1:
        raise BadModelFile(
            "Expected at least one class definition in the model file but found none. "
            "Please include the class definition of your model."
        )


@needs_auth
def upload_model(
    model_name,
    model,
    model_class_definition_file,
    create_token=True,
    checkpoint_dir=None,
):
    """
    Uploads the passed model and the model class definition to be served by EasyTensor.

    If checkpoint_dir is passed, the parameter will be used as the weights
    file and `model` will be ignored.

    Returns the model ID and a query access token.
    Creates a query access token for the model by default.
    """
    if checkpoint_dir is not None and not os.path.isdir(checkpoint_dir):
        raise FileNotFoundError(
            "Could not find the model weights file {}".format(checkpoint_dir)
        )

    check_model_class_definition_file(model_class_definition_file)
    temporary_directory = tempfile.mkdtemp()
    if checkpoint_dir is not None:
        model_directory = checkpoint_dir
    else:
        model_directory = os.path.join(temporary_directory, "model_weights")
        model.save_pretrained(model_directory)
    model_class_file = os.path.join(temporary_directory, "model.py")
    shutil.copy2(model_class_definition_file, model_class_file)
    archive_location = create_model_archive(model_directory, model_class_file)
    model_address, model_size = upload_archive(archive_location)
    model_id = create_model_object(
        model_address, model_name, model_size, Framework.TRANSFORMERS
    )
    if not create_token:
        return model_id, None
    return model_id, create_query_token(model_id)
    # return archive_location
