###################################################################################################
# Copyright © 2021 Neal Meswania
# Lisence: MIT
###################################################################################################

import logging

from dnd_app.core.config import Config

from dnd_app.request_handler.request import Request
from dnd_app.request_handler.request_handler_manager import GetRequestHandlerManagerSingleton

from dnd_app.viewer_widgets.spell_list.spell_detail_renderer import SpellDetailRenderer
from dnd_app.viewer_widgets.spell_list.spell_list_renderer import SpellListRenderer
from dnd_app.viewer_widgets.widget_base import WidgetBase

###################################################################################################
###################################################################################################
###################################################################################################


class SpellList(WidgetBase):

  def __init__(self, config: Config, character: str):
    self._dnd_config = config
    self._receipt = None
    self._LoadData(character)
    self._BuildRenderers()
    self._spell_list_index = 0

###################################################################################################

  def __del__(self):
    self._spell_list_renderer.Terminate()
    self._detail_renderer.Terminate()
    del self._spell_list_renderer
    del self._detail_renderer

###################################################################################################

  def renderers(self) -> SpellListRenderer:
    return self._spell_list_renderer

###################################################################################################

  def RequestSpellCallback(self, spell_name: str, index: int, *args):
    self._spell_list_index = index
    request = Request(type="spell", value=spell_name)
    request_manager_singleton = GetRequestHandlerManagerSingleton()
    self._receipt = request_manager_singleton.Request(request)

###################################################################################################

  def RequestNextSpellCallback(self, increment: int):
    spell_name, self._spell_list_index = self._spell_list_renderer.GetNextSpellAndIndex(
        self._spell_list_index + increment)
    self.RequestSpellCallback(spell_name, self._spell_list_index)

###################################################################################################

  def CheckForUpdates(self):
    if self._receipt is not None:
      if self._receipt.IsResponseReady():
        response = self._receipt.GetResponse()

        response_type = response.request.type()
        if response_type == "character":
          self._spell_list_renderer.Update(response.data())

        elif response_type == "spell":
          self._detail_renderer.Update(response.data())

        else:
          logging.critical(
              f"Unknown response type in SpellList: {response_type}, id: {response.request.id()}")

        self._receipt = None

###################################################################################################

  def _LoadData(self, character: str):
    request = Request(type="character", value=f"{character}/spell_list")
    request_manager_singleton = GetRequestHandlerManagerSingleton()
    self._receipt = request_manager_singleton.Request(request)

###################################################################################################

  def _BuildRenderers(self):
    self._spell_list_renderer = self._BuildSpellListRenderer()
    self._detail_renderer = self._BuildSpellDetailRenderer()

###################################################################################################

  def _BuildSpellListRenderer(self) -> SpellListRenderer:
    return SpellListRenderer(self._dnd_config, self)

###################################################################################################

  def _BuildSpellDetailRenderer(self) -> SpellDetailRenderer:
    return SpellDetailRenderer(self)


###################################################################################################
###################################################################################################
###################################################################################################
