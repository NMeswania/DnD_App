###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

import logging

from pathlib import Path

from dnd_app.core.config import Config
from dnd_app.request_handler.request import Request
from dnd_app.request_handler.request_handler_manager import GetRequestHandlerManagerSingleton
from dnd_app.viewer_widgets.equipment_list.equipment_list_renderer import EquipmentListRenderer
from dnd_app.viewer_widgets.equipment_list.equipment_detail_renderer import EquipmentDetailRenderer
from dnd_app.viewer_widgets.widget_base import WidgetBase

###################################################################################################
###################################################################################################
###################################################################################################


class EquipmentList(WidgetBase):

  def __init__(self, config: Config, proficiencies_path: Path):
    self._dnd_config = config
    self._receipt = None
    self._LoadData(proficiencies_path)
    self._BuildRenderers()

###################################################################################################

  def __del__(self):
    self._renderer.Terminate()
    del self._renderer

###################################################################################################

  def renderers(self) -> EquipmentListRenderer:
    return self._renderer

###################################################################################################

  def CheckForUpdates(self):
    if self._receipt is not None:
      if self._receipt.IsResponseReady():
        response = self._receipt.GetResponse()

        response_type = response.request.type()
        if response_type == "character":
          self._renderer.Update(response.data())

        elif response_type == "equipment":
          self._detail_renderer.Update(response.data())

        else:
          logging.critical(
              f"Unknown response type in Equipment: {response_type}, id: {response.request.id()}")

        self._receipt = None

###################################################################################################

  def _LoadData(self, ability_score_path: Path):
    request = Request(type="character", value="subs/equipment_list")
    request_manager_singleton = GetRequestHandlerManagerSingleton()
    self._receipt = request_manager_singleton.Request(request)

###################################################################################################

  def _BuildRenderers(self) -> EquipmentListRenderer:
    self._renderer = EquipmentListRenderer(self._dnd_config, self)
    self._detail_renderer = EquipmentDetailRenderer(self)

###################################################################################################

  def RequestEquipmentCallback(self, equipment_name: str, index: int, instance):
    self._equipment_list_index = index
    request = Request(type="equipment", value=equipment_name)
    request_manager_singleton = GetRequestHandlerManagerSingleton()
    self._receipt = request_manager_singleton.Request(request)

###################################################################################################

  def RequestNextEquipmentCallback(self, increment: int, instance):
    equipment_name, self._equipment_list_index = self._renderer.GetNextEquipmentAndIndex(
        self._equipment_list_index + increment)
    self.RequestEquipmentCallback(equipment_name, self._equipment_list_index, instance)


###################################################################################################
###################################################################################################
###################################################################################################
