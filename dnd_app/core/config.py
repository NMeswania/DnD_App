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

  def __init__(self, config: dict, common: dict):
    self.config = config
    self.common = common

###################################################################################################

  def __call__(self, node: str = ""):
    if (node != "") and (node in self.config.keys()):
      return Config(self.config[node], self.common)
    return self


###################################################################################################
###################################################################################################
###################################################################################################


class ConfigParser:

  def __init__(self, config_path: str):
    config_abs_path = Path(config_path).resolve()

    assert config_abs_path.is_file(), f"Config is not a file: {config_abs_path}"

    with open(config_path, 'r') as stream:
      try:
        config = yaml.safe_load(stream)

        if "dnd_app" not in config.keys():
          logging.critical("'dnd_app' not in config file, exiting.")
          sys.exit(0)

        self.config = config['dnd_app']
        self.common_config = self.config["common"]

      except yaml.YAMLError as exc:
        logging.critical(exc)

    logging.info("Successfully parsed config")

###################################################################################################

  def GetConfig(self):
    return Config(self.config, self.common_config)


###################################################################################################
###################################################################################################
###################################################################################################
