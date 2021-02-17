import os
from pathlib import Path
import json
import logging

LOGGER = logging.getLogger(__name__)

_EASYTENSOR_PATH = os.path.join(str(Path.home()), ".easytensor")
_CONFIG_PATH = os.path.join(_EASYTENSOR_PATH, "config.json")


def get_config():
    """
    Returns the config for the user.
    If no config object is stored, it will create a new one and return it.
    """
    ensure_easytensor_config()
    with open(_CONFIG_PATH) as fin:
        return json.load(fin)


def ensure_easytensor_path():
    if not os.path.isdir(_EASYTENSOR_PATH):
        os.mkdir(_EASYTENSOR_PATH)


def ensure_easytensor_config():
    """
    Checks that there is a config file for the user and creates one if not.
    """
    ensure_easytensor_path()
    # ensure file exists
    if not os.path.isfile(_CONFIG_PATH):
        with open(_CONFIG_PATH, "w") as fout:
            json.dump({}, fout, indent=2)
        return

    # if it exists, ensure that it's valid json
    try:
        with open(_CONFIG_PATH) as fin:
            config = json.load(fin)
            if not isinstance(config, dict):
                raise BaseException("config is malformed.")
    except BaseException:
        LOGGER.warning(
            "Config at %s is malformed. Repacing with an empty config.", _CONFIG_PATH)
        os.remove(_CONFIG_PATH)
        with open(_CONFIG_PATH, "w") as fout:
            json.dump({}, fout, indent=2)


def update_config(updates: dict):
    """
    Updates the config dictionary with the dictioanry that is passed.
    """
    current = get_config()
    current.update(updates)
    _store_config(current)


def _store_config(config: dict):
    """
    Stoers the config dictionary into the config path.
    """
    ensure_easytensor_config()
    with open(_CONFIG_PATH, "w") as fout:
        json.dump(config, fout, indent=2)
