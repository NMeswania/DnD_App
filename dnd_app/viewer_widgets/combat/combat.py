###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

import logging

from pathlib import Path

from dnd_app.core.config import Config
from dnd_app.request_handler.request import Request
from dnd_app.request_handler.request_handler_manager import GetRequestHandlerManagerSingleton
from dnd_app.viewer_widgets.widget_base import WidgetBase
from dnd_app.viewer_widgets.combat.combat_renderer import CombatRenderer

###################################################################################################
###################################################################################################
###################################################################################################


class Combat(WidgetBase):

  def __init__(self, config: Config, weapon_list_path: Path):
    self._dnd_config = config
    self._receipt = None
    self._LoadData(weapon_list_path)
    self._BuildRenderers()

###################################################################################################

  def __del__(self):
    self._renderer.Terminate()
    del self._renderer

###################################################################################################

  def renderers(self) -> list:
    return [self._renderer]

###################################################################################################

  def RequestCallback(self, type: str, value: str, instance):
    request = Request(type=type, value=value)
    request_manager_singleton = GetRequestHandlerManagerSingleton()
    self._receipt = request_manager_singleton.Request(request)

###################################################################################################

  def CheckForUpdates(self):
    if self._receipt is not None:
      if self._receipt.IsResponseReady():
        response = self._receipt.GetResponse()

        response_type = response.request.type()
        if response_type == "character":
          self._renderer.Update(response.data())

        else:
          logging.critical(
              f"Unknown response type in Weapon: {response_type}, id: {response.request.id()}")

        self._receipt = None

###################################################################################################

  def _LoadData(self, weapon_list_path: Path):
    request = Request(type="character", value="subs/combat")
    request_manager_singleton = GetRequestHandlerManagerSingleton()
    self._receipt = request_manager_singleton.Request(request)

###################################################################################################

  def _BuildRenderers(self):
    self._renderer = CombatRenderer(self._dnd_config, self)


###################################################################################################
###################################################################################################
###################################################################################################
