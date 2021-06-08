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
from dnd_app.viewer_widgets.weapon_list.weapon_list_renderer import WeaponListRenderer
from dnd_app.viewer_widgets.weapon_list.weapon_detail_renderer import WeaponDetailRenderer

###################################################################################################
###################################################################################################
###################################################################################################


class WeaponList(WidgetBase):

  def __init__(self, config: Config, weapon_list_path: Path):
    self._dnd_config = config
    self._receipt = None
    self._LoadData(weapon_list_path)
    self._BuildRenderers()

###################################################################################################

  def __del__(self):
    self._weapon_list_renderer.Terminate()
    self._weapon_detail_renderer.Terminate()
    del self._weapon_list_renderer
    del self._weapon_detail_renderer

###################################################################################################

  def renderers(self) -> list:
    return [self._weapon_list_renderer]

###################################################################################################

  def RequestWeaponCallback(self, weapon_name: str, instance):
    request = Request(type="weapon", value=weapon_name)
    request_manager_singleton = GetRequestHandlerManagerSingleton()
    self._receipt = request_manager_singleton.Request(request)

###################################################################################################

  def CheckForUpdates(self):
    if self._receipt is not None:
      if self._receipt.IsResponseReady():
        response = self._receipt.GetResponse()

        response_type = response.request.type()
        if response_type == "character":
          self._weapon_list_renderer.Update(response.data())

        elif response_type == "weapon":
          self._weapon_detail_renderer.Update(response.data())

        else:
          logging.critical(
              f"Unknown response type in Weapon: {response_type}, id: {response.request.id()}")

        self._receipt = None

###################################################################################################

  def _LoadData(self, weapon_list_path: Path):
    request = Request(type="character", value="subs/weapon_list")
    request_manager_singleton = GetRequestHandlerManagerSingleton()
    self._receipt = request_manager_singleton.Request(request)

###################################################################################################

  def _BuildRenderers(self):
    self._weapon_list_renderer = self._BuildWeaponListRenderer()
    self._weapon_detail_renderer = self._BuildWeaponDetailRenderer()

###################################################################################################

  def _BuildWeaponListRenderer(self) -> WeaponListRenderer:
    return WeaponListRenderer(self._dnd_config, self)

###################################################################################################

  def _BuildWeaponDetailRenderer(self) -> WeaponDetailRenderer:
    return WeaponDetailRenderer(self)


###################################################################################################
###################################################################################################
###################################################################################################
