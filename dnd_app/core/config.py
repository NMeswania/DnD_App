###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

import logging
from pathlib import Path
import sys
import yaml

import dnd_app.core.config_exceptions as config_exceptions

###################################################################################################
###################################################################################################
###################################################################################################


class Config:

  def __init__(self, config: dict, common: dict, data_dir: Path):
    self.config = config
    self.common = common
    self.data_dir = data_dir

###################################################################################################

  def __call__(self, node: str=""):
    if (node != "") and (node in self.config.keys()):
      return Config(self.config[node], self.common, self.data_dir)
    return self

###################################################################################################

  def get(self, node: str=""):
    return self._get(self.config, node)

###################################################################################################

  def get_common(self, node: str=""):
    return self._get(self.common, node)

###################################################################################################

  def get_data_dir(self) -> Path:
    return self.data_dir

###################################################################################################

  def _get(self, config, node: str=""):
    if node in config.keys():
      return config[node]
    else:
      raise config_exceptions.NoNode(node)


###################################################################################################
###################################################################################################
###################################################################################################


class ConfigParser:

  def __init__(self, config_path: str, data_dir: str):
    config_abs_path = Path(config_path).resolve()
    data_dir_abs_path = Path(data_dir).resolve()

    assert config_abs_path.is_file(), f"Config is not a file: {config_abs_path}"
    assert data_dir_abs_path.is_dir(), f"Data dir is not a directory: {data_dir_abs_path}"

    with open(config_path, 'r') as stream:
      try:
        config = yaml.safe_load(stream)

        if "dnd_app" not in config.keys():
          logging.critical("'dnd_app' not in config file, exiting.")
          sys.exit(0)

        self.config = config['dnd_app']
        self.common_config = self.config['common']
        self.data_dir = data_dir_abs_path

      except yaml.YAMLError as exc:
        logging.critical(exc)

    logging.info("Successfully parsed config")

###################################################################################################

  def GetConfig(self):
    return Config(self.config, self.common_config, self.data_dir)


###################################################################################################
###################################################################################################
###################################################################################################
