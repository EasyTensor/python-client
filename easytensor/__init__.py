"""
Main module. Imports some functions to expose at the top level.
"""
from easytensor.auth import get_auth_token
from easytensor.urls import set_base_url
from easytensor.constants import Framework
from easytensor import tensorflow
from easytensor import pytorch
