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
from dnd_app.viewer_widgets.abilities_list.abilities_list_renderer import AbilitiesListRenderer
from dnd_app.viewer_widgets.abilities_list.abilities_detail_renderer import AbilitiesDetailRenderer

###################################################################################################
###################################################################################################
###################################################################################################


class AbilitiesList(WidgetBase):

  def __init__(self, config: Config, weapon_list_path: Path):
    self._dnd_config = config
    self._receipt = None
    self._LoadData(weapon_list_path)
    self._BuildRenderers()
    self._ability_list_index = 0

###################################################################################################

  def __del__(self):
    self._renderer.Terminate()
    del self._renderer

###################################################################################################

  def renderers(self) -> AbilitiesListRenderer:
    return self._renderer

###################################################################################################

  def RequestCallback(self, ability_name: str, index: int, *args):
    self._ability_list_index = index
    request = Request(type="ability", value=ability_name)
    request_manager_singleton = GetRequestHandlerManagerSingleton()
    self._receipt = request_manager_singleton.Request(request)

###################################################################################################

  def RequestNextAbilityCallback(self, increment: int):
    ability_name, self._ability_list_index = self._renderer.GetNextAbilityAndIndex(
        self._ability_list_index + increment)
    self.RequestCallback(ability_name, self._ability_list_index)

###################################################################################################

  def CheckForUpdates(self):
    if self._receipt is not None:
      if self._receipt.IsResponseReady():
        response = self._receipt.GetResponse()

        response_type = response.request.type()
        if response_type == "character":
          self._renderer.Update(response.data())

        elif response_type == "ability":
          self._detail_renderer.Update(response.data())

        else:
          logging.critical(f"Unknown response type in AbilityList: "
                           f"{response_type}, id: {response.request.id()}")

        self._receipt = None

###################################################################################################

  def _LoadData(self, weapon_list_path: Path):
    request = Request(type="character", value="subs/abilities_list")
    request_manager_singleton = GetRequestHandlerManagerSingleton()
    self._receipt = request_manager_singleton.Request(request)

###################################################################################################

  def _BuildRenderers(self):
    self._renderer = self._BuildAbilitiesListRenderer()
    self._detail_renderer = self._BuildAbilitiesDetailRenderer()

###################################################################################################

  def _BuildAbilitiesListRenderer(self) -> AbilitiesListRenderer:
    return AbilitiesListRenderer(self._dnd_config, self)

###################################################################################################

  def _BuildAbilitiesDetailRenderer(self) -> AbilitiesDetailRenderer:
    return AbilitiesDetailRenderer(self)


###################################################################################################
###################################################################################################
###################################################################################################
