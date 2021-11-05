import os
import json
import logging.config

"""
Die Inhalte logger_init.py und logging_config.json basieren auf dem
in der Vorlesung vorgestellten Beispiel "Minimalbeispiel Logger"
"""


def setup_logging(default_filename):
    path = os.path.join(os.path.dirname(__file__), default_filename)

    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)

        # set the directories for the logs to this folder
        config['handlers']['info_file_handler']['filename'] = os.path.join(
            os.path.dirname(__file__), config['handlers']['info_file_handler']['filename'])
        config['handlers']['warning_file_handler']['filename'] = os.path.join(
            os.path.dirname(__file__), config['handlers']['warning_file_handler']['filename'])
        config['handlers']['error_file_handler']['filename'] = os.path.join(
            os.path.dirname(__file__), config['handlers']['error_file_handler']['filename'])
        # set the logging
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=logging.INFO)
        get_logger(__name__).warn(
            "Config './Logger/logging_config.json' not found. Using standard logging settings ...")


def get_logger(module_name):
    return logging.getLogger(module_name)
