"""
A module for constants used throughout the library.
"""
from enum import Enum


class Framework(Enum):
    """
    An enum for the different types of frameworks supported in EasyTensor.
    """

    TENSORFLOW = "TF"
    PYTORCH = "PT"
