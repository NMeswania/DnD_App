###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

import logging
from pathlib import Path
import sys
import yaml

###################################################################################################
###################################################################################################
###################################################################################################


class Config:

  def __init__(self, config_path: str):
    self.config = {}

    config_abs_path = Path(config_path).resolve()

    assert config_abs_path.is_file(), f"Config is not a file: {config_abs_path}"

    with open(config_path, 'r') as stream:
      try:
        self.config = yaml.safe_load(stream)

        if "dnd_app" not in self.config.keys():
          logging.critical("'dnd_app' not in config file, exiting.")
          sys.exit(0)

        self.config = self.config['dnd_app']

      except yaml.YAMLError as exc:
        logging.critical(exc)

    logging.info("Successfully parsed config")

###################################################################################################

  def __call__(self, node: str = "") -> dict:
    if (node != "") and (node in self.config.keys()):
      return self.config[node]
    return self.config


###################################################################################################
###################################################################################################
###################################################################################################
