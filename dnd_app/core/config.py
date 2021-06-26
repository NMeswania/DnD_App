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

CONFIG = r"dnd_app.yaml"
DATA_DIR = r"data"

###################################################################################################
###################################################################################################
###################################################################################################


class Config:

  def __init__(self, config: dict, common: dict, data_dir: Path):
    self._config = config
    self._common = common
    self._data_dir = data_dir

###################################################################################################

  def __call__(self, node: str = ""):
    if (node != "") and (node in self._config.keys()):
      return Config(self._config[node], self._common, self._data_dir)
    return self

###################################################################################################

  def get(self, node: str = ""):
    return self._get(self._config, node)

###################################################################################################

  def get_common(self, node: str = ""):
    return self._get(self._common, node)

###################################################################################################

  def get_data_dir(self) -> Path:
    return self._data_dir

###################################################################################################

  def _get(self, config, node: str = ""):
    if node in config.keys():
      return config[node]
    else:
      raise config_exceptions.NoNode(node)


###################################################################################################
###################################################################################################
###################################################################################################


class ConfigParser:

  def __init__(self):
    app_root_dir = Path(__file__).parent.parent
    config_abs_path = (app_root_dir / CONFIG).resolve()
    data_dir_abs_path = (app_root_dir / DATA_DIR).resolve()

    assert config_abs_path.is_file(), f"Config is not a file: {config_abs_path}"
    assert data_dir_abs_path.is_dir(), f"Data dir is not a directory: {data_dir_abs_path}"

    with open(config_abs_path, 'r') as stream:
      try:
        config = yaml.safe_load(stream)

        if "dnd_app" not in config.keys():
          logging.critical("'dnd_app' not in config file, exiting.")
          sys.exit(0)

        self._config = config['dnd_app']
        self._common_config = self._config['common']
        self._data_dir = data_dir_abs_path

      except yaml.YAMLError as exc:
        logging.critical(exc)

    logging.info("Successfully parsed config")

###################################################################################################

  def GetConfig(self):
    return Config(self._config, self._common_config, self._data_dir)


###################################################################################################
###################################################################################################
###################################################################################################
