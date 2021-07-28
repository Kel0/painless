import os
import json
import logging
import logging.config

from settings import ABS_PATH


def setup_logging(path: str = os.path.join(ABS_PATH.parent, "logging.json")) -> None:
    with open(path, "rt") as f:
        config = json.load(f)
    logging.config.dictConfig(config)


setup_logging()
